import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
const bankFiles = [
  ['core', 'data/questions-core.json'],
  ['practical', 'data/questions-practical.json'],
  ['extension', 'data/questions-extension.json']
];
const topics = JSON.parse(fs.readFileSync(path.join(root, 'data/topics.json'), 'utf8'));
const references = JSON.parse(fs.readFileSync(path.join(root, 'data/references.json'), 'utf8'));
const topicIds = new Set(topics.map((t) => t.id));
const referenceIds = new Set(references.map((r) => r.id));
const all = [];
const errors = [];
const warnings = [];
const bankCounts = {};
const exactPrompts = new Map();

for (const [expectedBank, relative] of bankFiles) {
  const file = path.join(root, relative);
  let bank;
  try { bank = JSON.parse(fs.readFileSync(file, 'utf8')); }
  catch (error) { errors.push(`${relative}: invalid JSON (${error.message})`); continue; }
  if (!Array.isArray(bank)) { errors.push(`${relative}: root must be an array`); continue; }
  bankCounts[expectedBank] = bank.length;
  for (const [index, q] of bank.entries()) {
    const label = `${relative}[${index}]`;
    if (q.bank !== expectedBank) errors.push(`${label}: bank field must be ${expectedBank}`);
    if (!q.id || typeof q.id !== 'string') errors.push(`${label}: missing stable ID`);
    if (!Number.isInteger(q.number) || q.number < 1) errors.push(`${label}: invalid global question number`);
    if (!topicIds.has(q.topicId)) errors.push(`${label}: unknown topicId ${q.topicId}`);
    if (!referenceIds.has(q.referenceId)) errors.push(`${label}: unknown referenceId ${q.referenceId}`);
    if (!['basic', 'medium', 'hard', 'expert'].includes(q.difficulty)) errors.push(`${label}: invalid difficulty`);
    if (typeof q.question !== 'string' || q.question.trim().length < 15) errors.push(`${label}: question statement is missing or too short`);
    if (!Array.isArray(q.options) || q.options.length !== 4) errors.push(`${label}: single-answer MCQ must have exactly four options`);
    else {
      if (new Set(q.options.map((o) => String(o).trim().toLowerCase())).size !== 4) errors.push(`${label}: answer options are not distinct`);
      if (q.options.some((o) => typeof o !== 'string' || !o.trim())) errors.push(`${label}: an answer option is empty or not a string`);
    }
    if (!Number.isInteger(q.correctAnswer) || q.correctAnswer < 0 || q.correctAnswer > 3) errors.push(`${label}: correctAnswer must be a 0-based index from 0 to 3`);
    if (typeof q.explanation !== 'string' || q.explanation.trim().length < 30) errors.push(`${label}: missing or weak overall explanation`);
    if (!Array.isArray(q.optionExplanations) || q.optionExplanations.length !== 4 || q.optionExplanations.some((x) => typeof x !== 'string' || x.trim().length < 12)) errors.push(`${label}: each option needs an explanation`);
    if (typeof q.hint !== 'string' || q.hint.trim().length < 8) errors.push(`${label}: missing or weak hint`);
    const promptKey = String(q.question || '').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
    if (exactPrompts.has(promptKey)) errors.push(`${label}: exact/normalised prompt duplicate of ${exactPrompts.get(promptKey)}`);
    else exactPrompts.set(promptKey, label);
    all.push(q);
  }
}

const idSet = new Set();
const numberSet = new Set();
for (const q of all) {
  if (idSet.has(q.id)) errors.push(`Duplicate question ID: ${q.id}`);
  idSet.add(q.id);
  if (numberSet.has(q.number)) errors.push(`Duplicate global question number: ${q.number}`);
  numberSet.add(q.number);
}

// Lightweight lexical similarity scan. This flags candidates for human review; it is not semantic proof.
function tokenSet(text) {
  const stop = new Set(['the','and','for','what','which','when','where','does','how','why','with','from','into','using','use','calculate','find','compute','let','is','are','was','were','a','an','of','to','in','on','at','by','be','it','its','that','this','or','as','if','then','has','have','had','must','can','may','will','would','should','do','is','most','best','one','two','all','every','only','their','there','than','what','how']);
  return new Set(String(text).toLowerCase().replace(/[^\p{L}\p{N}]+/gu, ' ').split(/\s+/).filter((t) => (t.length > 2 || /^\d+$/.test(t)) && !stop.has(t)));
}
for (let i = 0; i < all.length; i++) {
  const a = tokenSet(all[i].question);
  for (let j = i + 1; j < all.length; j++) {
    const b = tokenSet(all[j].question);
    const intersection = [...a].filter((t) => b.has(t)).length;
    const union = new Set([...a, ...b]).size;
    const jaccard = union ? intersection / union : 0;
    if (jaccard > 0.72) warnings.push(`High lexical overlap candidate: ${all[i].id} ↔ ${all[j].id} (${jaccard.toFixed(2)})`);
  }
}

const sortedNumbers = all.map((q) => q.number).sort((a, b) => a - b);
for (let i = 0; i < sortedNumbers.length; i++) {
  if (sortedNumbers[i] !== i + 1) errors.push(`Global numbering gap or non-sequential value at position ${i + 1}`);
}

console.log('Question bank validation report');
console.log('--------------------------------');
console.log(`Core syllabus: ${bankCounts.core ?? 0}`);
console.log(`Practical / Maths: ${bankCounts.practical ?? 0}`);
console.log(`Beyond syllabus: ${bankCounts.extension ?? 0}`);
console.log(`Total: ${all.length}`);
console.log(`Topics: ${topics.length}; references: ${references.length}`);
console.log(`Unique IDs: ${idSet.size}; unique global numbers: ${numberSet.size}`);
console.log(`Errors: ${errors.length}; overlap warnings: ${warnings.length}`);
if (warnings.length) {
  console.log('\nOverlap candidates (manual review recommended):');
  for (const warning of warnings) console.log(`- ${warning}`);
}
if (errors.length) {
  console.error('\nValidation errors:');
  for (const error of errors) console.error(`- ${error}`);
  process.exitCode = 1;
} else {
  console.log('\nStructural validation passed. This does not replace a full expert review of every technical explanation or semantic duplicate.');
}
