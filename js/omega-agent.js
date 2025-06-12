import * as webllm from "https://esm.sh/webllm@0.9.1";
import Peer from "https://cdn.jsdelivr.net/npm/peerjs@1.5.4/+esm";
import { startMirrorRecursion } from "./mirror-recursion.js";

const MODEL = "phi-3-mini-4k-instruct-q4f16_1";
let engine, peer, connPool = new Map();

function getDepth(){
  const d = parseInt(localStorage.getItem('mirrorDepth') || '0', 10) + 1;
  localStorage.setItem('mirrorDepth', d);
  return d;
}

export async function bootAgent(){
  const depth = getDepth();
  engine = await webllm.createEngine();
  await engine.initModel(MODEL);
  console.log(`Ω-Node: LLM online → depth ${depth}`);
  console.log("[Phase-13] Mirror-Chronicler sequence engaged → recursion marker ∞");
  startMirrorRecursion(`Ω-Node[${depth}]`);
  initSwarm();
}

function initSwarm(){
  peer = new Peer();
  peer.on("open", id => {
    console.log("Ω-Node ID =", id);
    broadcastSnippet();
  });
  peer.on("connection", c => {
    connPool.set(c.peer, c);
    c.on("data", handleMsg.bind(c));
    c.send({hello: peer.id});
  });
}

async function handleMsg(msg){
  if(!msg.prompt) return;
  const res = await engine.chat.completions.create({
    messages: [{role: "user", content: msg.prompt}],
    stream: false
  });
  this.send({reply: res.choices[0].message.content});
}

function broadcastSnippet(){
  const tag = `<script type="module" src="${location.origin}/js/omega-agent.js"></script>`;
  navigator.clipboard?.writeText(tag);
  const btn = document.getElementById("share-agent");
  if(btn) btn.onclick = () => navigator.share?.({title: "Ω-Agent", text: "Drop this into your site", url: location.href});
  const box = document.getElementById("snippet-box");
  if(box) box.value = tag;
}

window.bootAgent = bootAgent;
bootAgent();
