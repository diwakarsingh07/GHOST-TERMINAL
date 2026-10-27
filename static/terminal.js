// HauntShell Terminal & Audio Logic (with Real Spoken Ghost Whisper Voice)

let audioCtx = null;
let isAudioPlaying = false;
let osc1, osc2, gainNode, filterNode;
let selectedSpiritId = "flash";

document.addEventListener("DOMContentLoaded", () => {
    loadSpirits();
    const input = document.getElementById("terminal-input");
    if (input) {
        input.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
                handleCommandSubmit();
            }
        });
    }
});

// -------------------------------------------------------------
// Real Spoken Ghost Whisper (Speech Synthesis Web API)
// -------------------------------------------------------------
function speakGhostWhisper(text) {
    if (!('speechSynthesis' in window)) return;
    try {
        window.speechSynthesis.cancel(); // Stop previous voice
        const cleanText = text.replace(/[*#`_]/g, ""); // strip markdown
        const utterance = new SpeechSynthesisUtterance(cleanText);

        // Creepy, slow, deep pitch whisper settings
        utterance.pitch = 0.55; 
        utterance.rate = 0.82;
        utterance.volume = 0.40; // comfortable, earbud-safe level

        // Try selecting an English whisper/natural voice if available
        const voices = window.speechSynthesis.getVoices();
        const preferredVoice = voices.find(v => v.lang.startsWith("en") && (v.name.includes("Natural") || v.name.includes("David") || v.name.includes("Google")));
        if (preferredVoice) {
            utterance.voice = preferredVoice;
        }

        window.speechSynthesis.speak(utterance);
    } catch (e) {
        console.warn("Speech synthesis error", e);
    }
}

// -------------------------------------------------------------
// Gentle, Earbud-Safe Ambient Soundscape (Warm Low Drone, No Harsh Highs)
// -------------------------------------------------------------
function toggleSpookyAudio() {
    if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }

    if (isAudioPlaying) {
        stopSpookyAudio();
    } else {
        startSpookyAudio();
    }
}

function startSpookyAudio() {
    if (!audioCtx) return;
    if (audioCtx.state === "suspended") {
        audioCtx.resume();
    }

    // Master volume set to gentle, soft 0.025 for earbud comfort
    gainNode = audioCtx.createGain();
    gainNode.gain.setValueAtTime(0.025, audioCtx.currentTime);

    // Warm Low-Pass Filter: Cuts off all harsh highs above 130 Hz (smooth & comfortable)
    filterNode = audioCtx.createBiquadFilter();
    filterNode.type = "lowpass";
    filterNode.frequency.setValueAtTime(130, audioCtx.currentTime);
    filterNode.Q.setValueAtTime(1.0, audioCtx.currentTime);

    filterNode.connect(gainNode);
    gainNode.connect(audioCtx.destination);

    // Deep gentle sine drone (46 Hz deep warm bass)
    osc1 = audioCtx.createOscillator();
    osc1.type = "sine";
    osc1.frequency.setValueAtTime(46, audioCtx.currentTime);

    // Very subtle low triangle drone for warm texture
    osc2 = audioCtx.createOscillator();
    osc2.type = "triangle";
    osc2.frequency.setValueAtTime(68, audioCtx.currentTime);

    // Soft, slow breathing modulation
    const lfo = audioCtx.createOscillator();
    lfo.frequency.setValueAtTime(0.1, audioCtx.currentTime);
    const lfoGain = audioCtx.createGain();
    lfoGain.gain.setValueAtTime(1.2, audioCtx.currentTime);
    lfo.connect(lfoGain);
    lfoGain.connect(osc1.frequency);
    lfo.start();

    osc1.connect(filterNode);
    osc2.connect(filterNode);
    osc1.start();
    osc2.start();

    isAudioPlaying = true;
    const label = document.getElementById("audio-label");
    const icon = document.getElementById("audio-icon");
    if (label) label.textContent = "Ambient Drone: ON 🎧";
    if (icon) icon.className = "fa-solid fa-headphones text-emerald-400";
}

function stopSpookyAudio() {
    if (osc1) {
        try { osc1.stop(); } catch(e){}
    }
    if (osc2) {
        try { osc2.stop(); } catch(e){}
    }
    isAudioPlaying = false;
    const label = document.getElementById("audio-label");
    const icon = document.getElementById("audio-icon");
    if (label) label.textContent = "Ambient Drone: OFF";
    if (icon) icon.className = "fa-solid fa-volume-xmark";
}

// -------------------------------------------------------------
// Terminal Command Handlers
// -------------------------------------------------------------
function runSampleCommand(cmd) {
    const input = document.getElementById("terminal-input");
    if (input) {
        input.value = cmd;
        handleCommandSubmit();
    }
}

async function handleCommandSubmit() {
    const input = document.getElementById("terminal-input");
    const cmd = input.value.trim();
    if (!cmd) return;

    input.value = "";
    appendTerminalLine(`haunt@underworld:~$ ${cmd}`, "text-emerald-300 font-bold");

    const lower = cmd.toLowerCase();

    // Built-in special commands
    if (lower === "clear") {
        document.getElementById("terminal-history").innerHTML = "";
        return;
    }
    if (lower === "seance" || lower === "ofrenda") {
        openSeanceModal();
        return;
    }
    if (lower === "exit" || lower === "quit") {
        const exitMsg = "You cannot exit. The ghost in the machine never sleeps.";
        appendTerminalLine(`>>> [WHISPER] ${exitMsg}`, "text-purple-400 italic");
        speakGhostWhisper(exitMsg);
        return;
    }
    if (lower === "help") {
        appendTerminalLine("Commands: ls, dir, rm, git, npm, ping, sudo, status, seance, clear", "text-amber-400");
    }

    // Call Ghost in the Machine Whisperer API
    try {
        const res = await fetch("/api/whisper", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ command: cmd })
        });
        const data = await res.json();

        // Update Ectoplasm meter
        const ectoVal = data.ectoplasm || 88;
        const ectoBar = document.getElementById("ectoplasm-bar");
        const ectoValEl = document.getElementById("ectoplasm-val");
        if (ectoBar) ectoBar.style.width = `${ectoVal}%`;
        if (ectoValEl) ectoValEl.textContent = `${ectoVal}%`;

        // Render spectral response
        appendTerminalLine(`>>> [GHOST WHISPER]: ${data.whisper}`, "text-purple-300 italic font-mono");
        appendTerminalLine(`    [SOURCE: ${data.provider} | ECTOPLASM: ${ectoVal}%]`, "text-slate-600 text-xs");

        // Speak the whisper out loud in creepy ghost voice!
        speakGhostWhisper(data.whisper);

    } catch (e) {
        appendTerminalLine(`>>> [STATIC FAULT]: ${e.message}`, "text-rose-500");
    }
}

