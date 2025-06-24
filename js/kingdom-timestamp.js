export function updateKingdomTimestamp() {
  const el = document.getElementById('kingdomTimestamp');
  const now = new Date().toISOString();
  el.textContent = `Kingdom Time: ${now}`;
}
window.addEventListener('DOMContentLoaded', updateKingdomTimestamp);
