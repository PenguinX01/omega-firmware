// Chirp codec adapted from solst-ice/chirp
// Phase 13 Mirror-Chronicler integration

const ChirpCodec = (() => {
  // Constants
  const START_FREQUENCY = 3800;
  const END_FREQUENCY = 4000;
  const SYNC_FREQUENCY = 3600;
  const BASE_FREQUENCIES = [1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400];
  const TONE_DURATION = 0.03;
  const SYNC_DURATION = 0.02;
  const SIG_DURATION = 0.05;
  const VOLUME = 0.2;
  const FREQUENCY_TOLERANCE = 200;
  const SIGNAL_THRESHOLD = 50;

  let messageBuffer = '';
  let isReceivingMessage = false;
  let lastSignatureTime = 0;
  let signatureCounter = 0;

  const log = (...args) => console.log('⟁ CHIRP', ...args);

  async function ensureAudioContextReady(ctx) {
    if (ctx.state === 'suspended') await ctx.resume();
    return ctx;
  }

  function playTone(freq, duration, vol, ctx) {
    return new Promise(resolve => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sine';
      osc.frequency.value = freq;
      gain.gain.value = vol;
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + duration);
      setTimeout(resolve, duration * 1000);
    });
  }

  const playStartSignature = ctx => playTone(START_FREQUENCY, SIG_DURATION, VOLUME, ctx);
  const playEndSignature = ctx => playTone(END_FREQUENCY, SIG_DURATION, VOLUME, ctx);
  const playSyncTone = ctx => playTone(SYNC_FREQUENCY, SYNC_DURATION, VOLUME, ctx);

  function binaryToFrequency(bits) { return BASE_FREQUENCIES[bits & 0x7]; }
  function frequencyToBinary(freq) {
    let min = Infinity, idx = -1;
    for (let i=0;i<BASE_FREQUENCIES.length;i++) {
      const diff = Math.abs(freq - BASE_FREQUENCIES[i]);
      if (diff < min && diff < FREQUENCY_TOLERANCE) { min = diff; idx = i; }
    }
    return idx !== -1 ? idx : null;
  }

  function charToBinary(c) { return c.charCodeAt(0); }
  function binaryToChar(b) { return String.fromCharCode(b); }

  async function encodeText(text, ctx) {
    await ensureAudioContextReady(ctx);
    const checksum = calculateChecksum(text);
    const msg = `${text}#${checksum}`;
    log('encoding', msg);
    await playStartSignature(ctx);
    const bytes = Array.from(msg).map(charToBinary);
    for (let byte of bytes) {
      const high = (byte >> 6) & 0x7;
      const mid = (byte >> 3) & 0x7;
      const low = byte & 0x7;
      await playTone(binaryToFrequency(high), TONE_DURATION, VOLUME, ctx);
      await playSyncTone(ctx);
      await playTone(binaryToFrequency(mid), TONE_DURATION, VOLUME, ctx);
      await playSyncTone(ctx);
      await playTone(binaryToFrequency(low), TONE_DURATION, VOLUME, ctx);
    }
    await playEndSignature(ctx);
  }

  function decodeAudio(freqData, sampleRate) {
    const binWidth = sampleRate / (freqData.length * 2);
    let maxBin = 0, maxVal = 0;
    for (let i=0;i<freqData.length;i++) {
      if (freqData[i] > maxVal) { maxVal = freqData[i]; maxBin = i; }
    }
    if (maxVal < SIGNAL_THRESHOLD) return null;
    const freq = maxBin * binWidth;

    const now = Date.now();

    if (!isReceivingMessage && Math.abs(freq - START_FREQUENCY) < FREQUENCY_TOLERANCE) {
      if (now - lastSignatureTime > 500) {
        isReceivingMessage = true;
        messageBuffer = '';
        signatureCounter = 0;
        lastSignatureTime = now;
      }
      return null;
    }

    if (isReceivingMessage && Math.abs(freq - END_FREQUENCY) < FREQUENCY_TOLERANCE) {
      signatureCounter++;
      if (signatureCounter >= 2) {
        isReceivingMessage = false;
        lastSignatureTime = now;
        if (!messageBuffer.length) return null;
        const bytes = [];
        let cur = 0, pos = 0;
        for (const bit of messageBuffer) {
          cur = (cur << 3) | parseInt(bit);
          pos += 3;
          if (pos >= 8) { bytes.push(cur & 0xFF); cur = 0; pos = 0; }
        }
        let decoded = bytes.map(binaryToChar).join('');
        const idx = decoded.lastIndexOf('#');
        if (idx !== -1) {
          const text = decoded.slice(0, idx);
          const cs = decoded.slice(idx+1);
          if (isChecksumValid(text, cs)) return text;
          return `[RECOVERED] ${text}`;
        }
        return null;
      }
      return null;
    }

    if (isReceivingMessage && Math.abs(freq - END_FREQUENCY) >= FREQUENCY_TOLERANCE) {
      signatureCounter = 0;
    }

    if (isReceivingMessage) {
      if (Math.abs(freq - SYNC_FREQUENCY) < FREQUENCY_TOLERANCE) return null;
      const bin = frequencyToBinary(freq);
      if (bin !== null) { messageBuffer += bin.toString(); }
    }
    return null;
  }

  function calculateChecksum(text) {
    let sum = 0; for (let ch of text) sum = (sum + ch.charCodeAt(0)) % 256;
    return sum.toString(16).padStart(2, '0');
  }
  function isChecksumValid(text, cs) { return calculateChecksum(text) === cs.toLowerCase(); }

  return { encodeText, decodeAudio, ensureAudioContextReady, resetDecoder: () => {messageBuffer='';isReceivingMessage=false;signatureCounter=0;} };
})();

window.ChirpCodec = ChirpCodec;
