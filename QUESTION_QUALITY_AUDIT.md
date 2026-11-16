# Question Quality & Coverage Audit

## 1. Source and coverage basis

Primary source: the five-page ACTS Pune document, **Suggested Teaching Guidelines for Mathematics and Statistics for AI — PGCP-AI August 2026**.

The syllabus material is organised into:

- **I. Fundamentals of AI:** Sessions 1–15.
- **II. Mathematics for AI — Linear Algebra:** Sessions 1–8.
- **II. Mathematics for AI — Calculus:** Sessions 9–15.

The source does not prescribe a standalone Statistics module. Statistics/probability-related questions, where present, are classified as supplementary in the extension bank rather than represented as required syllabus coverage.

Assignments in the source were used to infer suitable numerical/application question styles. They were not converted into extra topic units.

## 2. Current bank counts

| Bank | Current | Target | Gap |
|---|---:|---:|---:|
| Core syllabus | 69 | 350 | 281 |
| Practical / mathematics applications | 46 | 150 | 104 |
| Beyond-syllabus extension | 20 | 100 | 80 |
| **Total** | **135** | **600** | **465** |

The source prompt has conflicting counts in its bank headings and detailed requirements: the headings say 300 core and 100 practical, while the detailed requirements specify 350 core and 150 practical. This release adopts the detailed requirement (350 + 150 + 100 = 600).

**Status:** This is a curated first bank, not a claim that the 600-question target is complete. The implementation deliberately avoids bulk-generated filler questions.

## 3. Question record completeness

Each current question includes:

- Stable unique ID and global question number.
- Bank, topic ID, difficulty, and question type.
- A question statement and four answer options.
- One zero-based correct-answer index.
- A learning-oriented overall explanation.
- An explanation/rationale for each of the four options.
- A non-answer-revealing hint.
- A topic reference ID.

Difficulty labels use Basic, Medium, Hard, and Expert. The label is intended to represent the cognitive work involved, not simply to balance category counts.

## 4. Structural validation performed

Command run: `npm run validate`.

Latest result:

```text
Core syllabus: 69
Practical / Maths: 46
Beyond syllabus: 20
Total: 135
Topics: 24; references: 24
Unique IDs: 135; unique global numbers: 135
Errors: 0; overlap warnings: 4
Structural validation passed.
```

The validator checks:

- Valid JSON in all three question banks.
- Required record fields and expected bank identity.
- Globally unique question IDs and numbers.
- Four non-empty, distinct answer options.
- A valid answer index (0–3).
- Overall and option-level explanations.
- A hint for every question.
- Valid topic and reference mappings.
- Exact duplicate prompts.
- High lexical-overlap candidates for manual review.

## 5. Similarity warnings reviewed

The validator reported four high lexical-overlap pairs. They were manually inspected and use similar numeric/matrix notation, but the intended tasks are different:

- `PRACTICAL-002`: vector dot product.
- `PRACTICAL-010`: matrix transpose.
- `PRACTICAL-030`: matrix determinant.
- `PRACTICAL-003`: vector projection.
- `PRACTICAL-031`: diagonal matrix inverse.

The pairs are lexical false positives around short mathematical expressions and repeated numeric tokens. The heuristic cannot guarantee semantic uniqueness, so future additions still require manual comparison at the learning-objective level.

## 6. Content-specific notes

- The course title includes Statistics, but no standalone statistics sessions appear in the supplied five-page teaching guideline. Related statistical content is marked as extension rather than core.
- “Matrix Phylogeny” is preserved as a syllabus topic and has a dedicated reference.
- The syllabus uses terms such as “Turing Machine”, “Turing Test”, “Matrix Approximation”, “Singular Value Decomposition”, “Lagrange Multipliers”, and “Saddle Point”; these remain in the topic/reference structure.

## 7. Review boundaries and limitations

- Structural validation passed for the current records.
- Structural validation does not establish that every distractor is equally plausible or that every technical explanation is independently peer-reviewed.
- No external subject-matter expert review is claimed.
- The question bank is below its requested target by 465 questions. Additions should be developed topic-by-topic and validated before release.
- No automated test is claimed for all seven viewport sizes or every interaction. The interface contains responsive layout rules; the project README provides local run and validation steps for further browser QA.
