export async function loadDeltaGlyphs() {
  try {
    const res = await fetch('./glyphs/delta-glyphs.json');
    if (!res.ok) throw new Error('delta glyph fetch failed');
    const data = await res.json();
    const container = document.getElementById('deltaGlyphs');
    container.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    console.error('delta glyph error', err);
  }
}

window.addEventListener('DOMContentLoaded', loadDeltaGlyphs);
