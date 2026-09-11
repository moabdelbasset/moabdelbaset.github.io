# GitOps Application Delivery on OpenShift

This guide records the development milestone completed by September 11, 2026: building a Flask portfolio, publishing its tested container to Quay, deploying with OpenShift GitOps, correcting configuration drift, and releasing a content change through a GitOps PR.

The commands reconstruct the completed workflow from the implementation repositories and recorded session results. They are documentation, not commands rerun against the cluster during writing. Expected results are labeled separately from recorded evidence. The repository names intentionally retain the existing spelling `portolio`.

## Scope and environment

| Item | Recorded value |
| --- | --- |
| OpenShift | 4.22.11 |
| Nodes | Three Ready amd64 nodes, control-plane/master/worker roles |
| Infrastructure | KVM/libvirt VMs on one Hetzner dedicated server |
| OpenShift GitOps | 1.21.4, installed through the GUI |
| Application namespace | portfolio-development |
| Argo CD namespace | openshift-gitops |
| Application | Flask, Gunicorn, JSON content; no database or PVC |
| Registry | Public Quay image repository |
| GitOps source | Public GitHub repository |

This cluster has one physical failure domain. The development application requests one replica. Neither arrangement demonstrates host-level availability.

## Repositories and flow

- [Application repository](https://github.com/moabdelbasset/portolio-flask)
- [GitOps repository](https://github.com/moabdelbasset/portolio-flask-gitops)
- [Quay repository](https://quay.io/repository/moabdelbasset/portolio-flask)
- [Cluster installation](https://github.com/moabdelbasset/home-lab/wiki/Install-Openshift-Cluster-on-Hetzner-server)

```text
Edit Flask/content → GitHub Actions tests/build/smoke test → Quay
                                                             |
                                               Copy digest manually
                                                             |
                       GitOps pull request → Merge to main → Argo CD
                                                             |
                                            Deployment → Service → Route
```

A new Quay image alone does not trigger a release. Argo CD reads the GitOps repository; the digest-update PR is currently created manually. No webhook or automated cross-repository PR creation was demonstrated.

## 1. Prepare local tools and access

Use Git, Python (3.12 matches CI and the image), Docker or Podman, and an authenticated `oc` CLI. A working cluster and permission to install the GitOps operator and create namespaces are prerequisites. Configure your own GitHub and Quay accounts if reproducing this outside the original lab.

Check the target before making changes:

```sh
oc whoami
oc get clusterversion
oc get nodes -L kubernetes.io/arch
oc get ingress.config.openshift.io cluster \
  -o jsonpath='{.spec.domain}{"\n"}'
```

Recorded: OpenShift `4.22.11`, three Ready `amd64` nodes, and `apps.ocp-lab.aymantech.net` as the application domain. Adapt the domain and repository ownership throughout when using another environment.

## 2. Build the Flask portfolio

Application files:

```text
portolio-flask/
├── app.py
├── content.json
├── templates/index.html
├── static/style.css
├── requirements.txt
├── requirements.lock.txt
├── tests/test_app.py
├── Dockerfile
└── .github/workflows/ci.yml
```

`content.json` supplies profile text, skills, and projects. `templates/index.html` renders those values, and `static/style.css` controls presentation. The two Flask endpoints are `/` for the portfolio and `/healthz` for process health.

The application implementation:

```python
"""Personal portfolio. Edit content.json to customize the page."""
import json
from pathlib import Path
from flask import Flask, render_template

app = Flask(__name__)

@app.get('/')
def index():
    content = json.loads(Path(__file__).with_name('content.json').read_text())
    return render_template('index.html', **content)

@app.get('/healthz')
def health():
    return {'status': 'ok'}, 200
```

To reproduce the recorded source, clone the application and check out the demonstrated release commit on a new local branch. For ongoing work, use the repository's current main branch instead.

```sh
git clone https://github.com/moabdelbasset/portolio-flask.git
cd portolio-flask
git switch -c reproduce-development 4f2c57a9aab9c272dd5ccc77b4c6f0608c67a1ed
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock.txt
python -m unittest discover -s tests -v
flask --app app run --port 5050
```

Open `http://127.0.0.1:5050`. Stop the development server with Ctrl+C before continuing. The Flask development server is for local checks; the deployed container uses Gunicorn.

The seven automated tests cover:

1. Home-page rendering and project links.
2. HTML escaping of profile content.
3. Stylesheet delivery.
4. The JSON health response.
5. Health response independence from the content file.
6. A 404 for unknown pages.
7. Rejection of POST requests to read-only routes.

The expected test result is seven passing tests. `/healthz` does not validate portfolio rendering, which is why readiness later checks `/`.

## 3. Containerize and smoke-test

The Dockerfile used for the milestone:

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app
COPY requirements.lock.txt ./
RUN pip install --no-cache-dir -r requirements.lock.txt

COPY app.py content.json ./
COPY templates/ ./templates/
COPY static/ ./static/

# Arbitrary OpenShift UIDs can read the app; runtime writes go to /tmp.
RUN chmod -R a+rX /app
USER 1001:0
EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--worker-tmp-dir", "/tmp", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
```

The image uses pinned Python dependencies, but `python:3.12-slim` is a mutable base tag. An image digest identifies the published artifact; it does not make future rebuilds from that base tag identical.

Build and run locally:

```sh
docker build -t portfolio:local .
docker run --rm --name portfolio -p 127.0.0.1:8080:8080 \
  --user 1001230000:0 --read-only \
  --tmpfs /tmp:rw,nosuid,nodev,size=64m \
  --cap-drop ALL --security-opt no-new-privileges portfolio:local
```

In a second terminal:

```sh
curl --fail http://127.0.0.1:8080/healthz
curl --fail --output /dev/null http://127.0.0.1:8080/
```

Expect a JSON health response and a successful page request. The image's default UID is 1001, but this test overrides it to check arbitrary-UID compatibility. Gunicorn writes worker temporary files under `/tmp`, and logs go to stdout/stderr. Stop the container with Ctrl+C.

A build on an ARM laptop can produce an ARM image. The demonstrated release was built in CI for the amd64 cluster; do not substitute a laptop-built image without checking architecture.

## 4. Configure Quay publishing

The final registry choice was Quay. In Quay, create `portolio-flask` under your account or organization. The recorded lab repository is public, so the cluster can pull without an image-pull Secret.

Create a robot account with Write permission on that repository. In the application repository on GitHub, use **Settings → Secrets and variables → Actions** to store:

| Secret name | Value |
| --- | --- |
| QUAY_USERNAME | Full Quay robot-account username |
| QUAY_TOKEN | Robot-account token |

Enter credentials directly in the secret settings. Do not put their values in Git or this guide. These credentials are for publishing; Argo CD reads the separate public GitOps repository without Git credentials.

## 5. Add GitHub Actions CI

Save the workflow as `.github/workflows/ci.yml`. This is the implementation used for the recorded milestone:

```yaml
name: Portfolio CI

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Check out source code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: python -m pip install -r requirements.lock.txt

      - name: Run tests
        run: python -m unittest discover -s tests -v

  build:
    needs: test
    runs-on: ubuntu-latest
    
    steps:
      - name: source code checkout
        uses: actions/checkout@v4

      - name: Build Docker image
        run: docker build --tag portfolio:ci .

      - name: Start container
        run: |
          docker run --detach --name portfolio \
            --publish 127.0.0.1:8080:8080 \
            --user 1001230000:0 \
            --read-only \
            --tmpfs /tmp:rw,nosuid,nodev,size=64m \
            portfolio:ci

      - name: Check container responds
        run: |
          curl --fail --show-error \
            --retry 10 --retry-all-errors --retry-delay 2 \
            --connect-timeout 2 --max-time 5 \
            http://127.0.0.1:8080/healthz

          curl --fail --show-error --max-time 5 \
            --output /dev/null \
            http://127.0.0.1:8080/

      - name: Log in to Quay
        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
        env:
          QUAY_USERNAME: ${{ secrets.QUAY_USERNAME }}
          QUAY_TOKEN: ${{ secrets.QUAY_TOKEN }}
        run: |
          printf '%s' "$QUAY_TOKEN" |
            docker login quay.io \
              --username "$QUAY_USERNAME" \
              --password-stdin

      - name: Publish tested image to Quay
        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
        env:
          IMAGE_NAME: quay.io/moabdelbasset/portolio-flask
        run: |
          IMAGE_TAG="$IMAGE_NAME:$GITHUB_SHA"

          docker tag portfolio:ci "$IMAGE_TAG"
          docker push "$IMAGE_TAG"

          IMAGE_DIGEST=$(docker image inspect "$IMAGE_TAG" \
            --format '{{index .RepoDigests 0}}')

          echo "### Published image" >> "$GITHUB_STEP_SUMMARY"
          echo "- Tag: \`$IMAGE_TAG\`" >> "$GITHUB_STEP_SUMMARY"
          echo "- Digest reference: \`$IMAGE_DIGEST\`" >> "$GITHUB_STEP_SUMMARY"

      - name: Show container logs
        if: always()
        run: docker logs portfolio

      - name: Remove container
        if: always()
        run: docker rm --force portfolio
```

Pull requests run tests, build, and smoke-test. Successful pushes to `main` additionally publish the already-tested image. The commit SHA becomes its tag, and the workflow summary reports the digest reference. The CI smoke test checks arbitrary UID/read-only operation; the additional capability restrictions are specified in the deployed manifest and local command above.

Commit the application changes and push them to your repository. In **Actions**, confirm that tests, build, both HTTP checks, and publishing pass. Copy the digest from **Published image** in the run summary.

The initial published artifact was:

```text
Source commit: 23b6ca4edd5500c1c245786b1b63dc5737d1e9f5
quay.io/moabdelbasset/portolio-flask@sha256:0a74a984dc17d241bcc50be54a8d62a5b8bb02b047ce8c0ebc6d07e09ed815b7
```

## 6. Install OpenShift GitOps through the GUI

The completed installation used the OpenShift web console. The CLI installation alternative discussed during preparation was not the method used.

1. In the Administrator console, open the operator catalog/OperatorHub.
2. Search for **Red Hat OpenShift GitOps** and select **Install**.
3. Use the `gitops-1.21` channel and `openshift-gitops-operator` installation namespace, with all-namespace scope. The setup guidance selected automatic update approval and cluster monitoring.
4. Wait for the installation to succeed, then verify the installed version and default instance.

The channel selects a release stream, not a fixed patch version. The recorded CSV showed `1.21.4`; future installations may offer different versions. The exact saved subscription settings were not exported in the session.

```sh
oc get csv -n openshift-gitops-operator
oc get argocd -n openshift-gitops
oc get pods -n openshift-gitops
oc rollout status deployment/openshift-gitops-server \
  -n openshift-gitops --timeout=180s
oc get route openshift-gitops-server -n openshift-gitops \
  -o jsonpath='https://{.spec.host}{"\n"}'
```

Recorded: CSV `openshift-gitops-operator.v1.21.4` in `Succeeded` phase and an `openshift-gitops` Argo CD instance. Initially the server pod was Running but `0/1` ready; running and ready are different states.

## 7. Resolve Cloudflare DNS access

Console and Argo CD access worked with local `/etc/hosts` overrides but failed through proxied cluster records. The recorded fix was switching the cluster records to **DNS only** in Cloudflare:

| Record in the aymantech.net zone | Target | Mode |
| --- | --- | --- |
| api.ocp-lab | Dedicated server public IP | DNS only |
| *.apps.ocp-lab | Dedicated server public IP | DNS only |
| Any existing explicit console record | Dedicated server public IP | DNS only |

The wildcard supplies DNS for console, OAuth, Argo CD, and portfolio Routes. Check existing exact records too, since they take precedence over a wildcard. With DNS-only records, clients connect directly to the server and OpenShift handles TLS.

The API uses port 6443, outside [Cloudflare's standard HTTP proxy supported ports](https://developers.cloudflare.com/fundamentals/reference/network-ports/). The earlier discussion also considered certificate coverage for deeply nested hostnames, but did not establish that as a separate confirmed root cause.

```sh
dig @1.1.1.1 +short api.ocp-lab.aymantech.net
dig @1.1.1.1 +short console-openshift-console.apps.ocp-lab.aymantech.net
dig @1.1.1.1 +short oauth-openshift.apps.ocp-lab.aymantech.net
dig @1.1.1.1 +short openshift-gitops-server-openshift-gitops.apps.ocp-lab.aymantech.net
```

Expect the dedicated server's public IP. After confirming DNS, remove or comment out only the matching cluster overrides in `/etc/hosts`. On macOS, if cached results persist:

```sh
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

Retry browser access and `oc get nodes`. DNS changes do not fix a separate certificate-trust problem; investigate the actual certificate error if one remains.

## 8. Access Argo CD

Open the Route returned in step 6. Use **Log in via OpenShift** when available. Alternatively, the default instance's local username is `admin`; retrieve its existing password in the console under **openshift-gitops → Secrets → openshift-gitops-cluster → admin.password**. Do not include the revealed value in screenshots or documentation.

Recorded outcome: access to Argo CD worked after the DNS fix and login guidance.

## 9. Create the GitOps repository and base

Create a separate repository on GitHub, `portolio-flask-gitops`, and clone it. This repository contains deployment configuration, not a second copy of the Flask source.

```text
portolio-flask-gitops/
├── base/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── route.yaml
│   └── kustomization.yaml
├── overlays/development/kustomization.yaml
└── argocd/development.yaml
```

The following base files reproduce the initial deployment configuration.

### `base/deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: portfolio
spec:
  replicas: 1
  selector:
    matchLabels:
      app: portfolio
  template:
    metadata:
      labels:
        app: portfolio
    spec:
      automountServiceAccountToken: false
      securityContext:
        runAsNonRoot: true
        seccompProfile:
          type: RuntimeDefault
      containers:
        - name: portfolio
          image: quay.io/moabdelbasset/portolio-flask@sha256:0a74a984dc17d241bcc50be54a8d62a5b8bb02b047ce8c0ebc6d07e09ed815b7
          ports:
            - name: http
              containerPort: 8080
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 256Mi
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
          startupProbe:
            httpGet:
              path: /healthz
              port: http
            periodSeconds: 2
            failureThreshold: 30
          readinessProbe:
            httpGet:
              path: /
              port: http
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /healthz
              port: http
            periodSeconds: 20
          volumeMounts:
            - name: tmp
              mountPath: /tmp
      volumes:
        - name: tmp
          emptyDir:
            sizeLimit: 64Mi
```

### `base/service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: portfolio
spec:
  selector:
    app: portfolio
  ports:
    - name: http
      port: 8080
      targetPort: http
  type: ClusterIP
```

### `base/route.yaml`

```yaml
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: portfolio
spec:
  to:
    kind: Service
    name: portfolio
  port:
    targetPort: http
  tls:
    termination: edge
    insecureEdgeTerminationPolicy: Redirect
```

### `base/kustomization.yaml`

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - deployment.yaml
  - service.yaml
  - route.yaml
```

The Deployment requests one replica and leaves `runAsUser` unset so OpenShift can assign its UID. It drops capabilities, disables privilege escalation, uses a read-only root filesystem, and does not mount a service-account token. `/tmp` uses a 64 MiB `emptyDir`; that is ephemeral storage, not a persistent volume.

CPU/memory requests and limits are starting settings, not load-tested sizing. The startup and liveness probes check `/healthz`, while readiness checks page rendering at `/`.

The Service selects `app: portfolio` and forwards port 8080 to the named container port. The edge-terminated Route handles HTTPS at the router and forwards HTTP internally; HTTP clients are redirected to HTTPS.

From the GitOps repository root:

```sh
oc kustomize base
```

This renders YAML locally; it does not apply it or validate it against the live cluster.

## 10. Add the development overlay

For the first deployment, use the initial digest in `overlays/development/kustomization.yaml`:

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: portfolio-development

resources:
  - ../../base

images:
  - name: quay.io/moabdelbasset/portolio-flask
    digest: sha256:0a74a984dc17d241bcc50be54a8d62a5b8bb02b047ce8c0ebc6d07e09ed815b7

patches:
  - target:
      group: route.openshift.io
      version: v1
      kind: Route
      name: portfolio
    patch: |-
      - op: add
        path: /spec/host
        value: portfolio-development.apps.ocp-lab.aymantech.net
```

The overlay assigns the namespace, selects the image digest, and patches the Route hostname. It does not create the namespace. The final milestone changes only its digest to the newer image in step 14.

```sh
oc kustomize overlays/development
git add base/ overlays/development/
git commit -m "Add portfolio base and development overlay"
git push
```

Inspect the rendered namespace, image reference, and Route host before committing.

## 11. Bootstrap namespace access and the Application

```sh
oc create namespace portfolio-development
oc label namespace portfolio-development \
  argocd.argoproj.io/managed-by=openshift-gitops
```

For an already-existing namespace, inspect it before reusing it. The managed-by label enables operator-managed access for the default instance. See [Red Hat's namespace management guidance](https://docs.redhat.com/en/documentation/red_hat_openshift_gitops/1.21/html/multitenancy/multitenancy-support-in-gitops).

The initial `argocd/development.yaml` deliberately omitted automatic synchronization:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: portfolio-development
  namespace: openshift-gitops
spec:
  project: default

  source:
    repoURL: https://github.com/moabdelbasset/portolio-flask-gitops.git
    targetRevision: main
    path: overlays/development

  destination:
    server: https://kubernetes.default.svc
    namespace: portfolio-development
```

```sh
git add argocd/development.yaml
git commit -m "Add development Argo CD application"
git push
oc apply -f argocd/development.yaml
```

The Application object lives in `openshift-gitops`; its workloads belong in `portfolio-development`. Its source points to `main` and `overlays/development` in GitHub.

## 12. Perform the first synchronization

Creating the Application initially produced no workloads because synchronization was manual. This was expected.

1. Open **portfolio-development** in Argo CD.
2. Inspect the missing/out-of-sync Deployment, Service, and Route.
3. Select **Sync → Synchronize**.
4. Wait for **Synced / Healthy**.

```sh
oc get pods,svc,route -n portfolio-development
oc rollout status deployment/portfolio \
  -n portfolio-development --timeout=180s
oc get application portfolio-development -n openshift-gitops \
  -o jsonpath='{.status.sync.status}{" / "}{.status.health.status}{"\n"}'
oc get deployment portfolio -n portfolio-development \
  -o jsonpath='{.spec.template.spec.containers[0].image}{"\n"}'
```

Recorded result: `Synced / Healthy`, the initial `0a74a984…` digest, and a working portfolio at the development HTTPS Route. The application address was `https://portfolio-development.apps.ocp-lab.aymantech.net`; this is a recorded lab endpoint, not a guarantee of ongoing uptime.

## 13. Enable and demonstrate self-healing

Add this beneath `spec` in `argocd/development.yaml`, alongside `source` and `destination`:

```yaml
  syncPolicy:
    automated:
      selfHeal: true
      prune: false
```

Automatic synchronization applies detected Git changes. Self-healing also corrects live configuration drift. Automatic pruning remains disabled. See [Argo CD automated sync documentation](https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/).

```sh
git add argocd/development.yaml
git commit -m "Enable development auto-sync and self-healing"
git push
oc apply -f argocd/development.yaml
```

The manual apply is necessary because this Application watches only `overlays/development`; it does not manage its own definition under `argocd/`. Merely pushing the Application file would not update its live configuration.

In one terminal, watch:

```sh
oc get deployment portfolio -n portfolio-development \
  -w -o custom-columns='NAME:.metadata.name,DESIRED:.spec.replicas,READY:.status.readyReplicas'
```

In another terminal, deliberately introduce drift in the development lab:

```sh
oc scale deployment portfolio -n portfolio-development --replicas=2
```

Do not manually sync or scale back during this experiment. The recorded watch, condensed to the relevant transitions, was:

```text
NAME        DESIRED   READY
portfolio   1         1
portfolio   2         1
portfolio   1         1
```

Argo CD restored the requested replica count to the one declared in Git. The watch did not show two ready replicas and contained no timestamps; it proves drift correction, not a measured recovery time or scaling-performance result. Stop watching with Ctrl+C.

## 14. Release a content change through GitOps

First work in the **application repository**. Edit `content.json` to make a visible change, test it, commit it, and push to `main`. Wait for GitHub Actions to finish publishing. The recorded release used:

```text
Commit: 4f2c57a9aab9c272dd5ccc77b4c6f0608c67a1ed
Tag: quay.io/moabdelbasset/portolio-flask:4f2c57a9aab9c272dd5ccc77b4c6f0608c67a1ed
Digest: quay.io/moabdelbasset/portolio-flask@sha256:85e7a1936b2a3d90cb2b681f0cfa916d9e47458509b7705d92ba6b9a70bf0f26
```

Now switch to the **GitOps repository**. From a clean checkout:

```sh
git switch main
git pull --ff-only
git switch -c release/development-4f2c57a
```

Change only the development overlay's digest:

```yaml
images:
  - name: quay.io/moabdelbasset/portolio-flask
    digest: sha256:85e7a1936b2a3d90cb2b681f0cfa916d9e47458509b7705d92ba6b9a70bf0f26
```

Use the digest from your own CI run for a new release. Leave the base image reference unchanged; the overlay overrides it.

```sh
oc kustomize overlays/development
git diff
git add overlays/development/kustomization.yaml
git commit -m "Deploy portfolio 4f2c57a to development"
git push -u origin release/development-4f2c57a
```

Open a pull request on GitHub from that release branch into `main`, review the digest change, and merge. Argo CD detects the merge; **Refresh** can request another comparison, but automatic synchronization performs deployment. Do not run `oc apply` for this application release.

```sh
oc get deployment portfolio -n portfolio-development \
  -o jsonpath='{.spec.template.spec.containers[0].image}{"\n"}'
oc get application portfolio-development -n openshift-gitops \
  -o jsonpath='{.status.sync.status}{" / "}{.status.health.status}{"\n"}'
```

Expected: the new digest and `Synced / Healthy` after reconciliation. Reload the portfolio and verify the changed content. The user confirmed that the website content changed after this release. No timestamped release measurement was captured.

## Troubleshooting encountered during the milestone

| Symptom | Explanation or resolution |
| --- | --- |
| Argo CD resource types not found | The GitOps operator/CRDs were not installed yet |
| Argo CD server Running but 0/1 Ready | Waited for startup/readiness before trying the interface |
| Access worked only with hosts-file overrides | Switched cluster Cloudflare records from proxied to DNS only |
| No workloads immediately after creating Application | First synchronization was manual; selected Sync in Argo CD |
| Publishing an image did not change the website | Deployment required merging its digest in the GitOps repository |
| Changing Application YAML in Git did not by itself manage the live object | Bootstrap Application definition is outside its watched overlay; apply it explicitly |

For further diagnosis, inspect Argo CD's resource error and the relevant namespace events before changing configuration:

```sh
oc get events -n portfolio-development --sort-by=.metadata.creationTimestamp
oc describe deployment portfolio -n portfolio-development
oc logs deployment/portfolio -n portfolio-development --tail=80
```

## Evidence and remaining milestones

Recorded evidence includes seven application tests in source, the CI workflow and published digest references, cluster/operator version output, the initial healthy Argo CD deployment, the replica drift watch, and confirmation of changed website content after the GitOps release.

Still pending:

- Staging overlay, Application, and promotion of the same image digest.
- Recovery through a Git revert.
- Automated creation of digest-update PRs.
- Timestamped delivery and recovery measurements.

There is no database or persistent storage in this application. Database backup, schema migration, and persistent-data recovery were not part of this milestone.

Useful screenshots to capture for a future update: successful CI run, Argo CD resource tree, the digest PR diff, and the updated portfolio. Screenshots and metrics have not been fabricated or added here.

## Source snapshot

This guide was assembled from the recorded implementation session and local source at these commits:

- [Application release source](https://github.com/moabdelbasset/portolio-flask/tree/4f2c57a9aab9c272dd5ccc77b4c6f0608c67a1ed)
- [GitOps source snapshot](https://github.com/moabdelbasset/portolio-flask-gitops/tree/d5dbad2ac2a0328f6e9d72a9d0ea75a021159d8c)

The milestone stops after the development content release. Later repository changes may extend this configuration.
