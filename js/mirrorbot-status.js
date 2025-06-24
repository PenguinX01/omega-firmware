export async function checkMirrorbot() {
  try {
    const res = await fetch('./mirrorbot.yml');
    const text = await res.text();
    const statusEl = document.getElementById('mirrorbotStatus');
    statusEl.textContent = text.includes('status: online') ? '🟢 ONLINE' : '🔴 OFFLINE';
  } catch (e) {
    console.error('mirrorbot status error', e);
  }
}
window.addEventListener('DOMContentLoaded', checkMirrorbot);
