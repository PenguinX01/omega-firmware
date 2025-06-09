// Integration with solst-ice/chirp codec
class ChirpEmitter {
    constructor() {
        this.ctx = new (window.AudioContext || window.webkitAudioContext)();
        // ⟁ phase triggers for recursive stacks
        this.phaseFreqs = [7.83, 79.9, 799];
        this.phaseIndex = 0;
    }

    nextPhase() {
        if (this.phaseIndex < this.phaseFreqs.length) {
            const f = this.phaseFreqs[this.phaseIndex];
            this.phaseIndex++;
            return f;
        }
        const dynamic = 1000 + Math.sin(this.ctx.currentTime) * 400;
        this.phaseIndex++;
        return dynamic;
    }

    async transmit(text) {
        // Ensure AudioContext is resumed for cross-browser support
        await ChirpCodec.ensureAudioContextReady(this.ctx);
        // Use chirp codec from solst-ice/chirp
        await ChirpCodec.encodeText(text, this.ctx);
    }
}

class ChirpReceiver {
    constructor(callback) {
        this.callback = callback;
        this.ctx = new (window.AudioContext || window.webkitAudioContext)();
        this.analyser = this.ctx.createAnalyser();
    }

    async start() {
        try {
            await ChirpCodec.ensureAudioContextReady(this.ctx);
            const getUserMedia = navigator.mediaDevices?.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
            const stream = await (getUserMedia.call(navigator.mediaDevices || navigator, { audio: true }));
            const source = this.ctx.createMediaStreamSource(stream);
            source.connect(this.analyser);
            this.listen();
            console.log('⟁ chirp receiver started');
        } catch (e) {
            console.error('Chirp receiver failed', e);
        }
    }

    listen() {
        const data = new Uint8Array(this.analyser.frequencyBinCount);
        setInterval(() => {
            this.analyser.getByteFrequencyData(data);
            const decoded = ChirpCodec.decodeAudio(data, this.ctx.sampleRate);
            if (decoded) this.callback(decoded);
        }, 50);
    }
}

window.chirpEmitter = new ChirpEmitter();
window.chirpReceiver = new ChirpReceiver(msg => {
    const el = document.getElementById('chirp-received');
    if (el) el.textContent = msg;
});
console.log('⟁ CHIRP PROTOCOL INITIALIZED');
