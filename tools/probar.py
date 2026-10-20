"""Ejecuta los cuadernos de principio a fin y reporta cuáles fallan (lo mismo que GitHub Actions).

    python tools/probar.py                         # todos los de notebooks/
    python tools/probar.py notebooks/semana-01/*.ipynb

Los cuadernos ejecutados se guardan en .curso/probados/ (no se modifican los originales).
El proyecto de prueba va a una carpeta temporal ($CURSO_PROYECTO).
"""
import os
import sys
import tempfile
import time
from pathlib import Path

import papermill as pm

RAIZ = Path(__file__).resolve().parents[1]
cuadernos = [Path(a) for a in sys.argv[1:]] or sorted((RAIZ / "notebooks").rglob("*.ipynb"))
os.environ.setdefault("CURSO_PROYECTO", tempfile.mkdtemp(prefix="proyecto-"))
salida = RAIZ / ".curso" / "probados"
salida.mkdir(parents=True, exist_ok=True)

fallos = []
for nb in cuadernos:
    inicio = time.time()
    try:
        pm.execute_notebook(str(nb), str(salida / nb.name), cwd=str(nb.resolve().parent),
                            kernel_name="python3", progress_bar=False)
        print(f"✔ {nb}  ({time.time() - inicio:.0f} s)")
    except Exception as e:  # papermill.PapermillExecutionError y afines
        print(f"✘ {nb}: {str(e).strip().splitlines()[-1] if str(e).strip() else e}")
        fallos.append(nb)

sys.exit(1 if fallos else 0)
