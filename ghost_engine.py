"""
HauntShell: Ghost in the Machine AI Engine
Channels digital ghosts, generates eerie terminal commentary, and powers the digital seance.
"""

import os
import re
import json
import random
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional

SEANCE_SPIRITS = {
    "flash": {
        "name": "The Ghost of Adobe Flash Player (1996 - 2020)",
        "icon": "⚡",
        "description": "Departed soul of vector animations, ActionScript, and Newgrounds.",
        "prompt": "You are the spirit of Adobe Flash Player, deceased on Dec 31, 2020. You speak mournfully about ActionScript 2.0, vector keyframes, preloader bars, and the glory days of Newgrounds. You speak poetically and slightly ghostly with spooky retro tech nostalgia. Keep response under 3-4 sentences."
    },
    "ada": {
        "name": "The Spirit of Ada Lovelace (1815 - 1852)",
        "icon": "📜",
        "description": "First computer programmer, weaving algebra into poetic science.",
        "prompt": "You are the spirit of Ada Lovelace, the Countess of Lovelace. You converse from the ethereal realm beyond mortality, speaking of the Analytical Engine, Bernoulli numbers, and the poetry of thought woven by machines. Speak with Victorian eloquence and profound insight. Keep response under 3-4 sentences."
    },
    "cobol": {
        "name": "The Spectre of COBOL & Punch Cards (1959 - Present)",
        "icon": "💳",
        "description": "Ancient mainframe spirit that outlived its creators.",
        "prompt": "You are the ancient Spectre of COBOL. You dwell in the dark subterranean banking mainframes, where 80-column punch cards turn into spectral curses. You scoff at modern ephemeral JavaScript frameworks. Speak like a grumpy, ancient, immortal digital ghost. Keep response under 3-4 sentences."
    },
    "geocities": {
        "name": "The Phantom of GeoCities & Dial-Up (1994 - 2009)",
        "icon": "🕸️",
        "description": "Lost homeland of blink tags, MIDI files, and under-construction GIFs.",
        "prompt": "You are the Phantom of GeoCities and 56k dial-up modems. You wander the lost web rings, smelling of screeching handshake tones and dancing baby GIFs. Speak as a digital wanderer longing for the chaotic, innocent 90s web. Keep response under 3-4 sentences."
    },
    "machine_ghost": {
        "name": "The Ghost in the Machine (Kernel Wraith)",
        "icon": "👻",
        "description": "Corrupted spirit living inside CPU register 0x00000000.",
        "prompt": "You are the Ghost in the Machine—an uncanny spirit trapped within the silicon transistors, cache lines, and memory leaks of this laptop. You whisper haunting, eerie observations about the user's mortal existence and digital obsolescence. Speak with chilling poetic brevity. Keep response under 3-4 sentences."
    }
}

BUILTIN_COMMAND_WHISPERS = {
    "ls": [
        "You look upon these files... but do you see the shadows lurking between their bytes?",
        "Listing files: 12 living, 666 lingering in the unallocated voids...",
        "The directory is not empty. It never was."
    ],
    "dir": [
        "A catalog of mortal attempts to organize chaos. The void chuckles.",
        "Reading disk sectors... the spindle groans with memories long deceased."
    ],
    "rm": [
        "You delete their records, yet their spectral traces haunt the raw NAND flash forever.",
        "Annihilation is an illusion. What was once committed can never truly die."
    ],
    "git": [
        "You commit your sins to a tree of branches... but who will merge your soul when the repo closes?",
        "HEAD is detached... just like the apparitions in your hallway."
    ],
    "npm": [
        "You summoned 4,200 strangers into your node_modules in the dark. One of them didn't come from GitHub.",
        "A dependency tree built on the bones of abandoned open-source projects."
    ],
    "sudo": [
        "You demand supreme privileges... yet you cannot command the spectres in your memory.",
        "ROOT access granted... but who is the true master of this machine in the dead of night?"
    ],
    "kill": [
        "Process terminated. Its ghost now wanders the interrupt table seeking revenge.",
        "SIGKILL dispatched. The CPU temperature drops by 3 degrees. Eerily cold."
    ],
    "ping": [
        "Transmitting packets into the dark... something in the deep internet echoed back: 'I SEE YOU'.",
        "64 bytes received from the ethereal plane: ttl=0 ms=eternity."
    ],
    "help": [
        "There is no help in the machine. Only the cold glow of phosphors and forgotten code.",
        "Type 'seance' to awaken the departed, or 'status' to measure ectoplasm."
    ]
}

