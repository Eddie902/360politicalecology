# 360 Political Ecology Website

Official research-informed publishing website project for 360politicalecology.org.

## Content
- Quarto source: `*.qmd`, `_quarto.yml`, `styles.css`
- Publication: `articles/africa-battery-minerals/`
- Prebuilt website: `_site/` (can be deployed directly via Cloudflare Pages)

## GitHub / Cloudflare Pages
Upload the *contents* of this folder to the GitHub repository root (`Eddie902/360politicalecology`).
Cloudflare Pages: choose the repository, production branch `main`, framework preset `None`, build command `exit 0`, and output directory `_site`.

The prebuilt `_site/` is included for the first deployment. For future edits, the GitHub Actions workflow renders Quarto and commits changes into `_site/`; verify the workflow has repository write permission (Settings → Actions → General → Workflow permissions → Read and write permissions) if the commit step fails.

Alternatively run `quarto render` locally, then commit both source and `_site/` files. The `.tex` pdfLaTeX workflow for articles remains independent.

**Publication note:** Issue 01 is scheduled for 13 October 2026. Complete final source verification before public release; this repository contains working publication material.
