# 360PE V3 — PR 5 Knowledge Navigation

## Scope
- Twelve topic landing pages aligned with the controlled V3 taxonomy in `_data/topics.yml`.
- A grouped topic directory on the existing `topics.qmd` page.
- Original ten-area descriptions and infographic preserved on the same page.
- Accessible Topics dropdown with direct links to all twelve pages.
- Publication discovery links on the homepage and `publications.qmd`.
- Additive responsive styles and GitHub Actions checks for twelve rendered topic pages.

## Classification and editorial integrity
The inaugural advance-online article has primary topic MIN and secondary topics ENE, GOV, JUS. Only those four topic pages link to the existing article as classified related analysis. The remaining eight topic pages explicitly say that there are currently no classified publications. No fabricated articles, datasets, videos, or claims of peer review.

## Technical notes
Quarto `project.render` includes `topics/**/*.qmd`. Each topic is a stable `topics/<slug>/index.qmd` source rendered to `topics/<slug>/index.html`. All topic pages link to existing root-level `topics.qmd`, `publications.qmd`, `research.qmd`, and `editorial-standards.qmd` via relative Quarto links. No old URL has been changed.

## Current scope boundary
This PR provides accurate manual classification links for the existing single publication. Automated topic-specific listings and a publication-to-topic generator are deferred until there are more articles; topic pages must be updated or generated when new articles are added. No social publishing, new Media page, DNS, Cloudflare production configuration, or article body edits.

## Review checklist
1. GitHub Actions metadata and Quarto checks pass.
2. All twelve topic pages render and internal links work.
3. Mobile Topics dropdown and two-column topic directory are visually reviewed.
4. Historical ten-area infographic and original article URL remain unchanged.
5. Review Cloudflare branch preview, if available, before authorizing merge.

**Do not merge or deploy to production without explicit approval.**
