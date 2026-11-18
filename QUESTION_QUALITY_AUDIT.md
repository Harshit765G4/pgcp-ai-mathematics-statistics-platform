# Question Quality & Coverage Audit — Updated Release

## 1. Syllabus basis

Primary source: ACTS Pune, *Suggested Teaching Guidelines for Mathematics and Statistics for AI — PGCP-AI August 2026*. The full supplied syllabus was used to organise the topic catalogue.

- **I. Fundamentals of AI:** Sessions 1–15.
- **II. Mathematics for AI — Linear Algebra:** Sessions 1–8.
- **II. Mathematics for AI — Calculus:** Sessions 9–15.

The source does not prescribe a standalone Statistics module. Statistics-adjacent professional material is kept in the supplementary extension bank, not claimed as core syllabus coverage. The syllabus term “Matrix Phylogeny” is retained as supplied.

## 2. Bank counts

| Bank | Current | Target |
|---|---:|---:|
| Core syllabus | 350 | 350 |
| Practical / mathematical applications | 150 | 150 |
| Beyond-syllabus extension | 100 | 100 |
| **Total** | **600** | **600** |

## 3. Coverage by syllabus section

| Section | Questions |
|---|---:|
| Fundamentals of AI | 245 |
| Linear Algebra | 197 |
| Calculus | 158 |
| **Total** | **600** |

All questions map to one of 24 topic IDs and a reusable reference ID.

## 4. Question record fields

Every record includes a permanent ID, global number, bank, topic ID, difficulty, question type, question statement, four options, zero-based correct answer, overall explanation, four option explanations, hint and reference ID. Existing IDs and original global numbers from the earlier 135-question release were preserved; newly added questions receive new IDs and numbers.

## 5. Validation performed

Command: `npm run validate`.

- Core: 350
- Practical: 150
- Extension: 100
- Total: 600
- Topics: 24; references: 24
- Unique IDs: 600
- Unique global question numbers: 600
- Structural errors: 0
- Lexical-overlap warnings: 681

The structural validator checks JSON parsing, required fields, unique IDs and global numbers, four distinct options, valid answer indices, explanations, option-level rationales, hints, topic/reference mappings, exact duplicate prompts and lexical-overlap candidates.

## 6. Important quality limitation

The 681 lexical-overlap warnings are not proof that 681 pairs are semantic duplicates, because the detector is a lightweight token-overlap heuristic. However, the high count means the bank has **not** passed a complete semantic-uniqueness audit. Some newly added items use related concept patterns or parameterised practice cases. Review the flagged pairs and the mathematical calculations before treating this as a final exam-ready question bank. No external subject-matter expert review is claimed.

## 7. Scope notes

- The prior `questions.json` reference files contained Python-programming questions. Their record structure was used as a format reference only; their unrelated questions were not imported.
- The supplied syllabus assignments informed numerical and application question styles; they were not added as separate syllabus chapters.
- The source document title includes Statistics, but the supplied sessions do not define a standalone statistics unit.

## 8. Testing boundaries

Structural JSON validation passed. JavaScript syntax and static HTML/CSS parsing are checked separately. Full manual browser testing across all requested viewport widths and independent expert review of all 600 explanations/options have not been completed.
