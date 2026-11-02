# Portfolio content model

- Add a **new project** as `_projects/<slug>.md`, with front matter including `slug`, `order`, `name`, `field`, `summary`, `image`, `image_alt`, `status`, `stack`, and only verified links.
- Add an **external achievement** to `_data/recognitions.yml`. Use a stable `id` and `project` slug, `type` (`publication`, `listing`, `dataset_record`, `collaboration`), `status`, `source`, `title`, `detail`, and source `url`.
- Do **not** invent dates. Add `date: YYYY-MM-DD` only if independently known.
- Add `status: pending` for claims lacking public verification; the template deliberately excludes pending entries. Merely communicating with an institution is **not** a confirmed collaboration.
- Use `type: publication` for published authored pieces, `listing` for a third-party link/directory, `dataset_record` for catalogue records, and `collaboration` **only** for a documented formal collaborative activity.
- Related achievement links are sourced from the same file across the portfolio overview, project case study, archive and milestone article; do not manually duplicate records.
- Add a long-form milestone post in `_posts/YYYY-MM-DD-slug/` with `layout: milestone`, `project_id`, optional `evidence_ids` / `lang` / `alternate_url`, original content and properly licensed screenshots. Data-driven related evidence comes from `_data/recognitions.yml`.
- Do not treat self-submitted directories, pending outreach, correspondence, future appearances or data-use records as editorial endorsement. Public article content should make this distinction explicit.
- Capture images of the owner's own project interfaces or use owned/licensed graphics; do not use generated bird photographs as factual documentation.
