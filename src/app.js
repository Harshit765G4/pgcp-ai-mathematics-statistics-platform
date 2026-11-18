const DATA_FILES = [
  './data/questions-core.json',
  './data/questions-practical.json',
  './data/questions-extension.json'
];
const LETTERS = ['A', 'B', 'C', 'D'];
const PROFILE_PREFIX = 'pgcpai-math-ai-profile:';
const THEME_KEY = 'pgcpai-math-ai-theme';
const ACTIVE_PROFILE_KEY = 'pgcpai-math-ai-active-profile';
const $ = (id) => document.getElementById(id);

let questions = [];
let topics = [];
let references = [];
let questionById = new Map();
let topicById = new Map();
let referenceById = new Map();
let visibleQuestions = [];
let currentQuestionId = null;
let progress = null;
let profileName = 'Learner';
let activeLearningTab = 'hint';
let randomOrder = [];
let timerInterval = null;
let lastTimerSecond = -1;
let activeOverlay = null;
let mobileDrawer = null;
let toastTimer = null;

function defaultProgress(name) {
  return {
    schemaVersion: 1,
    candidateName: name,
    answers: {},
    flags: [],
    hints: [],
    timer: { durationSec: 1800, remainingSec: 1800, deadline: null, running: false, completed: false },
    session: { createdAt: Date.now(), lastActiveAt: Date.now(), checkedCount: 0 },
    themePreference: localStorage.getItem(THEME_KEY) || 'system'
  };
}

function profileKey(name) {
  const slug = String(name || 'Learner').trim().toLowerCase().replace(/[^a-z0-9_-]+/g, '-').replace(/^-|-$/g, '') || 'learner';
  return PROFILE_PREFIX + slug;
}

function loadProfile(name) {
  profileName = String(name || 'Learner').trim().slice(0, 40) || 'Learner';
  const raw = localStorage.getItem(profileKey(profileName));
  if (!raw) return defaultProgress(profileName);
  try {
    const parsed = JSON.parse(raw);
    if (parsed?.schemaVersion !== 1 || typeof parsed.answers !== 'object' || !Array.isArray(parsed.flags) || !Array.isArray(parsed.hints)) {
      return defaultProgress(profileName);
    }
    return {
      ...defaultProgress(profileName),
      ...parsed,
      candidateName: profileName,
      answers: parsed.answers || {},
      flags: parsed.flags || [],
      hints: parsed.hints || [],
      timer: { ...defaultProgress(profileName).timer, ...(parsed.timer || {}) }
    };
  } catch {
    return defaultProgress(profileName);
  }
}

