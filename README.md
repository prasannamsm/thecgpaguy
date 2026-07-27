# Product Requirement Document (PRD) & Spec Doc — v2

## Product Name: TheCGPAGuy
### Codename / Architecture Reference: Syllabus-Anchored Local AI Learning Platform
### Target Audience: CS Department pattern, MIT MAHE Bengaluru — Phase 1 pilot: single student (personal use)
### Deployment Model: Networked Authoring / Fully Offline Runtime

---

## Changelog since v1

- Product named **TheCGPAGuy**. Note: the name ties the brand to the CGPA grading convention (common at Indian institutions like MAHE) — fine for the current India/MIT-MAHE-style pilot audience, but worth revisiting if Phase 2 distribution ever extends beyond that market.
- Split architecture into two explicit environments: **Authoring** (needs internet) and **Runtime** (fully offline). v1's "Zero Cloud Dependency" language was ambiguous — clarified to mean *no cloud hosting of the app*, not *no API calls ever*.
- UC-101 now assumes the ingested PDF **is** the prescribed textbook (full content), not just a syllabus outline — this is the actual source of "invariant truth" definitions.
- Added UC-101b: Open Content & Media Augmentation — sources supplementary open content and images/GIFs from the internet, staged for **mandatory** admin review before caching (nothing auto-freezes).
- Content generation moved to a cloud-hosted frontier model via API (authoring-time only) to preserve GATE/JEE-Advanced-level rigor; local/free LLMs are reserved for runtime grading, not generation.
- UC-203 grading changed from keyword token-matching to a semantic-equivalence check (local/free LLM) against a structured answer key.
- New Section 5: Distribution & Compliance Roadmap — makes the phased rollout (personal pilot → paid distribution) explicit, and flags IP/licensing review as a blocking checklist item before any payment is collected.
- DB schema extended with content-provenance fields (source, license status) for ingested and sourced media.

---

## 1. Executive Summary & Architecture

### 1.1 Two Environments, Not One

| | Authoring Environment | Runtime Environment |
|---|---|---|
| Who uses it | Admin (you) | Student |
| Network | **Online required** — cloud API calls for generation, web access for open-content/media sourcing | **Fully offline** — no network calls |
| Compute | Cloud-hosted frontier LLM (via API) for generation; local free LLM optional for review assist | Local free LLM (e.g., Ollama / Llama 3 / Mistral) for semantic grading only — no generation at runtime |
| Storage | Staging tables (unreviewed) + local SQLite (frozen/approved) | Local SQLite (read-only for content, read/write for progress) |
| "Zero Cloud" claim | N/A — this environment is expected to be online | True — this environment never calls out |

"No cloud dependency" in this doc now specifically means: **the student-facing app is never deployed to or dependent on a cloud host, and runs with zero network calls once content is frozen locally.** It does not mean the authoring pipeline avoids API calls — it doesn't, by design, to preserve academic rigor.

### 1.2 Academic Complexity Guardrails (unchanged from v1)

- **Primary Standard:** MIT MAHE, Bengaluru CS Department patterns.
- **Secondary Benchmarking:** Falls back to IIT JEE Advanced / GATE CS complexity where MIT-specific patterns aren't defined.

---

## 2. Admin Module Specifications

### UC-101: Curriculum & Reference Ingestion (revised)

- **Actor:** Academic Admin.
- **Input:** The prescribed **textbook itself** (full PDF/text), plus the syllabus document defining unit splits and objectives.
- **System Action:**
  1. Extracts structural metadata (units, topics) from the syllabus.
  2. Extracts and indexes the actual textbook passages relevant to each topic — this becomes the source-of-truth text referenced by generation, not a paraphrase invented from the model's training data.
  3. Every generated definition (UC-102) is generated *grounded in* the retrieved textbook passage, and the passage citation (chapter/page) is stored alongside it for later verification.

### UC-101b: Open Content & Media Augmentation (new)

- **Actor:** Academic Admin.
- **System Action:**
  1. For each concept, searches the web for openly available supplementary material — explainer articles, videos, and candidate images/GIFs illustrating the concept.
  2. Every result is staged with its **source URL and a license tag** (`open` / `needs_review` / `unknown`) — nothing is auto-approved into the local cache.
  3. Admin reviews and approves/rejects each item in the staging workspace (UC-103) before it's written to local storage.

### UC-102: Depth Profile & Complexity Calibration (revised)

- Same configuration panel as v1 (institution profile, academic year, fallback rigor engine, tone).
- **Generation model:** routed via a cloud-hosted frontier model API call (authoring-time only). This is the piece that makes GATE/JEE-Advanced-level rigor realistic — a laptop-local 7–8B model is not a reliable source for correct complexity derivations or high-quality distractors at that difficulty.

### UC-103: Staging Workspace & Multimedia Linker (revised)

- Same review dashboard as v1, now covering three review queues: generated definitions/analogies (against textbook citation), generated assessment items, and sourced open content/media (against license tag).
- **Recommended (not yet mandatory in tooling, but strongly advised operationally):** no content reaches the frozen local cache without a human pass, at least for Section B/C assessment items and any proof-style question, given the grading engine's reliance on semantic checks rather than deterministic verification.

### UC-104: Assessment Blueprint Editor (unchanged from v1)

- Section A (short/definitional), Section B (analytical/derivation), Section C (multi-correct MCQ matrix, 10–30 options, 3–6 correct) — same as v1.

---

## 3. Student Module Specifications

### UC-201: Bootstrapping & Local Cache Retrieval (unchanged)

