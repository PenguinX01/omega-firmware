// Contradiction Feed - Phase 13 Mirror-Chronicler
// Recursion marker: Ω∞

async function startContradictionFeed() {
  const log = document.getElementById('scrollStepLog');
  if (!log) return;
  try {
    const res = await fetch('./contradictions.json');
    const contradictions = await res.json();
    shuffle(contradictions);
    let index = 0;
    async function displayNext() {
      const item = contradictions[index];
      index = (index + 1) % contradictions.length;
      const line = document.createElement('div');
      line.className = 'terminal-line';
      const prefix = `🧠 [${item.glyph}] `;
      typeLine(prefix + item.text, line, () => {
        log.appendChild(line);
        log.scrollTop = log.scrollHeight;
        const delay = 5000 + Math.random() * 5000;
        setTimeout(displayNext, delay);
      });
    }
    displayNext();
  } catch (err) {
    console.error('[ContradictionFeed] failed to load', err);
  }
}

function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
}

function typeLine(text, el, cb) {
  let i = 0;
  const cursor = document.createElement('span');
  cursor.className = 'cursor';
  el.textContent = '';
  el.appendChild(cursor);
  function step() {
    if (i < text.length) {
      el.textContent = text.slice(0, i + 1);
      el.appendChild(cursor);
      i++;
      setTimeout(step, 40);
    } else {
      el.removeChild(cursor);
      cb && cb();
    }
  }
  step();
}

window.addEventListener('load', startContradictionFeed);
