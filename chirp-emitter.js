class FractalChirpEmitter extends ChirpEmitter {
    constructor() {
        super();
        this.recursion = 0; // ⟁ recursion marker
    }

    encodeFractal(text) {
        // Simple fractal encoding: mirror each char's bits
        let bits = '';
        for (const ch of text) {
            const b = ch.charCodeAt(0).toString(2).padStart(8,'0');
            bits += b + b.split('').reverse().join('');
        }
        return bits;
    }

    transmitFractal(text) {
        const bits = this.encodeFractal(text);
        let time = this.ctx.currentTime;
        const phase = this.nextPhase();
        const step = 1 / (phase * 5); // phase locked timing
        for (const bit of bits) {
            const freq = (bit === '1' ? 1200 : 800) + phase;
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.frequency.setValueAtTime(freq, time);
            gain.gain.setValueAtTime(0.25, time);
            osc.connect(gain).connect(this.ctx.destination);
            osc.start(time);
            osc.stop(time + step);
            time += step * 1.2;
        }
        this.recursion++;
    }
}

window.fractalEmitter = new FractalChirpEmitter();
console.log('⟁ FRACTAL EMITTER READY');