function saveProgress() {
  if (!progress) return;
  progress.candidateName = profileName;
  progress.session.lastActiveAt = Date.now();
  try {
    localStorage.setItem(profileKey(profileName), JSON.stringify(progress));
    localStorage.setItem(ACTIVE_PROFILE_KEY, profileName);
    $('saveStatus').textContent = `Saved locally · ${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
  } catch (error) {
    $('saveStatus').textContent = 'Could not save · browser storage may be full';
    console.error('Progress save failed', error);
  }
}

function escapeHTML(value) {
  return String(value ?? '').replace(/[&<>"']/g, (char) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  })[char]);
}

function showToast(message) {
  const region = $('toastRegion');
  region.innerHTML = '';
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.textContent = message;
  region.appendChild(toast);
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { toast.remove(); }, 2600);
}

function setTheme(preference, persist = true) {
  const value = ['light', 'dark', 'system'].includes(preference) ? preference : 'system';
  const resolved = value === 'system'
    ? (window.matchMedia?.('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
    : value;
  document.documentElement.dataset.theme = resolved;
  $('themeSelect').value = value;
  if (persist) {
    localStorage.setItem(THEME_KEY, value);
    if (progress) {
      progress.themePreference = value;
      saveProgress();
    }
  }
}

function topicName(topicId) {
  return topicById.get(topicId)?.name || 'General';
}

function currentQuestion() {
  return questionById.get(currentQuestionId) || null;
}

function questionState(questionId) {
  return progress.answers[questionId] || { selected: null, checked: false, correct: null, attempts: 0 };
}

function isFlagged(questionId) {
  return progress.flags.includes(questionId);
}

function isHintRevealed(questionId) {
  return progress.hints.includes(questionId);
}

function checkedAnswerEntries() {
  return Object.entries(progress.answers).filter(([id, item]) => questionById.has(id) && item?.checked);
}

function profileStats() {
  const entries = checkedAnswerEntries();
  const correct = entries.filter(([, item]) => item.correct).length;
  const incorrect = entries.length - correct;
  const attempted = entries.length;
  return {
    total: questions.length,
    attempted,
    correct,
    incorrect,
    remaining: Math.max(0, questions.length - attempted),
    accuracy: attempted ? Math.round((correct / attempted) * 100) : null,
    completion: questions.length ? Math.round((attempted / questions.length) * 100) : 0
  };
}

function activeFilterConfig() {
  return {
    mode: $('modeSelect').value,
    subject: $('subjectSelect').value,
    bank: $('bankSelect').value,
    topic: $('topicSelect').value,
    difficulty: $('difficultySelect').value,
    status: $('statusSelect').value,
    search: $('searchInput').value.trim().toLowerCase()
  };
}

function shuffleArray(items) {
  const copy = [...items];
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

function getVisibleQuestions() {
  const f = activeFilterConfig();
  let result = questions.filter((q) => {
    const section = topicById.get(q.topicId)?.section || '';
    if (f.subject !== 'all' && section !== f.subject) return false;
    if (f.bank !== 'all' && q.bank !== f.bank) return false;
    if (f.topic !== 'all' && q.topicId !== f.topic) return false;
    if (f.difficulty !== 'all' && q.difficulty !== f.difficulty) return false;
    const state = questionState(q.id);
    const flagged = isFlagged(q.id);
    const wrong = state.checked && !state.correct;
    const unanswered = !state.checked;
    if (f.mode === 'incorrect' && !wrong) return false;
    if (f.mode === 'flagged' && !flagged) return false;
    if (f.mode === 'unanswered' && !unanswered) return false;
    if (f.status === 'incorrect' && !wrong) return false;
    if (f.status === 'unanswered' && !unanswered) return false;
    if (f.status === 'flagged' && !flagged) return false;
    if (f.search) {
      const haystack = [q.question, ...q.options, topicName(q.topicId), q.id, q.bank].join(' ').toLowerCase();
      if (!haystack.includes(f.search)) return false;
    }
    return true;
  });
  if (f.mode === 'random' || f.mode === 'mock') {
    const rank = new Map(randomOrder.map((id, index) => [id, index]));
    result.sort((a, b) => (rank.get(a.id) ?? Number.MAX_SAFE_INTEGER) - (rank.get(b.id) ?? Number.MAX_SAFE_INTEGER));
  } else {
    result.sort((a, b) => a.number - b.number);
  }
  return result;
}

function refreshVisibleQuestions(keepCurrent = true) {
  const oldId = currentQuestionId;
  visibleQuestions = getVisibleQuestions();
  if (keepCurrent && visibleQuestions.some((q) => q.id === oldId)) {
    currentQuestionId = oldId;
  } else {
    currentQuestionId = visibleQuestions[0]?.id || null;
  }
  renderAll();
}

function renderStats() {
  const stats = profileStats();
  $('statTotal').textContent = stats.total;
  $('statAttempted').textContent = stats.attempted;
  $('statAttemptedFoot').textContent = `${stats.completion}% completed`;
  $('statCorrect').textContent = stats.correct;
  $('statAccuracy').textContent = stats.accuracy === null ? '—' : `${stats.accuracy}%`;
  $('statProgress').textContent = `${stats.completion}%`;
  $('progressBar').style.width = `${stats.completion}%`;
  $('statRemaining').textContent = `${stats.remaining} questions remaining`;
  $('navigatorAttempted').textContent = `${stats.attempted} attempted`;
  $('navigatorFlagged').textContent = `${progress.flags.length} flagged`;
}

function renderBankSummary() {
  const summary = ['core', 'practical', 'extension'].map((bank) => {
    const bankQuestions = questions.filter((q) => q.bank === bank);
    const checked = bankQuestions.filter((q) => questionState(q.id).checked).length;
    const name = bank === 'core' ? 'Core syllabus' : bank === 'practical' ? 'Practical / Maths' : 'Beyond syllabus';
    return `<div class="bank-chip"><span>${name}</span><strong>${checked}/${bankQuestions.length} checked</strong></div>`;
  }).join('');
  $('bankSummary').innerHTML = summary;
}

function renderNavigator() {
  $('visibleCount').textContent = visibleQuestions.length;
  const grid = $('questionGrid');
  grid.innerHTML = '';
  visibleQuestions.forEach((q) => {
    const state = questionState(q.id);
    const dot = document.createElement('button');
    dot.type = 'button';
    dot.className = 'question-dot';
    if (q.id === currentQuestionId) dot.classList.add('active');
    if (state.checked) dot.classList.add(state.correct ? 'correct' : 'incorrect');
    if (state.selected !== null && !state.checked) dot.classList.add('selected');
    if (isFlagged(q.id)) dot.classList.add('flagged');
    dot.textContent = q.number;
    dot.title = `${q.id} · ${topicName(q.topicId)}${state.checked ? state.correct ? ' · Correct' : ' · Incorrect' : ' · Not checked'}${isFlagged(q.id) ? ' · Flagged' : ''}`;
    dot.setAttribute('aria-label', dot.title);
    dot.addEventListener('click', () => navigateTo(q.id));
    grid.appendChild(dot);
  });
  renderBankSummary();
}

function renderEmptyState() {
  const hasQuestion = Boolean(currentQuestion());
  $('questionCard').hidden = !hasQuestion;
  $('emptyState').hidden = hasQuestion;
  if (!hasQuestion) {
    $('visibleCount').textContent = '0';
  }
}

function renderOptions(q, state) {
  const container = $('answerOptions');
  container.innerHTML = '';
  q.options.forEach((option, index) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'option-button';
    button.setAttribute('role', 'radio');
    button.setAttribute('aria-checked', String(state.selected === index));
    button.disabled = state.checked;
    if (state.selected === index) button.classList.add('selected');
    if (state.checked && index === q.correctAnswer) button.classList.add('correct-option');
    if (state.checked && state.selected === index && !state.correct) button.classList.add('wrong-option');
    const letter = document.createElement('span');
    letter.className = 'option-letter';
    letter.textContent = LETTERS[index];
    const content = document.createElement('span');
    content.className = 'option-content';
    content.textContent = option;
    button.append(letter, content);
    if (state.checked && index === q.correctAnswer) {
      const status = document.createElement('span');
      status.className = 'option-state';
      status.textContent = '✓';
      button.appendChild(status);
    } else if (state.checked && index === state.selected && !state.correct) {
      const status = document.createElement('span');
      status.className = 'option-state';
      status.textContent = '×';
      button.appendChild(status);
    }
    button.addEventListener('click', () => selectAnswer(q.id, index));
    container.appendChild(button);
  });
  $('selectedLabel').textContent = state.selected === null ? 'No option selected' : `Option ${LETTERS[state.selected]} selected`;
}

function renderFeedback(q, state) {
  const feedback = $('answerFeedback');
  if (!state.checked) {
    feedback.hidden = true;
    feedback.innerHTML = '';
    feedback.className = 'answer-feedback';
    return;
  }
  feedback.hidden = false;
  feedback.className = `answer-feedback ${state.correct ? 'correct-feedback' : 'wrong-feedback'}`;
  const selectedRationale = q.optionExplanations?.[state.selected] || '';
  feedback.innerHTML = `
    <div class="feedback-title">${state.correct ? '✓ Correct answer' : '× Not quite — review the reasoning'}</div>
    <div class="feedback-explanation">${escapeHTML(q.explanation)}</div>
    ${!state.correct ? `<div class="feedback-selected"><strong>Your choice (${LETTERS[state.selected]}):</strong> ${escapeHTML(selectedRationale)}<br><strong>Correct answer:</strong> ${LETTERS[q.correctAnswer]} — ${escapeHTML(q.options[q.correctAnswer])}</div>` : ''}
  `;
}

function renderQuestion() {
  renderEmptyState();
  const q = currentQuestion();
  if (!q) return;
  const state = questionState(q.id);
  $('questionNumber').textContent = `QUESTION ${String(q.number).padStart(3, '0')}`;
  $('questionTopic').textContent = topicName(q.topicId);
  $('questionBank').textContent = q.bank === 'core' ? 'Core syllabus' : q.bank === 'practical' ? 'Practical / Maths' : 'Beyond syllabus';
  $('questionDifficulty').textContent = q.difficulty[0].toUpperCase() + q.difficulty.slice(1);
  $('questionDifficulty').className = `difficulty-badge ${q.difficulty}`;
  $('questionStem').textContent = q.question;
  const position = visibleQuestions.findIndex((item) => item.id === q.id) + 1;
  $('questionPosition').textContent = `${position} of ${visibleQuestions.length}`;
  $('questionProgressBar').style.width = `${visibleQuestions.length ? position / visibleQuestions.length * 100 : 0}%`;
  renderOptions(q, state);
  renderFeedback(q, state);
  $('previousButton').disabled = position <= 1;
  $('nextButton').disabled = position >= visibleQuestions.length;
  $('checkButton').disabled = state.selected === null && !state.checked;
  $('checkButton').textContent = state.checked ? 'Try again' : 'Check answer';
  $('flagButton').textContent = isFlagged(q.id) ? '⚑ Flagged · Remove' : '⚑ Flag for review';
  $('flagButton').classList.toggle('flag-active', isFlagged(q.id));
  $('hintButton').textContent = isHintRevealed(q.id) ? '✦ Hint revealed' : '✦ Reveal hint';
  renderLearningContent();
}

function renderHint(q) {
  if (!isHintRevealed(q.id)) {
    return `<div class="panel-empty"><div class="panel-empty-icon">✦</div><h3>Hint is hidden</h3><p>Reveal a small clue without affecting your score.</p><button class="btn btn-primary" id="revealHintInside">Reveal hint</button></div>`;
  }
  return `<div class="reference-title">A CLUE FOR THIS QUESTION</div><h3>Think about the key idea</h3><p>${escapeHTML(q.hint)}</p><div class="note-box">Hints do not affect your score. You can revisit this clue later in the same profile.</div>`;
}

function renderReference(q) {
  const ref = referenceById.get(q.referenceId) || referenceById.get(q.topicId + '-ref');
  if (!ref) {
    return `<h3>Reference not available</h3><p>No reference section is mapped to this topic yet.</p>`;
  }
  const definitions = (ref.definitions || []).map(([term, definition]) => `<div class="definition-item"><strong>${escapeHTML(term)}</strong><span>${escapeHTML(definition)}</span></div>`).join('');
  const keyPoints = (ref.keyPoints || []).map((item) => `<li>${escapeHTML(item)}</li>`).join('');
  const mistakes = (ref.commonMistakes || []).map((item) => `<li>${escapeHTML(item)}</li>`).join('');
  return `<div class="reference-title">${escapeHTML(topicName(q.topicId))} · SESSIONS ${escapeHTML(ref.sessions || topicById.get(q.topicId)?.sessions || '')}</div>
    <h3>${escapeHTML(ref.title)}</h3><p>${escapeHTML(ref.overview)}</p>
    <h4>Key definitions</h4><div class="definition-list">${definitions}</div>
    <h4>Important concepts</h4><ul>${keyPoints}</ul>
    <h4>Worked example / application</h4><div class="example-box">${escapeHTML(ref.example || 'Review the definitions and apply them to a small example.')}</div>
    <h4>Common mistakes</h4><ul>${mistakes}</ul>
    <div class="note-box"><strong>Examination focus:</strong> ${escapeHTML(ref.examNotes || '')}</div>`;
}

function renderLearningContent() {
  const q = currentQuestion();
  if (!q) {
    $('learningContent').innerHTML = '<div class="panel-empty"><h3>No active question</h3><p>Change your filters to continue.</p></div>';
    return;
  }
  $('hintTab').classList.toggle('active', activeLearningTab === 'hint');
  $('referenceTab').classList.toggle('active', activeLearningTab === 'reference');
  $('hintTab').setAttribute('aria-selected', String(activeLearningTab === 'hint'));
  $('referenceTab').setAttribute('aria-selected', String(activeLearningTab === 'reference'));
  $('learningContent').innerHTML = activeLearningTab === 'hint' ? renderHint(q) : renderReference(q);
  const reveal = $('revealHintInside');
  if (reveal) reveal.addEventListener('click', revealHint);
}

function renderAll() {
  renderStats();
  renderNavigator();
  renderQuestion();
}

function navigateTo(questionId) {
  if (!visibleQuestions.some((q) => q.id === questionId)) return;
  currentQuestionId = questionId;
  renderAll();
  if (mobileDrawer === 'navigator') closeMobileDrawer();
}

function navigateByOffset(offset) {
  const index = visibleQuestions.findIndex((q) => q.id === currentQuestionId);
  const next = visibleQuestions[index + offset];
  if (next) navigateTo(next.id);
}

function selectAnswer(questionId, index) {
  const state = questionState(questionId);
  if (state.checked) return;
  progress.answers[questionId] = { ...state, selected: index, checked: false, correct: null };
  saveProgress();
  renderAll();
}

function checkAnswer() {
  const q = currentQuestion();
  if (!q) return;
  const state = questionState(q.id);
  if (state.checked) {
    retryQuestion(q.id);
    return;
  }
  if (state.selected === null) return;
  const correct = state.selected === q.correctAnswer;
  progress.answers[q.id] = { ...state, checked: true, correct, attempts: (state.attempts || 0) + 1, checkedAt: Date.now() };
  progress.session.checkedCount = checkedAnswerEntries().length;
  saveProgress();
  renderAll();
  if (correct) showToast('Correct — your progress has been saved.');
  else showToast('Not quite. Review the explanation and try again.');
}

function retryQuestion(questionId) {
  const old = questionState(questionId);
  progress.answers[questionId] = { selected: null, checked: false, correct: null, attempts: old.attempts || 0 };
  saveProgress();
  renderAll();
}

function resetCurrentQuestion() {
  const q = currentQuestion();
  if (!q) return;
  const old = questionState(q.id);
  delete progress.answers[q.id];
  saveProgress();
  renderAll();
  showToast(`Question ${q.number} reset.`);
}

function toggleFlag() {
  const q = currentQuestion();
  if (!q) return;
  if (isFlagged(q.id)) progress.flags = progress.flags.filter((id) => id !== q.id);
  else progress.flags.push(q.id);
  saveProgress();
  renderAll();
}

function revealHint() {
  const q = currentQuestion();
  if (!q) return;
  if (!isHintRevealed(q.id)) progress.hints.push(q.id);
  activeLearningTab = 'hint';
  saveProgress();
  renderAll();
  openMobileDrawer('learning');
}

function openReference() {
  activeLearningTab = 'reference';
  renderLearningContent();
  openMobileDrawer('learning');
}

function nextUnanswered() {
  const currentIndex = visibleQuestions.findIndex((q) => q.id === currentQuestionId);
  const ordered = [...visibleQuestions.slice(currentIndex + 1), ...visibleQuestions.slice(0, currentIndex + 1)];
  const target = ordered.find((q) => !questionState(q.id).checked);
  if (target) navigateTo(target.id);
  else showToast('No unchecked questions remain in the current view.');
}

function clearFilters() {
  $('modeSelect').value = 'all';
  $('subjectSelect').value = 'all';
  $('bankSelect').value = 'all';
  $('topicSelect').value = 'all';
  $('difficultySelect').value = 'all';
  $('statusSelect').value = 'all';
  $('searchInput').value = '';
  randomOrder = [];
  refreshVisibleQuestions(false);
}

function onFilterChange(event) {
  if (event?.target?.id === 'modeSelect') {
    const mode = $('modeSelect').value;
    if (mode === 'random' || mode === 'mock') randomOrder = shuffleArray(questions).map((q) => q.id);
    if (mode === 'mock') {
      progress.timer = { durationSec: 3600, remainingSec: 3600, deadline: null, running: false, completed: false };
      startTimer(60);
      showToast('Timed mock exam started · 60 minutes.');
    }
  }
  refreshVisibleQuestions(false);
}

function populateTopicSelect() {
  const select = $('topicSelect');
  topics.forEach((topic) => {
    const option = document.createElement('option');
    option.value = topic.id;
    option.textContent = `${topic.section} · ${topic.name}`;
    select.appendChild(option);
  });
}

function openOverlay(id) {
  closeMobileDrawer();
  activeOverlay = id;
  $(id).hidden = false;
  syncScrim();
  const firstInput = $(id).querySelector('input,button,select');
  firstInput?.focus({ preventScroll: true });
}

function closeOverlay(id = activeOverlay) {
  if (!id) return;
  $(id).hidden = true;
  if (activeOverlay === id) activeOverlay = null;
  syncScrim();
}

function openMobileDrawer(type) {
  if (window.innerWidth > 780) return;
  closeOverlay(activeOverlay);
  closeMobileDrawer();
  mobileDrawer = type;
  if (type === 'navigator') $('navigatorPanel').classList.add('mobile-open');
  if (type === 'learning') $('learningPanel').classList.add('mobile-open');
  syncScrim();
}

function closeMobileDrawer() {
  $('navigatorPanel').classList.remove('mobile-open');
  $('learningPanel').classList.remove('mobile-open');
  mobileDrawer = null;
  syncScrim();
}

function syncScrim() {
  const visible = Boolean(activeOverlay || mobileDrawer);
  $('scrim').classList.toggle('visible', visible);
}

function getTimerRemaining() {
  const timer = progress.timer;
  if (timer.running && timer.deadline) return Math.max(0, Math.ceil((timer.deadline - Date.now()) / 1000));
  return Math.max(0, Math.floor(timer.remainingSec || 0));
}

function formatTime(seconds) {
  const mins = Math.floor(seconds / 60).toString().padStart(2, '0');
  const secs = Math.floor(seconds % 60).toString().padStart(2, '0');
  return `${mins}:${secs}`;
}

function renderTimer() {
  if (!progress) return;
  const timer = progress.timer;
  const remaining = getTimerRemaining();
  $('timerDisplay').textContent = formatTime(remaining);
  $('timerMinutes').value = Math.max(1, Math.round((timer.durationSec || 1800) / 60));
  $('timerStart').textContent = timer.running ? 'Running…' : timer.remainingSec < timer.durationSec && !timer.completed ? 'Resume timer' : 'Start timer';
  $('timerStart').disabled = timer.running;
  $('timerPause').disabled = !timer.running;
  $('timerStatus').textContent = timer.completed ? 'Time is up. Your answers remain saved.' : timer.running ? 'Timer running — your deadline is stored as a timestamp.' : timer.remainingSec < timer.durationSec ? 'Paused. Resume when ready.' : 'Ready when you are.';
  if (timer.running && remaining <= 60) $('timerDisplay').style.color = 'var(--red)';
  else $('timerDisplay').style.color = 'var(--text)';
}

function startTimer(minutes = null) {
  const timer = progress.timer;
  if (minutes !== null) {
    const seconds = Math.min(240, Math.max(1, Number(minutes))) * 60;
    timer.durationSec = seconds;
    timer.remainingSec = seconds;
    timer.completed = false;
  }
  if (timer.completed || timer.remainingSec <= 0) {
    timer.remainingSec = timer.durationSec || 1800;
    timer.completed = false;
  }
  timer.deadline = Date.now() + timer.remainingSec * 1000;
  timer.running = true;
  saveProgress();
  renderTimer();
  ensureTimerInterval();
}

function pauseTimer() {
  const timer = progress.timer;
  if (!timer.running) return;
  timer.remainingSec = getTimerRemaining();
  timer.running = false;
  timer.deadline = null;
  saveProgress();
  renderTimer();
}

function resetTimer() {
  const mins = Math.min(240, Math.max(1, Number($('timerMinutes').value) || 30));
  progress.timer = { durationSec: mins * 60, remainingSec: mins * 60, deadline: null, running: false, completed: false };
  saveProgress();
  renderTimer();
  showToast('Timer reset.');
}

function ensureTimerInterval() {
  if (timerInterval) return;
  timerInterval = setInterval(() => {
    const remaining = getTimerRemaining();
    if (remaining !== lastTimerSecond) {
      lastTimerSecond = remaining;
      renderTimer();
    }
    if (progress.timer.running && remaining <= 0) {
      progress.timer.running = false;
      progress.timer.deadline = null;
      progress.timer.remainingSec = 0;
      progress.timer.completed = true;
      saveProgress();
      renderTimer();
      showToast('Study timer finished. Your current progress is saved.');
    }
  }, 250);
}

function renderAnalytics() {
  const stats = profileStats();
  const entries = checkedAnswerEntries();
  const correct = stats.correct;
  $('resultsSubtitle').textContent = `Candidate: ${profileName} · ${new Date().toLocaleDateString()}`;
  $('resultMetrics').innerHTML = [
    ['Checked', stats.attempted], ['Correct', correct], ['Incorrect', stats.incorrect], ['Accuracy', stats.accuracy === null ? '—' : `${stats.accuracy}%`]
  ].map(([label, value]) => `<div class="result-metric"><strong>${value}</strong><span>${label}</span></div>`).join('');

  const topicStats = new Map();
  entries.forEach(([id, answer]) => {
    const q = questionById.get(id);
    if (!q) return;
    const current = topicStats.get(q.topicId) || { attempted: 0, correct: 0 };
    current.attempted++;
    if (answer.correct) current.correct++;
    topicStats.set(q.topicId, current);
  });
  const topicRows = [...topicStats.entries()].map(([topicId, data]) => ({
    name: topicName(topicId), accuracy: Math.round(data.correct / data.attempted * 100), ...data
  })).sort((a, b) => a.accuracy - b.accuracy);
  $('topicAnalytics').innerHTML = topicRows.length ? topicRows.map((row) => `<div class="analytics-row"><span class="analytics-name" title="${escapeHTML(row.name)}">${escapeHTML(row.name)} · ${row.attempted} checked</span><strong>${row.accuracy}%</strong><div class="progress-track"><div class="progress-fill" style="width:${row.accuracy}%"></div></div></div>`).join('') : '<p class="dialog-copy">Check some answers to see topic performance.</p>';

  const difficultyStats = ['basic', 'medium', 'hard', 'expert'].map((level) => {
    const subset = entries.map(([id, ans]) => ({ q: questionById.get(id), ans })).filter((x) => x.q?.difficulty === level);
    const good = subset.filter((x) => x.ans.correct).length;
    return { level, attempted: subset.length, accuracy: subset.length ? Math.round(good / subset.length * 100) : null };
  }).filter((row) => row.attempted);
  $('difficultyAnalytics').innerHTML = difficultyStats.length ? difficultyStats.map((row) => `<div class="analytics-row"><span class="analytics-name">${row.level[0].toUpperCase() + row.level.slice(1)} · ${row.attempted} checked</span><strong>${row.accuracy}%</strong><div class="progress-track"><div class="progress-fill" style="width:${row.accuracy}%"></div></div></div>`).join('') : '<p class="dialog-copy">Difficulty analysis will appear after you check answers.</p>';

  const weak = topicRows.filter((row) => row.attempted > 0 && row.accuracy < 70).slice(0, 4);
  const strong = topicRows.filter((row) => row.attempted > 0 && row.accuracy >= 80).slice(-3);
  let suggestion = 'Keep practising across the topics to build a useful performance baseline.';
  if (weak.length) suggestion = `Prioritise revision in: ${weak.map((x) => `${x.name} (${x.accuracy}%)`).join('; ')}. Use topic practice and the study references, then retry incorrect questions.`;
  else if (strong.length) suggestion = `Good progress in: ${strong.map((x) => x.name).join('; ')}. Continue practising the remaining topics and increase difficulty gradually.`;
  $('reviewSuggestions').innerHTML = `<h3>Recommended next step</h3><p>${escapeHTML(suggestion)}${progress.flags.length ? ` You also have ${progress.flags.length} flagged question(s) to revisit.` : ''}</p>`;
}

function exportProgress() {
  const payload = {
    application: 'PGCP-AI Mathematics and Statistics for AI Learning Platform',
    schemaVersion: 1,
    exportedAt: new Date().toISOString(),
    candidateName: profileName,
    subject: 'Mathematics and Statistics for AI',
    questionDataVersion: '600-question-bank-v2',
    progress: {
      answers: progress.answers,
      flags: progress.flags,
      hints: progress.hints,
      timer: progress.timer,
      session: progress.session,
      themePreference: progress.themePreference
    }
  };
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `pgcp-ai-math-ai-progress-${profileName.toLowerCase().replace(/[^a-z0-9]+/g, '-')}.json`;
  a.click();
  URL.revokeObjectURL(url);
  showToast('Progress JSON exported.');
}

async function importProgressFile(file) {
  try {
    const parsed = JSON.parse(await file.text());
    if (parsed?.schemaVersion !== 1 || parsed?.subject !== 'Mathematics and Statistics for AI' || !parsed?.progress || typeof parsed.progress.answers !== 'object' || !Array.isArray(parsed.progress.flags) || !Array.isArray(parsed.progress.hints)) {
      throw new Error('This file is not a valid progress export for this application.');
    }
    const imported = parsed.progress;
    for (const [id, answer] of Object.entries(imported.answers)) {
      if (!questionById.has(id)) throw new Error(`Unknown question ID: ${id}`);
      if (answer.selected !== null && (!Number.isInteger(answer.selected) || answer.selected < 0 || answer.selected > 3)) throw new Error(`Invalid selected option for ${id}`);
      if (typeof answer.checked !== 'boolean') throw new Error(`Invalid checked status for ${id}`);
    }
    if (imported.flags.some((id) => !questionById.has(id)) || imported.hints.some((id) => !questionById.has(id))) throw new Error('The import contains question IDs that do not exist in this version.');
    if (!window.confirm('Import this file and replace the current progress for this candidate profile? Export a backup first if needed.')) return;
    progress.answers = imported.answers;
    progress.flags = [...new Set(imported.flags)];
    progress.hints = [...new Set(imported.hints)];
    if (imported.timer && typeof imported.timer === 'object') progress.timer = { ...progress.timer, ...imported.timer };
    if (imported.session && typeof imported.session === 'object') progress.session = { ...progress.session, ...imported.session };
    saveProgress();
    refreshVisibleQuestions(true);
    renderTimer();
    closeOverlay('settingsDialog');
    showToast('Progress imported successfully.');
  } catch (error) {
    showToast(error.message || 'Could not import this file.');
  } finally {
    $('importFile').value = '';
  }
}

function resetProfile() {
  if (!window.confirm(`Reset all saved answers, flags, hints and timer data for ${profileName}? This cannot be undone unless you exported a backup.`)) return;
  localStorage.removeItem(profileKey(profileName));
  progress = defaultProgress(profileName);
  saveProgress();
  clearFilters();
  renderTimer();
  closeOverlay('settingsDialog');
  showToast('This profile has been reset.');
}

function switchProfile(nextName) {
  const clean = String(nextName || '').trim().slice(0, 40) || 'Learner';
  if (clean.toLowerCase() === profileName.toLowerCase()) {
    $('candidateName').value = profileName;
    return;
  }
  saveProgress();
  pauseTimer();
  progress = loadProfile(clean);
  profileName = clean;
  localStorage.setItem(ACTIVE_PROFILE_KEY, profileName);
  $('candidateName').value = profileName;
  setTheme(progress.themePreference || 'system', false);
  randomOrder = [];
  refreshVisibleQuestions(false);
  renderTimer();
  if (progress.timer.running && progress.timer.deadline) ensureTimerInterval();
  showToast(`Switched to ${profileName}'s local profile.`);
}

function onKeyboard(event) {
  if (event.altKey || event.ctrlKey || event.metaKey) return;
  const tag = event.target?.tagName?.toLowerCase();
  if (['input', 'textarea', 'select'].includes(tag)) return;
  if (activeOverlay) {
    if (event.key === 'Escape') closeOverlay(activeOverlay);
    return;
  }
  if (event.key >= '1' && event.key <= '4') {
    const q = currentQuestion();
    if (q) selectAnswer(q.id, Number(event.key) - 1);
  } else if (event.key === 'ArrowLeft') {
    event.preventDefault(); navigateByOffset(-1);
  } else if (event.key === 'ArrowRight') {
    event.preventDefault(); navigateByOffset(1);
  } else if (event.key.toLowerCase() === 'h') {
    revealHint();
  } else if (event.key.toLowerCase() === 'f') {
    toggleFlag();
  } else if (event.key === 'Escape' && mobileDrawer) {
    closeMobileDrawer();
  }
}

function bindEvents() {
  $('themeSelect').addEventListener('change', (event) => setTheme(event.target.value));
  $('candidateName').addEventListener('change', (event) => switchProfile(event.target.value));
  $('candidateName').addEventListener('keydown', (event) => { if (event.key === 'Enter') event.target.blur(); });
  ['modeSelect', 'subjectSelect', 'bankSelect', 'topicSelect', 'difficultySelect', 'statusSelect'].forEach((id) => $(id).addEventListener('change', onFilterChange));
  $('searchInput').addEventListener('input', () => refreshVisibleQuestions(true));
  $('clearFilters').addEventListener('click', clearFilters);
  $('emptyClear').addEventListener('click', clearFilters);
  $('previousButton').addEventListener('click', () => navigateByOffset(-1));
  $('nextButton').addEventListener('click', () => navigateByOffset(1));
  $('nextUnanswered').addEventListener('click', nextUnanswered);
  $('checkButton').addEventListener('click', checkAnswer);
  $('flagButton').addEventListener('click', toggleFlag);
  $('hintButton').addEventListener('click', revealHint);
  $('referenceButton').addEventListener('click', openReference);
  $('resetQuestionButton').addEventListener('click', resetCurrentQuestion);
  $('hintTab').addEventListener('click', () => { activeLearningTab = 'hint'; renderLearningContent(); });
  $('referenceTab').addEventListener('click', () => { activeLearningTab = 'reference'; renderLearningContent(); });
  $('mobileNavOpen').addEventListener('click', () => openMobileDrawer('navigator'));
  $('focusToggle').addEventListener('click', () => {
    $('appShell').classList.toggle('focus-mode');
    $('focusToggle').classList.toggle('is-active', $('appShell').classList.contains('focus-mode'));
  });
  $('timerOpen').addEventListener('click', () => { renderTimer(); openOverlay('timerDialog'); });
  $('resultsOpen').addEventListener('click', () => { renderAnalytics(); openOverlay('resultsDialog'); });
  $('settingsOpen').addEventListener('click', () => openOverlay('settingsDialog'));
  document.querySelectorAll('[data-close]').forEach((button) => button.addEventListener('click', () => closeOverlay(button.dataset.close)));
  $('closeResults').addEventListener('click', () => closeOverlay('resultsDialog'));
  $('exportButton').addEventListener('click', exportProgress);
  $('settingsExport').addEventListener('click', exportProgress);
  $('importButton').addEventListener('click', () => $('importFile').click());
  $('importFile').addEventListener('change', (event) => { const file = event.target.files?.[0]; if (file) importProgressFile(file); });
  $('resetAllButton').addEventListener('click', resetProfile);
  $('timerStart').addEventListener('click', () => {
    const timer = progress.timer;
    if (timer.remainingSec < timer.durationSec && !timer.completed) startTimer(null);
    else startTimer(Number($('timerMinutes').value));
  });
  $('timerPause').addEventListener('click', pauseTimer);
  $('timerReset').addEventListener('click', resetTimer);
  $('timerMinutes').addEventListener('change', () => {
    if (!progress.timer.running) {
      const mins = Math.min(240, Math.max(1, Number($('timerMinutes').value) || 30));
      progress.timer.durationSec = mins * 60;
      progress.timer.remainingSec = mins * 60;
      progress.timer.completed = false;
      saveProgress();
      renderTimer();
    }
  });
  $('scrim').addEventListener('click', () => {
    if (activeOverlay) closeOverlay(activeOverlay);
    if (mobileDrawer) closeMobileDrawer();
  });
  document.addEventListener('keydown', onKeyboard);
  window.matchMedia?.('(prefers-color-scheme: dark)').addEventListener?.('change', () => {
    if ((progress?.themePreference || localStorage.getItem(THEME_KEY) || 'system') === 'system') setTheme('system', false);
  });
  window.addEventListener('beforeunload', () => {
    if (progress?.timer?.running) {
      progress.timer.remainingSec = getTimerRemaining();
      saveProgress();
    }
  });
}

async function init() {
  try {
    const responses = await Promise.all([
      ...DATA_FILES.map((url) => fetch(url)),
      fetch('./data/topics.json'),
      fetch('./data/references.json')
    ]);
    if (responses.some((response) => !response.ok)) throw new Error('One or more question or reference files could not be loaded.');
    const json = await Promise.all(responses.map((response) => response.json()));
    questions = json.slice(0, 3).flat();
    topics = json[3];
    references = json[4];
    questionById = new Map(questions.map((q) => [q.id, q]));
    topicById = new Map(topics.map((t) => [t.id, t]));
    referenceById = new Map(references.map((r) => [r.id, r]));
    populateTopicSelect();
    const rememberedProfile = localStorage.getItem(ACTIVE_PROFILE_KEY) || 'Learner';
    progress = loadProfile(rememberedProfile);
    profileName = progress.candidateName || rememberedProfile || 'Learner';
    $('candidateName').value = profileName;
    setTheme(progress.themePreference || localStorage.getItem(THEME_KEY) || 'system', false);
    visibleQuestions = [...questions].sort((a, b) => a.number - b.number);
    currentQuestionId = visibleQuestions[0]?.id || null;
    bindEvents();
    renderAll();
    renderTimer();
    if (progress.timer.running && progress.timer.deadline) ensureTimerInterval();
  } catch (error) {
    console.error(error);
    $('questionStem').textContent = 'The learning data could not be loaded. Open this application through a local web server or its deployed URL (not directly as a file).';
    $('answerOptions').innerHTML = `<p class="dialog-copy">${escapeHTML(error.message)}</p>`;
  }
}

init();
