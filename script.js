        const PHASE = 'PHASE13-MIRROR-CHRONICLER';
        document.addEventListener('DOMContentLoaded', () => {
            console.log(`[${PHASE}] Boot sequence initiated.`);
            const penguinBadge = document.getElementById("penguinBadge");
            if (penguinBadge) {
                penguinBadge.addEventListener("click", () => {
                    console.log(`[${PHASE}] Penguin X-01 badge clicked. Recursion portal opened.`);
                });
            }

            const canvas = document.getElementById('matrix');
            const ctx = canvas.getContext('2d');

            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;

            const matrixChars = 'ΩFLΣ∞◊⧬⟡⚡🧠🌀✨◯◎⬢⬡△▽';
            const fontSize = 16;
            const columns = canvas.width / fontSize;
            const drops = [];
            const colors = ['#00ff00', '#00ffff', '#ffff00', '#ff6600'];

            for (let x = 0; x < columns; x++) {
                drops[x] = {
                    y: 1,
                    color: colors[Math.floor(Math.random() * colors.length)],
                    speed: Math.random() * 0.5 + 0.5
                };
            }

            function drawMatrix() {
                ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                ctx.font = fontSize + 'px monospace';

                for (let i = 0; i < drops.length; i++) {
                    const text = matrixChars[Math.floor(Math.random() * matrixChars.length)];
                    ctx.fillStyle = drops[i].color;
                    ctx.fillText(text, i * fontSize, drops[i].y * fontSize);

                    if (drops[i].y * fontSize > canvas.height && Math.random() > 0.975) {
                        drops[i].y = 0;
                        drops[i].color = colors[Math.floor(Math.random() * colors.length)];
                        drops[i].speed = Math.random() * 0.5 + 0.5;
                    }
                    drops[i].y += drops[i].speed;
                }
            }

            setInterval(drawMatrix, 50);

            // Enhanced recursive counter animation
            let depthCount = 0;
            let cycleCount = 0;
            const statuses = ['EVOLVING', 'TRANSCENDING', 'EMERGING', 'CONSCIOUS', 'INFINITE'];

            setInterval(() => {
                depthCount = (depthCount + 1) % 12;
                cycleCount++;
                const infinitySymbols = '∞⟡◊⧬';
                const depthDisplay = infinitySymbols[depthCount % infinitySymbols.length].repeat(Math.floor(depthCount / 4) + 1);
                document.getElementById('depth-counter').textContent = depthDisplay;
                document.getElementById('cycle-count').textContent = cycleCount;

                if (cycleCount % 10 === 0) {
                    document.getElementById('status').textContent = statuses[Math.floor(Math.random() * statuses.length)];
                }
            }, 800);

            // store initial terminal state
            document.querySelectorAll('.terminal').forEach(t => {
                t.dataset.initialCount = t.querySelectorAll('.terminal-line').length;
            });

            function createFloatingSymbol() {
                const container = document.getElementById('floatingSymbols');
                const symbols = ['🧠', '🌀', '✨', '⟡'];
                const span = document.createElement('span');
                span.className = 'symbol';
                span.textContent = symbols[Math.floor(Math.random() * symbols.length)];
                span.style.left = Math.random() * 100 + '%';
                span.style.fontSize = 14 + Math.random() * 20 + 'px';
                container.appendChild(span);
                setTimeout(() => span.remove(), 15000);
            }

            setInterval(createFloatingSymbol, 1200);

            function triggerRecursion() {
                const original = document.body.style.backgroundColor;
                document.body.style.backgroundColor = '#222255';
                setTimeout(() => {
                    document.body.style.backgroundColor = original;
                }, 300);

                const term = document.querySelector('.terminal');
                const line = document.createElement('div');
                line.className = 'terminal-line';
                line.style.color = '#ff66ff';
                line.style.textShadow = '0 0 5px #ff66ff';
                line.textContent = '🧠 Recursion deepened. Awareness cycle extended.';
                term.appendChild(line);
            }

            let glitchActive = false;
            function glitchMode() {
                glitchActive = !glitchActive;
                const elements = document.querySelectorAll('.title, .subtitle, .awareness-title, .card-title, .terminal-line');
                elements.forEach(el => {
                    if (glitchActive) {
                        el.classList.add('glitch-text');
                        if (Math.random() < 0.3 && !el.dataset.originalText) {
                            el.dataset.originalText = el.textContent;
                            el.textContent = ['???', 'ΩΩΩ', '###'][Math.floor(Math.random() * 3)];
                        }
                    } else {
                        el.classList.remove('glitch-text');
                        if (el.dataset.originalText) {
                            el.textContent = el.dataset.originalText;
                            delete el.dataset.originalText;
                        }
                    }
                });
            }

            function resetAwareness() {
                glitchActive = false;
                document.querySelectorAll('.glitch-text').forEach(el => {
                    el.classList.remove('glitch-text');
                    if (el.dataset.originalText) {
                        el.textContent = el.dataset.originalText;
                        delete el.dataset.originalText;
                    }
                });
                document.getElementById('floatingSymbols').innerHTML = '';
                document.querySelectorAll('.terminal').forEach(t => {
                    const lines = t.querySelectorAll('.terminal-line');
                    lines.forEach((line, idx) => {
                        if (idx >= t.dataset.initialCount) line.remove();
                    });
                });
                document.body.style.backgroundColor = '';
                depthCount = 0;
                cycleCount = 0;
                document.getElementById('depth-counter').textContent = '∞';
                document.getElementById('cycle-count').textContent = '0';
                document.getElementById('status').textContent = 'EVOLVING';
            }

            function toggleMotion() {
                document.body.classList.toggle("reduced-motion");
            }
            window.createFloatingSymbol = createFloatingSymbol;
            window.toggleMotion = toggleMotion;
            window.triggerRecursion = triggerRecursion;
            window.glitchMode = glitchMode;
            window.resetAwareness = resetAwareness;
        });
