import os
import http.server
import socketserver
import textwrap

# --- BAGIAN 1: KONTEN FILE GAME (HTML & JS) ---

html_content = textwrap.dedent("""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Py-Web Idle Empire</title>
        <style>
            :root {
                --bg-color: #121212;
                --card-bg: #1e1e1e;
                --primary-color: #00adb5;
                --secondary-color: #ff5722;
                --text-color: #e0e0e0;
                --accent-color: #393e46;
                --border-radius: 12px;
                --transition-speed: 0.2s;
            }

            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: var(--bg-color);
                color: var(--text-color);
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }

            .game-container {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 30px;
                width: 90%;
                max-width: 1000px;
                padding: 20px;
            }

            .dashboard, .shop {
                background-color: var(--card-bg);
                border-radius: var(--border-radius);
                padding: 30px;
                box-shadow: 0 10px 20px rgba(0,0,0,0.4);
            }

            .dashboard {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                position: relative;
            }

            .score-display {
                margin-bottom: 20px;
            }

            .score-label {
                font-size: 1.2rem;
                color: var(--primary-color);
                text-transform: uppercase;
                letter-spacing: 2px;
            }

            .score-value {
                font-size: 3.5rem;
                font-weight: bold;
                margin: 10px 0;
            }

            .stat {
                font-size: 1rem;
                color: #888;
                margin: 5px 0;
            }

            #btn-click {
                background-color: var(--primary-color);
                color: white;
                border: none;
                padding: 20px 40px;
                font-size: 1.5rem;
                font-weight: bold;
                border-radius: 50px;
                cursor: pointer;
                box-shadow: 0 6px 0 #00888f;
                transition: transform 0.05s, box-shadow 0.05s;
                position: relative;
                overflow: hidden;
            }

            #btn-click:active {
                transform: translateY(3px);
                box-shadow: 0 3px 0 #00888f;
            }

            #btn-click::after {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(255, 255, 255, 0.2);
                opacity: 0;
                transition: opacity 0.3s;
                border-radius: 50px;
            }

            #btn-click:hover::after {
                opacity: 1;
            }

            .floating-point {
                position: absolute;
                font-size: 1.5rem;
                color: var(--primary-color);
                font-weight: bold;
                opacity: 1;
                pointer-events: none;
                animation: floatUp 1s ease-out forwards;
            }

            @keyframes floatUp {
                0% { transform: translateY(0); opacity: 1; }
                100% { transform: translateY(-50px); opacity: 0; }
            }

            .shop-title {
                text-align: center;
                color: var(--secondary-color);
                margin-bottom: 25px;
                text-transform: uppercase;
                letter-spacing: 2px;
            }

            .upgrade-list {
                display: flex;
                flex-direction: column;
                gap: 15px;
            }

            .upgrade-item {
                display: grid;
                grid-template-columns: 50px 1fr auto;
                align-items: center;
                gap: 15px;
                background-color: var(--accent-color);
                padding: 15px;
                border-radius: var(--border-radius);
                transition: background-color 0.2s;
            }

            .upgrade-item:hover {
                background-color: #4a5059;
            }

            .upgrade-icon {
                font-size: 2rem;
                text-align: center;
            }

            .upgrade-info h4 {
                margin: 0 0 5px;
            }

            .upgrade-info p {
                margin: 0;
                font-size: 0.9rem;
                color: #bbb;
            }

            .btn-upgrade {
                padding: 10px 20px;
                background-color: #444;
                color: white;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                transition: background-color 0.2s;
            }

            .btn-upgrade:hover:not(:disabled) {
                background-color: var(--secondary-color);
            }

            .btn-upgrade:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }

            @media (max-width: 768px) {
                .game-container {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>

        <div class="game-container">
            <div class="dashboard">
                <div class="score-display">
                    <div class="score-label">Empire Points</div>
                    <div id="score" class="score-value">0</div>
                </div>
                <div class="stat">Poin per Klik: <span id="pps">1</span></div>
                <div class="stat">Poin per Detik: <span id="autops">0</span></div>
                <br>
                <button id="btn-click">MULAILAH KLIK!</button>
            </div>

            <div class="shop">
                <h3 class="shop-title">💎 Empire Upgrades 💎</h3>
                <div class="upgrade-list">
                    
                    <div class="upgrade-item">
                        <div class="upgrade-icon">☝️</div>
                        <div class="upgrade-info">
                            <h4>Kekuatan Klik</h4>
                            <p>Level: <span id="pps-level">0</span> (+1 PPS)</p>
                        }
                        <button id="buy-pps" class="btn-upgrade">Beli (<span id="pps-cost">10</span>)</button>
                    </div>

                    <div class="upgrade-item">
                        <div class="upgrade-icon">🤖</div>
                        <div class="upgrade-info">
                            <h4>Auto-Bot Tipe A</h4>
                            <p>Level: <span id="bot-a-level">0</span> (+1 PPD)</p>
                        }
                        <button id="buy-bot-a" class="btn-upgrade">Beli (<span id="bot-a-cost">25</span>)</button>
                    </div>

                    <div class="upgrade-item">
                        <div class="upgrade-icon">🚀</div>
                        <div class="upgrade-info">
                            <h4>Auto-Bot Tipe B</h4>
                            <p>Level: <span id="bot-b-level">0</span> (+10 PPD)</p>
                        }
                        <button id="buy-bot-b" class="btn-upgrade">Beli (<span id="bot-b-cost">250</span>)</button>
                    </div>
                </div>
            </div>
        </div>

        <script src="script.js"></script>
    </body>
    </html>
""")

