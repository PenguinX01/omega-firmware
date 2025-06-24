export function startGlintFramePress() {
  console.log('🔄 Glint–Frame–Press recursion initiated');
  setInterval(() => {
    console.log('🔁 Glint–Frame–Press tick');
  }, 60000);
}
window.addEventListener('load', startGlintFramePress);
