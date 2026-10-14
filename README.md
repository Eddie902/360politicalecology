# 360PE Website V2 — Quarto + GitHub + Cloudflare Pages

The **original official masthead is used as an image** in `_quarto.yml` (`navbar.logo`), not rebuilt as website header text. The logo mark is included as a favicon asset; replace it with a cropped square export for optimal favicon visibility if needed.

## Safe migration (important)

1. **Back up your existing GitHub repository** or create a branch `website-v2` before making any changes.
2. Copy the new files into the repository. **Keep your existing full-text** `articles/africa-battery-minerals/index.qmd` if it is more complete than the summary version in this package. The package includes the complete article PDF as a stable download.
3. Retain any other existing articles or datasets not included in this package.
4. Replace the old workflow that commits generated `_site` files to `main` with `.github/workflows/validate.yml`, to avoid generated-output merge conflicts. Do not run both conflicting workflows.
5. In Cloudflare: **Workers & Pages → your Pages project → Settings → Builds & deployments**. Set Git provider to GitHub and select `main`; production branch `main`. **Build command**: `quarto render`. **Build output directory**: `_site`. Some Cloudflare Pages environments do not include Quarto by default, so configure the build using the installation procedure below or a compatible build image. Do not enter an arbitrary framework preset.
6. Cloudflare Git build environments may not have Quarto installed. Recommended robust Cloudflare build command:

   ```bash
   bash scripts/cloudflare-build.sh
   ```

   Build output directory: `_site` ; root directory: repo root. The script installs a pinned Linux AMD64 Quarto release if Quarto is missing. Cloudflare must provide a compatible Linux amd64 build environment, curl and tar. For other architectures revise the release URL.
7. Verify custom domain `360politicalecology.org` is assigned and active. Preserve current DNS records; do not recreate the domain or remove existing Search Console verification TXT records.
8. Use Google Search Console to inspect article canonical/indexability, then submit `https://360politicalecology.org/sitemap.xml` (if it is not already submitted). A valid sitemap/indexing request is not a guarantee of indexing.
9. **Do not publish** `contact@360politicalecology.org` as a working email until its forwarding/inbox has been configured and a test email succeeds.

## Local testing

Install Quarto from https://quarto.org/docs/get-started/ and run:

```bash
quarto render
quarto preview
```

This release is built from standalone `.qmd` files, CSS, images and PDF assets; it does not require an R or Python execution kernel.

## Optional: recommended simpler deployment pattern

If you prefer **GitHub Actions builds + Cloudflare Pages Direct Upload**, configure Cloudflare API token and project ID as GitHub secrets instead of enabling Git builds. Do *not* run both deployment strategies in parallel. The included default workflow validates the site but leaves deployment to Cloudflare Git integration.

## Where to customize

- `_quarto.yml`: navbar, footer, publishing metadata
- `styles.css`: visual identity and responsive sizing
- `founder.qmd`: approved biography and external professional URLs
- `contact.qmd`: add a verified email address after setup
- `articles/.../index.qmd`: retain the existing **complete article text** if already present
- `publications.qmd`: generated publication listing/RSS
- `topics.qmd`: exact ten areas of analysis

## Page-level accessibility

All pages have textual headings for screen readers and search engines, but the visual masthead is **only an image**, never duplicated as an invented text logo.
