# Antigravity AI IDE Standard Operating Procedures

This document enforces the Antigravity Strict Mode rules for AI-assisted development. All agents and developers must adhere to these conventions.

## 1. Aesthetic Guidelines
- **UI Quality:** All generated UI code (especially SvelteKit/Tailwind) MUST use premium design aesthetics.
- **Color Palettes:** Avoid plain CSS colors (red, blue, green). Utilize curated HSL palettes, glassmorphism UI elements, and sleek dark modes.
- **Interactivity:** Every UI component must include hover states and micro-animations to feel dynamic and responsive.

## 2. Commit and Documentation Standards (Antigravity Sync)
- **Commits:** All VCS commits must follow Conventional Commits standard (e.g., `feat:`, `fix:`, `docs:`, `refactor:`).
- **Documentation Sync:** Upon the completion of any feature, the agent MUST summarize the logic in 3-5 technical points and generate an *Update Snippet* to append to `Technical Specification Document.md`.

## 3. Tool Prioritization and execution
- **File Modifications:** Prefer native IDE filesystem tools (`replace_file_content`, `write_to_file`) over bash shell script equivalents (`sed`, `cat >>`).
- **No Side Effects:** Agents must never touch unrelated modules when fixing a scoped bug. Folder `/legacy` is off-limits.

## 4. Testing Requirements
- Every new feature or bug fix must state the testing methodology employed (Jest unit testing, Playwright E2E, or manual verification steps).