js_content = textwrap.dedent("""
    class ClickerGame {
        constructor() {
            this.initialState = {
                score: 0,
                pointsPerClick: 1,
                autoPointsPerSecond: 0,
                levels: {
                    pps: 0,
                    botA: 0,
                    botB: 0
                },
                costs: {
                    pps: 10,
                    botA: 25,
                    botB: 250
                }
            };
            this.state = this.loadGame() || { ...this.initialState, costs: { ...this.initialState.costs }, levels: { ...this.initialState.levels } };
            this.costsUpdateFactor = 1.3;

            this.ui = {
                score: document.getElementById('score'),
                pps: document.getElementById('pps'),
                autops: document.getElementById('autops'),
                btnClick: document.getElementById('btn-click'),
                dashboard: document.querySelector('.dashboard'),
                shopButtons: {
                    pps: document.getElementById('buy-pps'),
                    botA: document.getElementById('buy-bot-a'),
                    botB: document.getElementById('buy-bot-b')
                },
                shopLevels: {
                    pps: document.getElementById('pps-level'),
                    botA: document.getElementById('bot-a-level'),
                    botB: document.getElementById('bot-b-level')
                },
                shopCosts: {
                    pps: document.getElementById('pps-cost'),
                    botA: document.getElementById('bot-a-cost'),
                    botB: document.getElementById('bot-b-cost')
                }
            };

            this.init();
        }

        init() {
            this.ui.btnClick.addEventListener('click', (e) => this.handleClick(e));
            this.ui.shopButtons.pps.addEventListener('click', () => this.buyUpgrade('pps', 1, 'score', 'pointsPerClick'));
            this.ui.shopButtons.botA.addEventListener('click', () => this.buyUpgrade('botA', 1, 'score', 'autoPointsPerSecond'));
            this.ui.shopButtons.botB.addEventListener('click', () => this.buyUpgrade('botB', 10, 'score', 'autoPointsPerSecond'));

            this.startGameLoop();
            this.updateUI();
        }

        handleClick(e) {
            this.state.score += this.state.pointsPerClick;
            this.createFloatingPoint(e);
            this.updateUI();
            this.saveGame();
        }

        buyUpgrade(upgradeId, increment, paymentKey, stateEffectKey) {
            const cost = this.state.costs[upgradeId];
            if (this.state.score >= cost) {
                this.state.score -= cost;
                this.state[stateEffectKey] += increment;
                this.state.levels[upgradeId]++;
                this.state.costs[upgradeId] = Math.floor(cost * this.costsUpdateFactor);
                this.updateUI();
                this.saveGame();
            }
        }

        startGameLoop() {
            setInterval(() => {
                this.state.score += this.state.autoPointsPerSecond / 10;
                this.updateUI();
                this.saveGame();
            }, 100); // Update score every 100ms for smoothness
        }

        updateUI() {
            this.ui.score.innerText = Math.floor(this.state.score);
            this.ui.pps.innerText = this.state.pointsPerClick;
            this.ui.autops.innerText = this.state.autoPointsPerSecond;

            for (const key in this.ui.shopButtons) {
                const cost = this.state.costs[key];
                this.ui.shopLevels[key].innerText = this.state.levels[key];
                this.ui.shopCosts[key].innerText = cost;
                this.ui.shopButtons[key].disabled = this.state.score < cost;
            }
        }

        createFloatingPoint(e) {
            const floating = document.createElement('div');
            floating.classList.add('floating-point');
            floating.innerText = '+' + this.state.pointsPerClick;
            
            const btnRect = this.ui.btnClick.getBoundingClientRect();
            const dashRect = this.ui.dashboard.getBoundingClientRect();
            
            const x = e.clientX - dashRect.left - btnRect.width / 4;
            const y = e.clientY - dashRect.top - 20;

            floating.style.left = x + 'px';
            floating.style.top = y + 'px';
            
            this.ui.dashboard.appendChild(floating);
            
            setTimeout(() => {
                floating.remove();
            }, 1000);
        }

        saveGame() {
            localStorage.setItem('pyWebClickerSave', JSON.stringify(this.state));
        }

        loadGame() {
            const savedState = localStorage.getItem('pyWebClickerSave');
            return savedState ? JSON.parse(savedState) : null;
        }
    }

    const game = new ClickerGame();
""")

# --- BAGIAN 2: LOGIKA PYTHON UNTUK MEMBUAT FILE ---

file_content_map = {
    "index.html": html_content,
    "script.js": js_content,
}

print("🛠️ Sedang membangun file game...")

for filename, content in file_content_map.items():
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Berhasil membuat file: {filename}")
    else:
        print(f"⏩ File {filename} sudah ada, melewati.")

# --- BAGIAN 3: MENJALANKAN LOKAL SERVER ---

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

print(f"🌍 Server lokal aktif!")
print(f"Buka browser kamu dan ketik alamat: http://localhost:{PORT}")
print("Gunakan CTRL+C di terminal ini untuk mematikan server.")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server dihentikan. Sampai jumpa!")
