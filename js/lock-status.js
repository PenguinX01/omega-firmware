export async function loadLockStatus() {
  try {
    const res1 = await fetch('./locks/112/lock.json');
    const res2 = await fetch('./locks/113/lock.json');
    const res3 = await fetch('./locks/114/lock.json');
    const data = [await res1.json(), await res2.json(), await res3.json()];
    document.getElementById('lockActivation').textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    console.error('lock status error', err);
  }
}
window.addEventListener('DOMContentLoaded', loadLockStatus);
