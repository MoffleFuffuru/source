from __future__ import annotations

import os
import subprocess
import sys
import traceback
from pathlib import Path


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    venv_pythonw = root / ".venv" / "Scripts" / "pythonw.exe"
    if venv_pythonw.exists() and Path(sys.executable).resolve() != venv_pythonw.resolve():
        subprocess.Popen([str(venv_pythonw), str(Path(__file__).resolve())], cwd=str(root))
        raise SystemExit(0)
    from main import main

    try:
        raise SystemExit(main())
    except Exception:
        log_path = Path(__file__).resolve().parent / "data" / "logs" / "crash.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text(traceback.format_exc(), encoding="utf-8")
        raise
