"""Genera el mapa «dónde estamos» de cada etapa en slides/img/mapa-<etapa>.svg.

    python tools/mapas.py
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "utils"))
import estilo as es  # noqa: E402

es.set_style()
destino = RAIZ / "slides" / "img"
destino.mkdir(parents=True, exist_ok=True)
for clave, _, _ in es.ETAPAS:
    fig = es.mapa_curso(clave, destino / f"mapa-{clave}.svg")
    plt.close(fig)
print(f"{len(es.ETAPAS)} mapas en {destino.relative_to(RAIZ)}/")
