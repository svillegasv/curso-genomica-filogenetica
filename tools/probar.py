"""Ejecuta los cuadernos de principio a fin y reporta cuáles fallan (lo mismo que GitHub Actions).

    python tools/probar.py                         # todos los de notebooks/ y proyecto/
    python tools/probar.py notebooks/semana-01/*.ipynb

Las celdas de ejercicio muestran COMPLETE al estudiante; para probarlas se usa la respuesta guardada en su nota
interna (metadata["curso"]["respuesta"]). Una celda con COMPLETE sin respuesta interna se reporta como fallo.
Los cuadernos ejecutados se guardan en .curso/probados/ (no se modifican los originales).
El proyecto de prueba va a una carpeta temporal ($CURSO_PROYECTO).
"""
import os
import sys
import tempfile
import time
from pathlib import Path

import nbformat
import papermill as pm

RAIZ = Path(__file__).resolve().parents[1]
cuadernos = [Path(a) for a in sys.argv[1:]] or sorted(
    nb for carpeta in ("notebooks", "proyecto") for nb in (RAIZ / carpeta).rglob("*.ipynb"))
os.environ.setdefault("CURSO_PROYECTO", tempfile.mkdtemp(prefix="proyecto-"))
os.environ.setdefault("CURSO_EQUIPO", "REL7179B")     # clon de prueba para los cuadernos de proyecto
salida = RAIZ / ".curso" / "probados"
salida.mkdir(parents=True, exist_ok=True)


def con_respuestas(nb_path: Path) -> Path:
    """Copia del cuaderno con cada COMPLETE reemplazado por la respuesta interna de su celda."""
    nb = nbformat.read(nb_path, as_version=4)
    for i, celda in enumerate(nb.cells):
        respuesta = celda.get("metadata", {}).get("curso", {}).get("respuesta")
        if respuesta:
            celda.source = respuesta
        elif celda.cell_type == "code" and "COMPLETE" in celda.source:
            raise ValueError(f"la celda {i} tiene COMPLETE pero no tiene respuesta interna (use nb.ejercicio)")
    destino = salida / "entrada" / nb_path.name
    destino.parent.mkdir(exist_ok=True)
    nbformat.write(nb, destino)
    return destino


fallos = []
for nb in cuadernos:
    inicio = time.time()
    try:
        pm.execute_notebook(str(con_respuestas(nb)), str(salida / nb.name), cwd=str(nb.resolve().parent),
                            kernel_name="python3", progress_bar=False)
        print(f"✔ {nb}  ({time.time() - inicio:.0f} s)")
    except Exception as e:  # papermill.PapermillExecutionError y afines
        print(f"✘ {nb}: {str(e).strip().splitlines()[-1] if str(e).strip() else e}")
        fallos.append(nb)

sys.exit(1 if fallos else 0)
