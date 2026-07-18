# Mohamed Ayman — Engineering Blog

Personal portfolio and technical blog for solutions architecture, DevOps, cloud infrastructure, and automation.

The site is built with [Hugo](https://gohugo.io/) and the PaperMod theme, then deployed to GitHub Pages from the `main` branch.

## Local development

1. Clone the repository with its theme submodule:

   ```sh
   git clone --recurse-submodules <repository-url>
   ```

2. Run the development server with the Hugo Extended version pinned in the deployment workflow:

   ```sh
   hugo server --buildDrafts
   ```

3. Open `http://localhost:1313`.

## Content

- Blog articles live in `content/posts/`.
- Project case studies live in `content/projects/`.
- Site-wide design overrides live in `assets/css/extended/custom.css`.
- Generated files in `public/` are intentionally excluded from version control.

## Printable CV

The web CV links to a generated, ATS-readable PDF. Rebuild it after changing the CV content:

```sh
python3 scripts/build-cv-pdf.py
```

Publishing is automatic after changes are merged into `main`.
