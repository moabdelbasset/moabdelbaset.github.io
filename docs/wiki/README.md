# Home-lab wiki publication

`GitOps-Application-Delivery-on-OpenShift.md` is the canonical wiki draft. It covers the development milestone recorded through September 11, 2026.

To publish manually, open the home-lab GitHub wiki, create a page titled **GitOps Application Delivery on OpenShift**, select Markdown, and paste the guide contents. The guide has no Hugo front matter.

The same file is copied to `static/guides/` so the portfolio case study can offer a download before the wiki page is published. After edits, keep that copy synchronized:

```sh
cp docs/wiki/GitOps-Application-Delivery-on-OpenShift.md static/guides/GitOps-Application-Delivery-on-OpenShift.md
```

Once the wiki page is published, its URL can be added to the case study. No uncreated wiki URL is linked from the site.
