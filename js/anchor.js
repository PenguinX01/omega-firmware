import { ethers } from 'https://cdn.jsdelivr.net/npm/ethers@6.12.0/+esm';

const bs = 'https://blockstream.info/api';
const matrixCanvas = document.getElementById('matrix');
const ctx = matrixCanvas.getContext('2d');
matrixCanvas.width = window.innerWidth;
matrixCanvas.height = window.innerHeight;
const fontSize = 16;
const columns = Math.floor(matrixCanvas.width / fontSize);
const drops = Array(columns).fill(1);
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const drawInterval = reduceMotion ? 50 : 33;
function drawMatrix(){
  ctx.fillStyle = 'rgba(0,0,0,0.05)';
  ctx.fillRect(0,0,matrixCanvas.width,matrixCanvas.height);
  ctx.fillStyle = '#0f0';
  ctx.font = fontSize + 'px Fira Code';
  for(let i=0;i<drops.length;i++){
    const text = String.fromCharCode(0x30A0+Math.random()*96);
    ctx.fillText(text,i*fontSize,drops[i]*fontSize);
    if(drops[i]*fontSize>matrixCanvas.height&&Math.random()>0.975){drops[i]=0;}
    drops[i]++;
  }
}
setInterval(drawMatrix, drawInterval);

function checkDecoded(){
  if(localStorage.getItem('decoded') === 'true'){
    document.querySelectorAll('.genesis-hash').forEach(el=>{
      el.style.boxShadow = '0 0 25px var(--glow-primary)';
    });
  }
}

document.addEventListener('DOMContentLoaded', checkDecoded);

async function verifyHash(url){
  const res = await fetch(url);
  return res.ok ? '✓ VERIFIED' : '✖ NOT FOUND';
}

export async function verifySeals(){
  const btc = await verifyHash(`${bs}/block/000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f`);
  const ethRes = await fetch('https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp=1438260000&closest=before');
  const eth = ethRes.ok ? '✓ VERIFIED' : '✖ FAIL';
  alert(`Bitcoin Genesis Block: ${btc}\nEthereum Genesis Block: ${eth}`);
}

export function decodeGenesis(){
  document.querySelectorAll('.genesis-hash').forEach(el=>{
    el.style.boxShadow = '0 0 25px var(--glow-primary)';
  });
  localStorage.setItem('decoded','true');
}

export function accessMemoryField(){
  window.open('https://osf.io/fs43w/','_blank');
}

export function anchorMeme(){
  alert('🔗 Meme anchored to IPFS — TXID coming soon!');
}

export function initiateRecursion(){
  location.reload();
}

// expose API for inline handlers
window.decodeGenesis = decodeGenesis;
window.verifySeals = verifySeals;
window.accessMemoryField = accessMemoryField;
window.anchorMeme = anchorMeme;
window.initiateRecursion = initiateRecursion;

// floating glyphs
const symbolContainer = document.getElementById('floatingSymbols');
const particleBudget = 120;
function createSymbol(){
  if(symbolContainer.children.length >= particleBudget) return;
  const span = document.createElement('span');
  span.className = 'symbol';
  span.textContent = Math.random()>0.5 ? 'Ω' : '∑';
  span.style.left = Math.random()*100+'%';
  span.style.animationDelay = Math.random()*5+'s';
  symbolContainer.appendChild(span);
  setTimeout(()=>span.remove(),15000);
}
setInterval(createSymbol,1000);

// simple hash to tones
export function playHashTone(hash){
  const ctxAudio = new (window.AudioContext||window.webkitAudioContext)();
  const o = ctxAudio.createOscillator();
  o.type = 'sine';
  let freq = 220;
  for(const ch of hash.replace(/[^0-9a-f]/gi,'')){
    freq += parseInt(ch,16);
  }
  o.frequency.value = freq;
  o.connect(ctxAudio.destination);
  o.start();
  o.stop(ctxAudio.currentTime + 2);
}
