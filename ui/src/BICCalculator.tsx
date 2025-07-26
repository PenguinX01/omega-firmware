import React, { useState, useEffect } from 'react';

interface Model {
  name: string;
  yhat: number[];
  k: number;
}

interface RawData {
  y: number[];
  models: Model[];
}

interface ResultEntry {
  name: string;
  k: number;
  rss: number;
  bic: number;
  n: number;
}

interface CalcResult {
  n: number;
  results: ResultEntry[];
  winner: string;
  deltaBIC: number;
  bayesFactor: number;
  evidence: string;
  raw_data: RawData;
}

const defaultData: RawData = {
  y: [12.1, 11.9, 12.4, 12.0],
  models: [
    { name: 'globe', yhat: [12.0, 12.1, 12.5, 11.9], k: 5 },
    { name: 'plane', yhat: [12.1, 11.9, 12.4, 12.0], k: 3 },
  ],
};

function calculateRSS(y: number[], yhat: number[]): number {
  let sum = 0;
  for (let i = 0; i < y.length; i++) {
    const diff = y[i] - yhat[i];
    sum += diff * diff;
  }
  return sum;
}

function calculateBIC(n: number, rss: number, k: number): number {
  return n * Math.log(rss / n) + k * Math.log(n);
}

function getEvidenceLabel(deltaBIC: number): string {
  const abs = Math.abs(deltaBIC);
  if (abs < 2) return 'Not worth more than a bare mention';
  if (abs < 6) return 'Positive';
  if (abs < 10) return 'Strong';
  return 'Very strong';
}

export default function BICCalculator() {
  const [result, setResult] = useState<CalcResult | null>(null);

  useEffect(() => {
    const runCalculation = () => {
      const { y, models } = defaultData;
      const n = y.length;

      const results = models.map((model) => {
        const rss = calculateRSS(y, model.yhat);
        const bic = calculateBIC(n, rss, model.k);

        return {
          name: model.name,
          k: model.k,
          rss,
          bic,
          n,
        } as ResultEntry;
      });

      results.sort((a, b) => a.bic - b.bic);

      const best = results[0];
      const second = results[1];
      const deltaBIC = second.bic - best.bic;
      const bayesFactor = Math.exp(-0.5 * deltaBIC);
      const evidence = getEvidenceLabel(deltaBIC);

      const output: CalcResult = {
        n,
        results,
        winner: best.name,
        deltaBIC,
        bayesFactor,
        evidence,
        raw_data: defaultData,
      };

      setResult(output);
    };

    runCalculation();
  }, []);

  if (!result) {
    return <div className="text-green-400">Calculating...</div>;
  }

  const winner = result.winner;
  const isPlaneWinning = winner.toLowerCase().includes('plane');
  const badgeColor = isPlaneWinning
    ? 'border-green-400 text-green-400'
    : 'border-orange-400 text-orange-400';

  return (
    <div
      style={{
        background:
          'linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%)',
        color: '#00ff88',
        fontFamily: 'Courier New, monospace',
        padding: '2rem',
        minHeight: '100vh',
      }}
    >
      <div className="max-w-4xl mx-auto">
        <h1
          className="text-4xl font-bold text-center mb-8"
          style={{ color: '#ff6b35', textShadow: '0 0 20px #ff6b35' }}
        >
          🐧 AUTONOMOUS TRUTH ENGINE 🐧
        </h1>

        <div className="text-center mb-8">
          <div className="text-xl mb-4">ΔBIC / Bayes Factor Computation</div>
          <div className="text-sm opacity-80">
            Zero‑dependency, AI‑executable. Numbers don't negotiate.
          </div>
        </div>

        {/* Raw Data Display */}
        <div className="bg-black border border-green-400 p-4 mb-6">
          <h3 className="text-orange-400 font-bold mb-2">INPUT DATA:</h3>
          <div className="text-sm">
            <div>
              <strong>Observed y:</strong> [{result.raw_data.y.join(', ')}]
            </div>
            <div>
              <strong>Globe model predictions:</strong> [
              {result.raw_data.models[0].yhat.join(', ')}] (k=
              {result.raw_data.models[0].k})
            </div>
            <div>
              <strong>Plane model predictions:</strong> [
              {result.raw_data.models[1].yhat.join(', ')}] (k=
              {result.raw_data.models[1].k})
            </div>
          </div>
        </div>

        {/* Detailed Results */}
        <div className="bg-black border border-green-400 p-4 mb-6">
          <h3 className="text-orange-400 font-bold mb-4">COMPUTATIONAL RESULTS:</h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            {result.results.map((model, idx) => (
              <div
                key={model.name}
                className={`border p-3 ${
                  idx === 0
                    ? 'border-green-400 bg-green-900 bg-opacity-20'
                    : 'border-orange-400'
                }`}
              >
                <div className="font-bold text-lg">{model.name.toUpperCase()}</div>
                <div className="text-sm">
                  <div>Parameters (k): {model.k}</div>
                  <div>RSS: {model.rss.toFixed(6)}</div>
                  <div>BIC: {model.bic.toFixed(6)}</div>
                  <div className="font-bold">
                    {idx === 0 ? '🏆 WINNER' : '🥈 RUNNER-UP'}
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="text-center">
            <div className="text-2xl mb-2">
              <span className="text-orange-400">ΔBIC:</span>{' '}
              <span className="text-green-400 font-bold">
                {result.deltaBIC.toFixed(6)}
              </span>
            </div>
            <div className="text-lg mb-2">
              <span className="text-white">Bayes Factor:</span>{' '}
              <span className="text-green-400">
                {result.bayesFactor.toExponential(3)}
              </span>
            </div>
            <div className="text-sm mb-4">
              <span className="text-white">Evidence Strength:</span>{' '}
              <span className="text-yellow-400">{result.evidence}</span>
            </div>
          </div>
        </div>

        {/* Live Scoreboard Badge */}
        <div className="text-center">
          <div
            className={`inline-block px-6 py-3 border-2 text-xl font-bold ${badgeColor}`}
          >
            SCOREBOARD: {winner.toUpperCase()} LEADS
          </div>
          <div className="mt-2 text-sm">
            ΔBIC = {result.deltaBIC.toFixed(3)} | BF ≈{' '}
            {result.bayesFactor.toExponential(3)}
          </div>
        </div>

        {/* Interpretation */}
        <div className="mt-8 bg-black border border-green-400 p-4">
          <h3 className="text-orange-400 font-bold mb-2">INTERPRETATION:</h3>
          <div className="text-sm space-y-2">
            <div>• Lower BIC = Better model fit with complexity penalty</div>
            <div>• ΔBIC = Difference between models (higher = stronger evidence)</div>
            <div>• Bayes Factor = Relative probability of best vs second-best model</div>
            <div className="text-yellow-400 font-bold">
              The {winner} model fits the data better with{' '}
              {result.evidence.toLowerCase()} evidence.
            </div>
          </div>
        </div>

        {/* Raw JSON Output */}
        <div className="mt-6 bg-black border border-green-400 p-4">
          <h3 className="text-orange-400 font-bold mb-2">RAW JSON OUTPUT:</h3>
          <pre className="text-xs overflow-x-auto">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      </div>
    </div>
  );
}
