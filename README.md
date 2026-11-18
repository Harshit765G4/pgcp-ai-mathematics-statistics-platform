# PGCP-AI Mathematics and Statistics for AI — Learning & MCQ Practice Platform

A responsive, static web application for studying and practising the **Mathematics and Statistics for AI** subject in the PGCP-AI August 2026 programme. The uploaded ACTS Pune teaching-guidelines syllabus is the source of the syllabus map and core question coverage.

## Current content status

| Bank | Current questions | Target |
|---|---:|---:|
| Core syllabus | 350 | 350 |
| Practical / mathematics applications | 150 | 150 |
| Beyond-syllabus extension | 100 | 100 |
| **Total** | **600** | **600** |

The 600-question set covers the syllabus sections and sub-sections. Current distribution:

| Syllabus section | Questions |
|---|---:|
| Fundamentals of AI | 245 |
| Linear Algebra | 197 |
| Calculus | 158 |
| **Total** | **600** |

The supplied prior `questions.json` reference was used to understand the record shape (stable ID, bank, topic, difficulty, question, four options, answer index, explanation, hint, reference and number). Its earlier Python-programming questions were not copied into this subject bank. The current application retains its richer schema, including per-option explanations and stable bank-specific IDs.

**Content-quality qualification:** structural validation passes, but the lexical-overlap heuristic flags 681 pairs for manual review. Some are related learning objectives and some may be overly similar; this is not a certified semantic-uniqueness audit. The generated bank is a substantial practice release, not an expert-peer-reviewed examination paper. Review flagged pairs and technical explanations before relying on every item for a high-stakes exam.

## Features

- Three independently filterable banks: core syllabus, practical/mathematical applications, and supplementary beyond-syllabus material.
- Topic, bank, difficulty, status, and keyword filters; all, topic, random, incorrect, flagged, unanswered, and timed mock practice modes.
- Four-option MCQs with one best answer, answer key, explanation, per-option rationales, hint, topic mapping, reference mapping, difficulty, and stable ID.
- Circular question navigator: neutral for unchecked, green for correct, red for incorrect, active outline, and a separate flag marker.
- Answer checking only after selection; answer reveal after checking; retry and reset controls.
- Reusable topic study references with definitions, key concepts, examples, common mistakes, and examination notes.
- Light, dark, and system themes; preference is persisted.
- Desktop three-column workspace and responsive mobile navigator/learning drawers.
- Progress persistence per candidate profile using browser localStorage.
- JSON progress export/import with schema and question-ID checks and an overwrite confirmation.
- Timer with timestamp-based countdown, pause/resume/reset, and a 60-minute mock-exam mode.
- Focus mode, performance analytics, keyboard shortcuts, and next-unanswered navigation.
- Question-bank validation script and data templates.

## Project structure

```text
math-statistics-ai-platform/
├── index.html
├── package.json
├── vercel.json
├── README.md
├── QUESTION_QUALITY_AUDIT.md
├── data/
│   ├── topics.json
│   ├── references.json
│   ├── questions-core.json
│   ├── questions-practical.json
│   ├── questions-extension.json
│   └── templates/
│       ├── question.template.json
│       ├── topic.template.json
│       └── reference.template.json
├── src/
│   ├── app.js
│   └── styles.css
└── scripts/
    ├── build_questions.py
    ├── expand_question_banks.py
    └── validate-questions.mjs
```

## Run locally

No frontend build step or dependency installation is required. The application loads its JSON data using `fetch`, so serve the project over HTTP rather than opening `index.html` directly from the file system.

### Option 1: Python

```bash
cd math-statistics-ai-platform
python -m http.server 4173
```

Open `http://localhost:4173`.

### Option 2: npm script

```bash
npm run serve
```

Then open `http://localhost:4173`.

## Validate the question banks

Node.js 18+ is recommended. Run:

```bash
npm run validate
```