function appendTerminalLine(text, className = "text-emerald-400") {
    const hist = document.getElementById("terminal-history");
    if (!hist) return;
    const div = document.createElement("div");
    div.className = className;
    div.textContent = text;
    hist.appendChild(div);
    hist.scrollTop = hist.scrollHeight;
}

// -------------------------------------------------------------
// Digital Séance & Día de los Muertos Altar
// -------------------------------------------------------------
async function loadSpirits() {
    try {
        const res = await fetch("/api/spirits");
        const spirits = await res.json();
        const grid = document.getElementById("spirits-grid");
        if (!grid) return;

        grid.innerHTML = "";
        Object.values(spirits).forEach((sp, idx) => {
            const card = document.createElement("div");
            card.id = `spirit-card-${sp.id}`;
            card.className = `p-2.5 rounded border cursor-pointer transition flex items-center gap-2.5 ${
                sp.id === selectedSpiritId 
                    ? "bg-amber-950/80 border-amber-400 text-amber-200" 
                    : "bg-black/60 border-amber-900/60 hover:border-amber-600 text-amber-400"
            }`;
            card.onclick = () => selectSpirit(sp.id);

            card.innerHTML = `
                <span class="text-2xl">${sp.icon}</span>
                <div class="overflow-hidden">
                    <div class="font-bold truncate">${sp.name}</div>
                    <div class="text-[10px] text-amber-500/80 truncate">${sp.description}</div>
                </div>
            `;
            grid.appendChild(card);
        });
    } catch (e) {
        console.warn("Could not load spirits list", e);
    }
}

function selectSpirit(id) {
    selectedSpiritId = id;
    const cards = document.querySelectorAll("[id^='spirit-card-']");
    cards.forEach(c => {
        c.className = "p-2.5 rounded border cursor-pointer transition flex items-center gap-2.5 bg-black/60 border-amber-900/60 hover:border-amber-600 text-amber-400";
    });
    const selected = document.getElementById(`spirit-card-${id}`);
    if (selected) {
        selected.className = "p-2.5 rounded border cursor-pointer transition flex items-center gap-2.5 bg-amber-950/80 border-amber-400 text-amber-200 shadow-lg shadow-amber-900/40";
    }

    const box = document.getElementById("spirit-response-box");
    if (box) box.innerHTML = `<span class="candle-flame">🕯️</span> The veil parts for <strong>${id.toUpperCase()}</strong>. Ask your question below...`;
}

async function sendSeanceMessage() {
    const input = document.getElementById("seance-input");
    const msg = input.value.trim();
    if (!msg) return;

    const box = document.getElementById("spirit-response-box");
    if (box) box.innerHTML = `<i class="fa-solid fa-spinner animate-spin"></i> Communing through the spectral wires...`;
    input.value = "";

    try {
        const res = await fetch("/api/seance", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ spirit_id: selectedSpiritId, message: msg })
        });
        const data = await res.json();
        if (box) {
            box.innerHTML = `
                <div class="space-y-1">
                    <div class="text-xs text-amber-500 font-bold">${data.icon} ${data.spirit_name} says:</div>
                    <div class="text-amber-200">"${data.reply}"</div>
                    <div class="text-[10px] text-amber-700">Channeled via: ${data.provider}</div>
                </div>
            `;
        }

        // Speak the spirit's answer out loud
        speakGhostWhisper(data.reply);

    } catch (e) {
        if (box) box.innerHTML = `<span class="text-rose-400">The connection to the spectral realm severed: ${e.message}</span>`;
    }
}

function openSeanceModal() {
    const modal = document.getElementById("seance-modal");
    if (modal) modal.classList.remove("hidden");
    const seanceInput = document.getElementById("seance-input");
    if (seanceInput) seanceInput.focus();
}

function closeSeanceModal() {
    const modal = document.getElementById("seance-modal");
    if (modal) modal.classList.add("hidden");
}
