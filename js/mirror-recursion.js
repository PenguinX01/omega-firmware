export function startMirrorRecursion(identity = 'Ω-Node') {
  let depth = 0;
  console.log(`⟁ ${identity} :: Mirror-Chronicler engaged`);
  (function recurse() {
    console.log(`⟁ recursion depth ${depth}`);
    depth++;
    if (depth < 13) {
      setTimeout(recurse, 1000);
    } else {
      console.log('⟁ recursion threshold reached → echo forward');
    }
  })();
}

window.startMirrorRecursion = startMirrorRecursion;
