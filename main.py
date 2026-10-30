from __future__ import annotations

import argparse
import ctypes
import json
import logging
import os
from pathlib import Path

from mako import MakoCore
from mako.discord_service import DiscordService
from mako.shell_server import run_shell_server
from mako.ui import DesktopCompanion


ROOT = Path(os.environ.get("STELLA_APP_ROOT", Path(__file__).resolve().parent)).expanduser().resolve()
PROFILE = Path(os.environ.get("STELLA_PROFILE_DIR", ROOT)).expanduser().resolve()
_INSTANCE_MUTEX = None


def acquire_single_instance(name: str = "Local\\MakoV4DesktopCompanion") -> bool:
    """Hold a Windows named mutex for the lifetime of the desktop process."""
    global _INSTANCE_MUTEX
    if os.name != "nt":
        return True
    kernel32 = ctypes.windll.kernel32
    handle = kernel32.CreateMutexW(None, False, name)
    if not handle:
        return False
    if kernel32.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
        kernel32.CloseHandle(handle)
        return False
    _INSTANCE_MUTEX = handle
    return True


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mako V4 desktop companion")
    parser.add_argument(
        "--diagnostics",
        action="store_true",
        help="Print local configuration, model, memory, and asset status without opening the UI.",
    )
    parser.add_argument(
        "--smoke-ui",
        action="store_true",
        help="Create the desktop UI hidden, process one update, and close.",
    )
    parser.add_argument(
        "--electron-shell",
        action="store_true",
        help="Run the local API consumed by Stella's Electron control-panel shell.",
    )
    return parser.parse_args()


def configure_logging() -> None:
    log_directory = PROFILE / "data" / "logs"
    log_directory.mkdir(parents=True, exist_ok=True)
    # This shell may be launched outside the original desktop user's ACL. Keep
    # operational logging beside the data store instead of a stale locked log.
    logging.basicConfig(
        filename=PROFILE / "data" / "stella_runtime.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def main() -> int:
    arguments = parse_arguments()
    configure_logging()
    # Electron must not share the legacy UI mutex, but it still needs its own
    # guard: multiple shell children compete for the microphone and TTS queue.
    if arguments.electron_shell:
        if not acquire_single_instance("Local\\MakoV4ElectronShell"):
            logging.info("Stella Electron shell launch ignored: runtime already running")
            return 0
        return run_shell_server(ROOT)
    if (
        not arguments.diagnostics
        and not arguments.smoke_ui
        and not acquire_single_instance()
    ):
        logging.warning("Mako launch ignored: another desktop instance is already running")
        return 0
    core = MakoCore(ROOT)
    if arguments.diagnostics:
        print(json.dumps(core.diagnostics(), indent=2))
        core.close()
        return 0
    if arguments.smoke_ui:
        app = DesktopCompanion(core, hidden=True)
        app.root.update_idletasks()
        app.root.update()
        app.close()
        return 0

    discord = DiscordService(core, core.config.discord)
    discord.start()
    try:
        logging.info("Desktop UI event loop starting")
        DesktopCompanion(core, discord).run()
        logging.warning("Desktop UI event loop ended")
    finally:
        logging.info("Desktop shutdown cleanup starting")
        discord.stop()
        core.close()
        logging.shutdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
