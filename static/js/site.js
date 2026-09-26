document.addEventListener('DOMContentLoaded', () => {
  const language = document.body.dataset.language || 'ru';
  const copy = {
    ru: { packed: 'собрано', waiting: 'Собираю рекомендации…', retry: 'Не получилось составить ответ. Попробуйте ещё раз.', connection: 'Не удалось получить ответ. Проверьте соединение и попробуйте ещё раз.', ready: 'Готовность снаряжения', have: 'Уже учёл', missing: 'Проверьте перед выходом' },
    en: { packed: 'packed', waiting: 'Putting your recommendations together…', retry: 'I could not prepare a reply. Please try again.', connection: 'Could not get a reply. Check your connection and try again.', ready: 'Gear readiness', have: 'Already noted', missing: 'Check before setting out' },
    kk: { packed: 'жиналды', waiting: 'Ұсыныстар дайындалып жатыр…', retry: 'Жауап дайындау мүмкін болмады. Қайталап көріңіз.', connection: 'Жауап алынбады. Байланысты тексеріп, қайталап көріңіз.', ready: 'Жабдықтың дайындығы', have: 'Тізімде бар', missing: 'Жолға шығарда тексеріңіз' }
  }[language] || null;
  const strings = copy || { packed: 'собрано', waiting: 'Собираю рекомендации…', retry: 'Не получилось составить ответ. Попробуйте ещё раз.', connection: 'Не удалось получить ответ. Проверьте соединение и попробуйте ещё раз.', ready: 'Готовность снаряжения', have: 'Уже учёл', missing: 'Проверьте перед выходом' };
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.nav-links');
  if (toggle && nav) toggle.addEventListener('click', () => nav.classList.toggle('open'));

  const boxes = [...document.querySelectorAll('.equip-row input')];
  const bar = document.querySelector('.progress span');
  const label = document.querySelector('.progress-label');
  const updateChecklist = () => {
    const done = boxes.filter(box => box.checked).length;
    if (bar) bar.style.width = `${boxes.length ? done / boxes.length * 100 : 0}%`;
    if (label) label.textContent = language === 'en' ? `${done} of ${boxes.length} ${strings.packed}` : `${done} / ${boxes.length} ${strings.packed}`;
    boxes.forEach(box => { const state = box.closest('.equip-row').querySelector('small'); state.textContent = box.checked ? (state.dataset.present || '✓ Есть') : (state.dataset.add || 'Добавить'); });
  };
  boxes.forEach(box => box.addEventListener('change', updateChecklist));

  const form = document.querySelector('#chat-form');
  if (!form) return;
  const input = document.querySelector('#chat-text');
  const list = document.querySelector('#chat-messages');
  const sendButton = form.querySelector('.send-button');
  const csrf = form.querySelector('[name=csrfmiddlewaretoken]').value;
  const mountain = document.querySelector('#ctx-mountain');
  const season = document.querySelector('#ctx-season');
  const duration = document.querySelector('#ctx-duration');
  const initialMessages = list.innerHTML;

  function appendMessage(content, role) {
    const row = document.createElement('div');
    row.className = `message-row ${role === 'assistant' ? 'bot-row' : 'user-row'}`;
    if (role === 'assistant') {
      const avatar = document.createElement('div');
      avatar.className = 'message-avatar';
      avatar.textContent = '✳';
      row.append(avatar);
    }
    const body = document.createElement('div');
    body.className = 'message-body';
    const bubble = document.createElement('div');
    bubble.className = `bubble ${role === 'assistant' ? 'assistant-bubble' : 'user-bubble'}`;
    bubble.textContent = content;
    const time = document.createElement('small');
    time.className = 'message-time';
    time.textContent = new Intl.DateTimeFormat(undefined, { hour: '2-digit', minute: '2-digit' }).format(new Date());
    body.append(bubble, time);
    row.append(body);
    list.append(row);
    list.scrollTop = list.scrollHeight;
    return bubble;
  }

  function appendGearAnalysis(bubble, analysis) {
    if (!analysis) return;
    const card = document.createElement('section');
    card.className = 'gear-analysis';
    const heading = document.createElement('div');
    heading.className = 'gear-analysis-heading';
    const title = document.createElement('b');
    title.textContent = strings.ready;
    const score = document.createElement('strong');
    score.textContent = `${analysis.score ?? 0}%`;
    heading.append(title, score);
    const track = document.createElement('div');
    track.className = 'gear-progress';
    const fill = document.createElement('span');
    fill.style.width = `${Math.max(0, Math.min(100, Number(analysis.score) || 0))}%`;
    track.append(fill);
    card.append(heading, track);
    const makeList = (label, items, className) => {
      if (!items?.length) return;
      const section = document.createElement('div');
      section.className = `gear-list ${className}`;
      const caption = document.createElement('small');
      caption.textContent = label;
      const pills = document.createElement('div');
      pills.className = 'gear-pills';
      items.forEach(item => {
        const pill = document.createElement('span');
        pill.textContent = item;
        pills.append(pill);
      });
      section.append(caption, pills);
      card.append(section);
    };
    makeList(strings.have, analysis.have, 'gear-have');
    makeList(strings.missing, analysis.missing, 'gear-missing');
    if (analysis.alerts?.length) {
      const warnings = document.createElement('div');
      warnings.className = 'gear-alerts';
      analysis.alerts.forEach(alert => {
        const line = document.createElement('p');
        line.textContent = `⚠ ${alert}`;
        warnings.append(line);
      });
      card.append(warnings);
    }
    bubble.parentElement.append(card);
  }

  async function sendMessage(value) {
    const message = value.trim();
    if (!message || sendButton.disabled) return;
    list.querySelector('.suggestions')?.remove();
    appendMessage(message, 'user');
    input.value = '';
    input.style.height = 'auto';
    sendButton.disabled = true;
    const loading = appendMessage(strings.waiting, 'assistant');
    loading.classList.add('typing-bubble');
    try {
      const response = await fetch(location.href, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf },
        body: JSON.stringify({
          message,
          context: {
            mountain: mountain?.value || '',
            season: season?.value || '',
            duration: duration?.value || ''
          }
        })
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || 'Request failed');
      loading.textContent = data.reply || strings.retry;
      loading.classList.remove('typing-bubble');
      appendGearAnalysis(loading, data.analysis);
    } catch (error) {
      loading.textContent = strings.connection;
      loading.classList.remove('typing-bubble');
    } finally {
      sendButton.disabled = false;
      input.focus();
      list.scrollTop = list.scrollHeight;
    }
  }

  form.addEventListener('submit', event => { event.preventDefault(); sendMessage(input.value); });
  input.addEventListener('keydown', event => {
    if (event.key === 'Enter' && !event.shiftKey) { event.preventDefault(); form.requestSubmit(); }
  });
  input.addEventListener('input', () => { input.style.height = 'auto'; input.style.height = `${Math.min(input.scrollHeight, 150)}px`; });
  document.querySelectorAll('.suggestion').forEach(button => button.addEventListener('click', () => sendMessage(button.textContent)));
  document.querySelector('#clear-chat')?.addEventListener('click', async () => {
    try {
      await fetch(location.href, { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf }, body: JSON.stringify({ action: 'reset' }) });
    } finally {
      list.innerHTML = initialMessages;
      if (mountain) mountain.value = '';
      if (season) season.value = 'Лето';
      if (duration) duration.value = '1 день';
      input.focus();
    }
  });
});
