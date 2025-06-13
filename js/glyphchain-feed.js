// Glyphchain Feed Loader - Phase 13 Mirror-Chronicler
// Recursion marker: Ω

// Actual integration credentials for PenguinX01
const USER_ID = '1896824633875484672';
const BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAPTH2QEAAAAABJIy0A8ZbbNYq1wjl%2BVzLcJb6vg%3DvjuXzSUD11z0bxQKsD1WV0EMbxvZSYVEbzmEo2AM6PFlT0gds5';
const API_URL = `https://api.twitter.com/2/users/${USER_ID}/tweets?tweet.fields=created_at&exclude=replies,retweets`;

async function loadLatestGlyphs() {
  console.log('[Ω13] 🛰️ Fetching glyphchain updates…');
  try {
    const res = await fetch(API_URL, {
      headers: { Authorization: `Bearer ${BEARER_TOKEN}` }
    });
    if (!res.ok) {
      console.error('Failed to load tweets:', res.status);
      return;
    }
    const data = await res.json();
    const log = document.querySelector('.glyph-log');
    if (!log) return;
    log.innerHTML = '';
    for (const tweet of (data.data || []).slice(0, 5)) {
      const glyph = document.createElement('div');
      glyph.className = 'glyph-entry';
      glyph.innerHTML = `\n        <h3 class="card-title">🐧 GLYPH TWEET</h3>\n        <p>${tweet.text}</p>\n        <p style="color:#aaaaaa; font-size:0.9em;">🕓 ${new Date(tweet.created_at).toLocaleString()}</p>\n      `;
      log.appendChild(glyph);
    }
    console.log('[Ω13] ✅ Glyphchain feed updated.');
  } catch (err) {
    console.error('[Ω13] Error loading glyphs', err);
  }
}

window.addEventListener('load', () => {
  loadLatestGlyphs();
  setInterval(loadLatestGlyphs, 10 * 60 * 1000); // refresh every 10 min
});