The validator checks JSON parsing, required fields, unique question IDs, unique global question numbers, exactly four distinct options, valid answer indexes, explanations, per-option rationales, hints, topic/reference mappings, exact duplicate prompts, and high lexical-overlap candidates.

The initial curated set can be regenerated with `npm run build:questions` (Python 3 required). To expand banks that are below their targets, run `npm run expand:questions`. Do not run the initial build script over an expanded bank because it recreates the initial curated set. Review generated content and rerun validation before committing it.

The overlap detector is a heuristic, not a semantic AI model. The current audit reports 681 lexical-overlap candidates; manually inspect these before treating the bank as final exam material.

## Add questions

1. Choose the appropriate bank file:
   - `data/questions-core.json`
   - `data/questions-practical.json`
   - `data/questions-extension.json`
2. Copy `data/templates/question.template.json` and fill every field.
3. Assign a permanent unique ID using the relevant prefix (`CORE-`, `PRACTICAL-`, or `EXT-`). Never recycle or change a published ID.
4. Assign a global `number` that is not used anywhere else in any bank. Existing numbers should not be renumbered.
5. Use an existing `topicId` from `data/topics.json`, and a valid `referenceId` from `data/references.json`.
6. Keep `correctAnswer` zero-based: `0` = option A, `1` = B, `2` = C, `3` = D.
7. Write four plausible options and an explanation for each option. Include a hint that guides without giving away the answer.
8. Run `npm run validate` and manually inspect new content and any overlap warnings.

Question type values such as `concept`, `numerical`, `scenario`, `calculation`, and `supplement` are descriptive labels; the data loader does not hardcode a fixed enum.

## Add topics and study references

- Add a topic using `data/templates/topic.template.json` to `data/topics.json`.
- Add a corresponding study reference using `data/templates/reference.template.json` to `data/references.json`.
- The reference `topicId` should match the topic ID. Every question must map to an existing topic and a reference ID.
- Keep references reusable: one topic reference may support many questions.

## Deploy to Vercel

This is a static site. The repository root is the deployment root.

1. Push the complete project folder to a Git repository.
2. Import the repository into Vercel.
3. Set the project root to the folder containing `index.html`.
4. No build command is required.
5. Set the output directory to `.` (project root) if Vercel asks for one.
6. Deploy. Confirm the deployed site loads question JSON from the `data/` directory.

`vercel.json` is included with clean URL settings. The app is deployable as a static site; it does not require a server API.

## Persistence and privacy notes

- Candidate progress is stored in the current browser's localStorage, separated by a normalised candidate name.
- Theme preference is stored locally.
- Local browser storage does **not** sync across browsers or devices. Export a JSON backup and import it elsewhere to transfer progress.
- No account, backend, or cloud sync is included in this static release. A future Supabase/Firebase sync layer can be added behind the existing progress service boundary.

## Keyboard shortcuts

- `1`–`4`: select answer option A–D.
- `←` / `→`: previous / next question.
- `H`: reveal hint.
- `F`: flag or unflag the current question.
- `Esc`: close an active overlay or mobile drawer.

## Source coverage notes

- The syllabus explicitly provides Fundamentals of AI (Sessions 1–15), Linear Algebra (Sessions 1–8), and Calculus (Sessions 9–15).
- Although the subject title includes “Statistics”, the uploaded teaching-guidelines pages do not specify a separate Statistics module. Statistics/probability-related material is therefore labelled as beyond-syllabus/supplementary where included.
- The supplied mathematical assignments inform numerical practice styles; they are not treated as extra syllabus chapters.
- The phrase “Matrix Phylogeny” is retained from the syllabus and has its own reference section.

## Known limitations

- The initial question-bank size is 135, below the prompt's 600-question target. The app and data architecture support incremental expansion.
- Automated validation cannot prove the correctness of every mathematical explanation or detect all semantic duplicates. The audit report distinguishes structural checks from manual review.
- Responsive breakpoints and layout rules are implemented, but a full cross-device/manual browser QA pass remains a separate verification task if not described as completed in the audit report.
