# Research Roadmap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the supplied high-resolution research roadmap below About me, with a crisp responsive timeline that describes the four research stages shown in the reference image.

**Architecture:** Store the supplied 3840×846 PNG unchanged in the site's image directory. Render the stage labels and publications as semantic HTML beneath the image, then use scoped SCSS to align them to a desktop timeline and stack them into readable cards on narrow screens.

**Tech Stack:** Jekyll, Kramdown, HTML, SCSS, Python unittest/pytest.

## Global Constraints

- Preserve the supplied image bytes and native resolution.
- Place the roadmap immediately after the About me block and before Education.
- Use only the stage and publication copy visible in the supplied reference image.
- Keep all unrelated homepage content unchanged.
- Make the timeline readable on desktop and mobile.

---

### Task 1: Responsive research roadmap

**Files:**
- Create: `images/research-roadmap.png`
- Modify: `_pages/about.md`
- Modify: `assets/css/main.scss`
- Test: `tests/test_research_roadmap.py`

**Interfaces:**
- Consumes: the supplied 3840×846 PNG and the four labels from the annotated reference image.
- Produces: `.research-roadmap`, `.research-roadmap__track`, and four `.research-roadmap__stage` elements rendered beneath About me.

- [ ] **Step 1: Write the failing test**

  Add an integration test that builds the Jekyll site when available and otherwise inspects the source contract. It must verify the roadmap appears between About me and Education, the original image is present at 3840×846, all four stages and six publication labels are present, desktop track styling exists, and the mobile breakpoint stacks the stages.

- [ ] **Step 2: Run the test to verify it fails**

  Run `python -m pytest -q tests/test_research_roadmap.py` and confirm it fails because the roadmap asset and markup do not exist.

- [ ] **Step 3: Add the original asset and minimal implementation**

  Copy the supplied PNG byte-for-byte to `images/research-roadmap.png`. Insert a `<figure class="research-roadmap">` immediately after `</div>` for About me, with one image, one arrow track, and four stage blocks containing the reference labels. Add scoped desktop and mobile SCSS without changing global typography or existing sections.

- [ ] **Step 4: Run verification**

  Run `python -m pytest -q tests/test_research_roadmap.py`, `git diff --check`, and the GitHub Pages build. Confirm the deployed HTML and CSS contain the roadmap selectors after publishing.

- [ ] **Step 5: Commit and publish**

  Commit only the roadmap asset, markup, styles, test, and this plan. Push a feature branch, merge its pull request, and wait for the Pages deployment to complete successfully.

## Self-Review

- The plan covers asset fidelity, placement, copy, desktop alignment, mobile layout, tests, and deployment.
- The production selectors and test expectations use the same documented class contract.
- No locations, papers, dates, captions, or research claims are added beyond the supplied reference.
