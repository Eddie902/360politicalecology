# 360PE — one-time correction and deployment

This package is **source-first**. It contains ALL editable pages, branding graphics, PDF and DOCX publications, and the corrected Quarto and GitHub Actions files. It deliberately **does not contain `_site/`**, which is generated automatically by the GitHub Actions Quarto build. Never copy old `_site` HTML into your repository: this caused your merge conflicts.

## Install (existing GitHub Desktop repository)
1. In GitHub Desktop, select `360politicalecology`. If a merge is in progress, finish or abort it before copying files.
2. Click **Fetch origin** and **Pull origin** first, so your local `main` matches GitHub.
3. Create a backup of your local repository folder before replacing files.
4. Unzip this package, open its `360politicalecology` folder and copy its **contents**, including hidden `.github`, into the repository root. Replace matching source files, retaining your existing `.git` and existing `_site` folders. Do not nest the folder and do not delete `.git`.
5. GitHub Desktop: commit with message `Fix 360PE Quarto config and publishing workflow`; **Push origin**.
6. GitHub website → **Actions** → **Render Quarto website**. Wait for the new render and `Build website HTML` commit. Cloudflare Pages will subsequently deploy the updated `_site` (Cloudflare output folder `_site`, build command `exit 0`).
7. Check the deployed pages, nav logo, publications, source links and PDF downloads before publicity. The planned Issue 01 date is October 13; the live article is an advance online edition dated October 10.

## If another merge conflict appears
Never hand-merge files in `_site`. The automated workflow owns generated output. Resolve conflicts by retaining the generated Quarto version, or abort the merge, synchronize and retry with this *source-only* package. Verify the `.qmd`, `_quarto.yml`, and `styles.css` sources are preserved.

## Editorial caveat
Article fact-checking and checking external links remains a separate editorial task. The PDF publication is preserved, not newly revised to match HTML advance-edition metadata.
