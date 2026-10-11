# Updating 360PE in one operation

1. Extract the ZIP. Open `360politicalecology/` and copy **its contents** (not the parent folder) into the local GitHub Desktop clone of `Eddie902/360politicalecology`.
2. Merge folders and replace matching website files. Do not replace newer local research work without backing it up.
3. In GitHub Desktop, review Changes, commit `Update 360PE branding, article sources and layout`, then Push origin.
4. GitHub Actions (`.github/workflows/build-site.yml`) should render Quarto and push updated `_site` outputs. Check GitHub Actions for a green check. Cloudflare Pages then deploys `_site` from branch `main` using build command `exit 0`.
5. Verify homepage, logo, article source links, PDFs and mobile table overflow at your `.pages.dev` address. Refresh cache if you see old assets.

**Publishing caution:** The currently included article is public as an *advance online edition*; it still needs final factual/source checks. If you do not want it publicly accessible before the formal issue date, remove it and its public links from the deployable build before deployment.

**Source of truth:** Edit `.qmd`, `_quarto.yml` and `styles.css`; GitHub Actions regenerates `_site`. The bundled `_site` is an initial preview and may be superseded by the next build.