- Fully offline. Reads from local SQLite. No network calls, ever, in this environment.

### UC-202: Syllabus-Anchored Pedagogical Journey (revised — media type)

- Same 4-step layout (terminology, analogy, media, comparison matrix).
- Multimedia scoped to **images and GIFs** sourced via UC-101b (not heavier video production), reducing the manual content-authoring burden flagged in v1.

### UC-203: Gated Unit Milestones & Descriptive Evaluation (revised — grading method)

- Blocks access to subsequent units until the current unit's evaluation is completed, as in v1.
- **Grading method changed:** descriptive answers (including complexity derivations) are checked via a **semantic-equivalence comparison** run on a local/free LLM, against a structured answer key (required concepts + expected logical steps) — not raw keyword/token matching.
- **Residual risk to flag, not solved by this PRD:** a semantic check can catch missing/wrong concepts more reliably than it can verify that a multi-step mathematical derivation is *actually correct*. For gated (blocking) proof questions, spot-check the grader's accuracy against a small human-graded sample before trusting it to gate progress unsupervised.

### UC-204: "Bucket-Sorting" Multi-Option Evaluation Interface (unchanged)

### UC-205: Complex Multi-Correct Marking Engine (unchanged)

- +4 full / +1 partial (all-correct-only) / 0 unattempted / −2 any incorrect selected — as in v1. Note this is *inspired by* JEE Advanced scoring, not an exact replica of the real (scaled) JEE Advanced rubric — worth stating that explicitly if students will compare it to the real exam.

---

## 4. Local Database Schema Blueprint (extended)

```sql
-- Course Structure Hierarchy Table
CREATE TABLE local_courses (
    course_id TEXT PRIMARY KEY,
    course_code TEXT NOT NULL,
    course_name TEXT NOT NULL,
    target_profile TEXT,
    fallback_rigor TEXT
);

CREATE TABLE syllabus_units (
    unit_id TEXT PRIMARY KEY,
    course_id TEXT,
    unit_number INTEGER NOT NULL,
    unit_title TEXT NOT NULL,
    FOREIGN KEY(course_id) REFERENCES local_courses(course_id)
);

CREATE TABLE core_concepts (
    concept_id TEXT PRIMARY KEY,
    unit_id TEXT,
    concept_title TEXT NOT NULL,
    textbook_definition TEXT NOT NULL,
    textbook_source_ref TEXT,          -- NEW: chapter/page citation from ingested textbook
    simplified_analogy TEXT NOT NULL,
    FOREIGN KEY(unit_id) REFERENCES syllabus_units(unit_id)
);

-- NEW: separates media from concept, tracks provenance/license
CREATE TABLE concept_media (
    media_id TEXT PRIMARY KEY,
    concept_id TEXT,
    media_type TEXT NOT NULL,          -- 'IMAGE' | 'GIF'
    source_url TEXT,                  -- where it was sourced from
    license_status TEXT NOT NULL,      -- 'OPEN' | 'NEEDS_REVIEW' | 'UNKNOWN'
    admin_approved INTEGER NOT NULL,   -- 0/1 — must be 1 before runtime use
    local_path TEXT,
    FOREIGN KEY(concept_id) REFERENCES core_concepts(concept_id)
);

CREATE TABLE assessment_items (
    question_id TEXT PRIMARY KEY,
    unit_id TEXT,
    question_type TEXT NOT NULL,       -- 'SHORT_ANSWER', 'DESCRIPTIVE_PROOF', 'MULTI_CORRECT_MATRIX'
    question_text TEXT NOT NULL,
    textbook_grounding_source TEXT,
    grading_method TEXT NOT NULL,      -- NEW: 'SEMANTIC_LLM_CHECK' | 'STRUCTURED_RUBRIC' | 'MULTI_CORRECT_MATRIX'
    FOREIGN KEY(unit_id) REFERENCES syllabus_units(unit_id)
);

CREATE TABLE matrix_options_pool (
    option_id TEXT PRIMARY KEY,
    question_id TEXT,
    option_text TEXT NOT NULL,
    is_correct_flag INTEGER NOT NULL,
    FOREIGN KEY(question_id) REFERENCES assessment_items(question_id)
);
```

---

## 5. Distribution & Compliance Roadmap (new)

### Phase 1 — Personal Pilot (TheCGPAGuy, internal build)
- Single Windows laptop, single student (personal/family use).
- Textbook ingestion and internet-sourced images/GIFs used under a personal, non-commercial, fair-use assumption.
- No payment collected. No packaging/distribution needed yet.

### Phase 2 — Selected Paid Distribution
- **Blocking checklist before any payment is collected:**
  1. IP/licensing review of textbook-derived content — confirm rights, or restructure generation so it doesn't reproduce/closely paraphrase substantial textbook passages for paying third parties.
  2. License verification for every sourced image/GIF bundled into the paid product (open-licensed or properly cleared — not just "found on the internet").
  3. Packaging mechanism not yet designed: how does an approved course package (SQLite + media bundle) get from your authoring machine to a purchaser's laptop, and how are content updates versioned/delivered afterward?
- None of these are solved by this PRD — they're named here so Phase 2 doesn't start without a decision on them.

---

## 6. Open Risks Carried Forward

- Semantic-check grading is a good improvement over token-matching but isn't a guarantee of mathematical correctness for proof-style answers — spot-check before trusting it to gate progress.
- Rigor depends on the authoring-time model choice (cloud frontier model) — if cost becomes a concern later, that's the lever that will most directly affect content quality, not the runtime local model.
