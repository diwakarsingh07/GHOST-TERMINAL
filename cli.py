"""
HauntShell CLI: The Possessed Terminal for Command-Line Purists
"""

import sys
from pathlib import Path

# Fix Windows console encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from ghost_engine import GhostEngine, SEANCE_SPIRITS

console = Console()

def run_cli():
    console.print(Panel.fit(
        "[bold green]HAUNTSHELL[/bold green] - [purple]Ghost in the Machine[/purple]\n"
        "[dim]Día de los Muertos & Halloween AI Terminal • Hacktoberfest 2026[/dim]",
        border_style="purple"
    ))

    engine = GhostEngine()
    console.print("[dim green]Spectral connection established. Type commands or 'seance' to commune.[/dim green]")
    console.print("[dim]Commands: ls, git, rm, npm, ping, sudo, seance, exit[/dim]\n")

    while True:
        try:
            cmd = Prompt.ask("[bold green]haunt@underworld:~$[/bold green]").strip()
            if not cmd:
                continue

            if cmd.lower() in {"exit", "quit"}:
                console.print("[italic purple]>>> You try to exit, but the ghost whispers: 'There is no escape from the loop.'[/italic purple]")
                break

            if cmd.lower() == "clear":
                console.clear()
                continue

            if cmd.lower() == "seance":
                run_cli_seance(engine)
                continue

            # Process command with ghost engine
            res = engine.whisper_command(cmd)
            console.print(f"[bold purple]>>> [GHOST WHISPER]:[/bold purple] [italic]{res['whisper']}[/italic]")
            console.print(f"    [dim](Provider: {res['provider']} | Ectoplasm: {res['ectoplasm']}%) [/dim]\n")

        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]The terminal sleeps... for now.[/dim]")
            break

def run_cli_seance(engine: GhostEngine):
    console.print("\n[bold yellow]=== DIGITAL SEANCE ALTAR ===[/bold yellow]")
    console.print("Choose a spirit to awaken:")
    keys = list(SEANCE_SPIRITS.keys())
    for idx, k in enumerate(keys, 1):
        sp = SEANCE_SPIRITS[k]
        console.print(f"  [{idx}] {sp['name']}")

    choice = Prompt.ask("Select spirit (1-5)", default="1")
    try:
        sp_id = keys[int(choice) - 1]
    except Exception:
        sp_id = "flash"

    sp = SEANCE_SPIRITS[sp_id]
    console.print(f"\n[bold yellow]Channeling {sp['name']}...[/bold yellow]")
    msg = Prompt.ask("Whisper your question into the void")
    if msg:
        res = engine.conduct_seance(sp_id, msg)
        console.print(f"\n[italic yellow]\"{res['reply']}\"[/italic yellow]")
        console.print(f"[dim](Channeled via: {res['provider']})[/dim]\n")

if __name__ == "__main__":
    run_cli()
