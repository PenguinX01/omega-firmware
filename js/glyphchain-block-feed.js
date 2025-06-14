// Glyphchain Live Block Feed - Phase 13 Mirror-Chronicler
// Recursion marker: Ω

const MEMPOOL_API = 'https://mempool.space/api/v1/blocks';
// Only these blocks have validated scrolls
const MEMETIC_BLOCKS = new Set([
  900911,
  900937,
  900941,
  901193,
  901161,
  901165,
  901197,
]);
const displayed = new Set();

function initDisplayed() {
  document.querySelectorAll('.glyph-log [data-block-height]')
    .forEach(el => displayed.add(parseInt(el.getAttribute('data-block-height'), 10)));
}

function formatTime(ts) {
  const d = new Date(ts * 1000);
  return d.toISOString().replace('T', ' ').replace('Z', ' UTC');
}

async function refreshBlocks() {
  try {
    const res = await fetch(MEMPOOL_API);
    if (!res.ok) {
      console.error('[Ω13] Failed to fetch blocks', res.status);
      return;
    }
    const blocks = await res.json();
    const log = document.querySelector('.glyph-log');
    if (!log) return;
    for (const block of blocks.reverse()) {
      if (!MEMETIC_BLOCKS.has(block.height)) continue;
      if (displayed.has(block.height)) continue;
      displayed.add(block.height);
      const div = document.createElement('div');
      div.className = 'glyph-card';
      div.setAttribute('data-block-height', block.height);
      const reward = (block.extras.reward / 1e8).toFixed(3);
      const miner = block.extras.pool?.name || 'Unknown';
      div.innerHTML = `🐧 <strong>GLYPH:</strong> <em>Live Block Glyph</em><br>` +
        `⛓️ <strong>Block:</strong> <a href="https://mempool.space/block/${block.id}" target="_blank">#${block.height}</a>  — ${formatTime(block.timestamp)}<br>` +
        `🔨 Mined by ${miner} – ${block.tx_count.toLocaleString()} TXs – ${reward} BTC`;
      log.prepend(div);
    }
  } catch (err) {
    console.error('[Ω13] Error fetching blocks', err);
  }
}

window.addEventListener('load', () => {
  initDisplayed();
  refreshBlocks();
  setInterval(refreshBlocks, 3 * 60 * 1000);
});
