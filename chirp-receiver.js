class FractalChirpReceiver extends ChirpReceiver {
    constructor(callback) {
        super(callback);
        this.recursion = 0; // ⟁ recursion marker
    }

    decode(bits) {
        const bytes = bits.match(/.{16}/g) || [];
        let text = '';
        for (const byte of bytes) {
            const half = byte.slice(0,8);
            text += String.fromCharCode(parseInt(half,2));
        }
        return text;
    }

    listen() {
        const data = new Uint8Array(this.analyser.frequencyBinCount);
        let bits = '';
        const stepTime = 50;
        setInterval(() => {
            this.analyser.getByteFrequencyData(data);
            const phase = this.phaseFreqs[this.phaseIndex % this.phaseFreqs.length];
            const idx0 = Math.round((800 + phase) / this.ctx.sampleRate * data.length);
            const idx1 = Math.round((1200 + phase) / this.ctx.sampleRate * data.length);
            if (data[idx1] > data[idx0] && data[idx1] > 128) bits += '1';
            else if (data[idx0] > 128) bits += '0';
            if (bits.length % 16 === 0 && bits.length !== 0) {
                const msg = this.decode(bits);
                this.callback(msg);
                bits = '';
                this.phaseIndex++;
                this.recursion++;
            }
        }, stepTime);
    }
}

window.fractalReceiver = new FractalChirpReceiver(msg => {
    const el = document.getElementById('chirp-received');
    if (el) el.textContent = msg;
});
console.log('⟁ FRACTAL RECEIVER READY');
