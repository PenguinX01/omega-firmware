export function startFractalModule() {
  console.log('[Phase-13] Fractal Frequency Module engaged :: Ω∞');
  const heightEl = document.getElementById('btcHeight');
  const intervalEl = document.getElementById('btcInterval');
  const schumannEl = document.getElementById('schumannValue');
  const pulseEl = document.getElementById('glyphPulse');
  let prevTimestamp = null;
  async function refreshBlock() {
    try {
      const blocks = await fetch('https://blockstream.info/api/blocks').then(r => r.json());
      if (!blocks || blocks.length < 2) return;
      const latest = blocks[0];
      const prior = blocks[1];
      heightEl.textContent = latest.height;
      const delta = prevTimestamp ? latest.timestamp - prevTimestamp : latest.timestamp - prior.timestamp;
      intervalEl.textContent = delta + 's';
      prevTimestamp = latest.timestamp;
    } catch (err) {
      console.error('[Fractal] Block fetch error', err);
    }
  }
  function updateSchumann() {
    const t = Date.now() / 1000;
    const amp = (Math.sin(2 * Math.PI * 7.83 * t) + 1) / 2;
    schumannEl.textContent = amp.toFixed(2);
  }
  function pulseGlyph() {
    pulseEl.classList.toggle('active');
  }
  refreshBlock();
  setInterval(refreshBlock, 60000);
  setInterval(updateSchumann, 100);
  setInterval(pulseGlyph, 500);
}

window.startFractalModule = startFractalModule;
document.addEventListener('DOMContentLoaded', startFractalModule);
