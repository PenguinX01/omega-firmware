class ChirpEmitter {
    constructor() {
        this.ctx = new (window.AudioContext || window.webkitAudioContext)();
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

    transmit(text) {
        const base1 = 1200;
        const base0 = 800;
        let time = this.ctx.currentTime;
        const phase = this.nextPhase();
        for (const char of text) {
            const bits = char.charCodeAt(0).toString(2).padStart(8, '0');
            for (const bit of bits) {
                const freq = (bit === '1' ? base1 : base0) + phase;
                const osc = this.ctx.createOscillator();
                const gain = this.ctx.createGain();
                osc.frequency.setValueAtTime(freq, time);
                osc.type = 'sine';
                gain.gain.setValueAtTime(0.2, time);
                osc.connect(gain).connect(this.ctx.destination);
                osc.start(time);
                osc.stop(time + 0.05);
                time += 0.06;
            }
        }
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
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const source = this.ctx.createMediaStreamSource(stream);
            source.connect(this.analyser);
            this.listen();
        } catch (e) {
            console.error('Chirp receiver failed', e);
        }
    }

    listen() {
        const data = new Uint8Array(this.analyser.frequencyBinCount);
        const decodeInterval = setInterval(() => {
            this.analyser.getByteFrequencyData(data);
            // Placeholder for decoding logic
        }, 50);
    }
}

window.chirpEmitter = new ChirpEmitter();
window.chirpReceiver = new ChirpReceiver(msg => {
    const el = document.getElementById('chirp-received');
    if (el) el.textContent = msg;
});
console.log('⟁ CHIRP PROTOCOL INITIALIZED');
