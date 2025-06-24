import { useEffect, useState } from "react";

export default function RunicPulse() {
  const [depth, setDepth] = useState(0);

  useEffect(() => {
    const style = document.createElement("style");
    style.textContent = `
      body {
        background:
          radial-gradient(circle at center, #111 0%, #000 80%),
          repeating-linear-gradient(
            0deg,
            rgba(0, 255, 255, 0.1) 0px,
            rgba(0, 255, 255, 0.1) 2px,
            transparent 2px,
            transparent 10px
          ),
          repeating-linear-gradient(
            90deg,
            rgba(0, 255, 255, 0.1) 0px,
            rgba(0, 255, 255, 0.1) 2px,
            transparent 2px,
            transparent 10px
          );
      }

      @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
      }

      @keyframes glow {
        0% { text-shadow: 0 0 4px #0ff; }
        50% { text-shadow: 0 0 12px #0ff; }
        100% { text-shadow: 0 0 4px #0ff; }
      }

      .rune {
        display: inline-block;
        font-size: 4rem;
        animation: spin 6s linear infinite, glow 2s ease-in-out infinite;
        cursor: pointer;
        user-select: none;
      }

      .depth {
        margin-top: 0.5rem;
        color: #0ff;
        font-family: monospace;
        text-align: center;
      }
    `;
    document.head.appendChild(style);
    return () => {
      document.head.removeChild(style);
    };
  }, []);

  const handleClick = () => {
    setDepth((d) => d + 1);
  };

  return (
    <div style={{ textAlign: "center", paddingTop: "2rem" }} onClick={handleClick}>
      <div className="rune">⌖</div>
      <div className="depth">Fractal Depth: {depth}</div>
    </div>
  );
}