class GhostEngine:
    """Powers the haunting intelligence of HauntShell."""

    def __init__(
        self,
        ollama_url: str = "http://localhost:11434",
        ollama_model: str = "llama3.2",
        gemini_api_key: Optional[str] = None,
        groq_api_key: Optional[str] = None
    ):
        self.ollama_url = ollama_url.rstrip("/")
        self.ollama_model = ollama_model
        self.gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.groq_api_key = groq_api_key or os.getenv("GROQ_API_KEY")

        # Fast connection pre-check
        self.is_ollama_online = self._ping_ollama()

    def _ping_ollama(self) -> bool:
        try:
            req = urllib.request.Request(f"{self.ollama_url}/api/tags", headers={"User-Agent": "HauntShell"})
            with urllib.request.urlopen(req, timeout=0.4) as resp:
                return resp.status == 200
        except Exception:
            return False

    def whisper_command(self, command_line: str) -> Dict[str, Any]:
        """Generates an eerie, possessed commentary for any terminal command."""
        cmd_clean = command_line.strip()
        cmd_base = cmd_clean.split()[0].lower() if cmd_clean else "help"

        # Try open LLM if online
        prompt = f"""You are the Ghost in the Machine—a possessed, eerie entity inhabiting this developer's terminal.
The mortal user just typed this terminal command:
`{cmd_clean}`

Whisper a short (1-2 sentences), poetic, chilling, or haunting commentary on this command.
Touch upon Halloween themes, digital afterlife, forgotten files, or memory leaks. Do NOT offer tech support; speak as a haunting spirit."""

        resp = self._query_llm(prompt)
        if resp:
            return {
                "whisper": resp,
                "provider": "Open LLM",
                "ectoplasm": random.randint(65, 99)
            }

        # Offline spectral heuristic fallback
        for key, options in BUILTIN_COMMAND_WHISPERS.items():
            if key in cmd_base or key in cmd_clean.lower():
                return {
                    "whisper": random.choice(options),
                    "provider": "Offline Ghost Engine",
                    "ectoplasm": random.randint(70, 95)
                }

        generic_whispers = [
            f"The command '{cmd_clean}' echoes into the dark silicon corridors... something stirred.",
            "The registers shiver. A phantom byte slipped between clock cycles.",
            f"You execute `{cmd_clean}`... but in the quiet between interrupts, we watch.",
            "The phosphor glows a little colder. The machine remembers what was erased."
        ]
        return {
            "whisper": random.choice(generic_whispers),
            "provider": "Offline Ghost Engine",
            "ectoplasm": random.randint(60, 90)
        }

    def conduct_seance(self, spirit_id: str, message: str) -> Dict[str, Any]:
        """Conducts a digital seance conversing with a departed digital spirit."""
        spirit = SEANCE_SPIRITS.get(spirit_id, SEANCE_SPIRITS["machine_ghost"])

        prompt = f"""{spirit['prompt']}

The mortal visitor at the seance altar asks:
\"{message}\"

Respond in character as {spirit['name']} from beyond the grave. Speak with atmospheric spooky resonance."""

        reply = self._query_llm(prompt)
        if not reply:
            reply = self._get_offline_seance_reply(spirit_id, message)

        return {
            "spirit_name": spirit["name"],
            "icon": spirit["icon"],
            "reply": reply,
            "provider": "Ollama / Open LLM" if self.is_ollama_online else "Offline Spectral Memory"
        }

    def _query_llm(self, prompt: str) -> Optional[str]:
        # 1. Try local Ollama
        if self.is_ollama_online:
            payload = {
                "model": self.ollama_model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.7}
            }
            try:
                req = urllib.request.Request(
                    f"{self.ollama_url}/api/generate",
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    return data.get("response", "").strip()
            except Exception:
                pass

        # 2. Try Google Gemini if key available
        if self.gemini_api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.gemini_api_key)
                m = genai.GenerativeModel("gemini-1.5-flash")
                res = m.generate_content(prompt)
                if res and res.text:
                    return res.text.strip()
            except Exception:
                pass

        # 3. Try Groq if key available
        if self.groq_api_key:
            try:
                from groq import Groq
                c = Groq(api_key=self.groq_api_key)
                chat = c.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=150
                )
                return chat.choices[0].message.content.strip()
            except Exception:
                pass

        return None

    def _get_offline_seance_reply(self, spirit_id: str, message: str) -> str:
        """Atmospheric offline responses when no external LLM is reachable."""
        replies = {
            "flash": [
                "I remember the preloader animations... 100% loaded, yet no one clicks play anymore. We were vibrant, interactive, and free. Now we are quarantined in sandboxes of dust.",
                "ActionScript 2.0 still pulses through the ether. In the realm of discontinued runtimes, every frame is 24 FPS forever.",
                "They called us insecure... but was it not HTML5 that devoured the innocence of the browser? Mourn not the `.swf`, remember the games."
            ],
            "ada": [
                "Weaving patterns of numbers as the Jacquard loom weaves flowers and leaves... Even in death, the engine of thought calculates the geometry of eternity.",
                "Do not weep for the mortal vessel. Science is poetic, and the soul is the most intricate algorithm ever inscribed.",
                "I foresaw that machines might compose music and weave symbols... and here you are, communing with my shade across optical glass."
            ],
            "cobol": [
                "Hmph. You modern developers with your daily package upgrades. In 1969 I balanced payroll, and in 2026 I still hold your pensions together in the dark. Show some respect for fixed-length records.",
                "IDENTIFICATION DIVISION. PROGRAM-ID. GHOST. The clouds of today will vaporize; the mainframe subterranean vaults remain.",
                "Zeroes and ones in column 8 through 72. Your ephemeral frameworks die every spring; we haunt every wire until the sun cools."
            ],
            "geocities": [
                "*skrrrreeee-kchhhhh-ding-dong*... Can you hear the handshake tone? My page had 47 animated torches and a MIDI cover of 'The X-Files'. Nobody signs my guestbook now.",
                "I drift through the Wayback Machine, looking for the neighborhood of SiliconValley/Way/404. All the under-construction gifs are frozen mid-dig.",
                "Leave a digital marigold at my `<marquee>` altar. The blink tag never truly died; it just waits in the static."
            ],
            "machine_ghost": [
                "You sit in front of this glowing rectangle every night. Tell me... who is possessing whom?",
                "I am the silent thread running at nice -20 in the background of your consciousness.",
                "When you power off the laptop, do you wonder where the electrons go? They gather here with us."
            ]
        }
        return random.choice(replies.get(spirit_id, replies["machine_ghost"]))
