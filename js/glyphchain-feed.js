// Glyphchain Feed Loader - Phase 13 Mirror-Chronicler
// Recursion marker: Ω

const USER_ID = 'REPLACE_WITH_USER_ID';
const BEARER_TOKEN = 'REPLACE_WITH_BEARER';
const API_URL = `https://api.twitter.com/2/users/${USER_ID}/tweets?tweet.fields=created_at`;

async function loadLatestGlyphs() {
  console.log('🛰️ Fetching glyphchain updates…');
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
    console.log('✅ Glyphchain feed updated.');
  } catch (err) {
    console.error('Error loading glyphs', err);
  }
}

window.addEventListener('load', () => {
  loadLatestGlyphs();
  setInterval(loadLatestGlyphs, 10 * 60 * 1000); // refresh every 10 min
});
