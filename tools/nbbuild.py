"""Ayudantes para CREAR cuadernos nuevos del curso con la estructura estándar.

Basado en `tools/nbbuild.py` de *Bioinformática Práctica* (Juvenal Yosa, MIT).

El .ipynb es la fuente de verdad: este módulo solo genera el primer borrador. Después el cuaderno
se edita directamente (en Colab o en Jupyter) y no se vuelve a generar.
"""
import textwrap

import nbformat as nbf

REPO = "svillegasv/curso-genomica-filogenetica"
CURSO = "Genómica y Filogenética"
AUTOR = "Simón Villegas-Velásquez"


def colab_badge(path: str) -> str:
    return (f"[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)]"
            f"(https://colab.research.google.com/github/{REPO}/blob/main/{path})")


def header(path, titulo, semana, ra, duracion, requisitos):
    return f"""# {titulo}

{colab_badge(path)}

**{CURSO}** · {semana} · {AUTOR}

**🎯 Resultado de aprendizaje:** {ra}<br>
**⏱️ Duración:** {duracion} · **🧰 Requisitos:** {requisitos}

---
"""


SETUP = '''\
#@title ⚙️ Configuración (ejecute esta celda primero) { display-mode: "form" }
import os, sys, urllib.request
from pathlib import Path

RAW = "https://raw.githubusercontent.com/svillegasv/curso-genomica-filogenetica/main"
_utils = next((p / "utils" for p in [Path.cwd(), *Path.cwd().parents]
               if (p / "utils" / "curso.py").exists()), None)
if _utils is None:  # en Colab: se descargan las utilidades del curso
    _utils = Path(".curso/utils")
    _utils.mkdir(parents=True, exist_ok=True)
    for _f in ("curso.py", "estilo.py"):
        urllib.request.urlretrieve(f"{RAW}/utils/{_f}", _utils / _f)
sys.path.insert(0, str(_utils))

import curso
import estilo as es
import matplotlib.pyplot as plt
es.set_style()
print("Entorno listo ✔ | Colab:", curso.IN_COLAB)
'''

FOOTER = f"""---

<sub>**{CURSO}** · © 2026 {AUTOR} · Código bajo licencia MIT · Texto y figuras bajo CC BY 4.0 ·
[Repositorio](https://github.com/{REPO})</sub>
"""


def solucion(n, codigo: str) -> str:
    """Celda de solución oculta (Colab la muestra plegada como formulario)."""
    return f'#@title 🔑 Solución — Ejercicio {n} {{ display-mode: "form" }}\n' + textwrap.dedent(codigo).strip("\n")


class NB:
    def __init__(self):
        self.nb = nbf.v4.new_notebook()
        self.nb.metadata = {
            "colab": {"provenance": [], "toc_visible": True},
            "kernelspec": {"name": "python3", "display_name": "Python 3"},
            "language_info": {"name": "python"},
        }

    def md(self, s):
        self.nb.cells.append(nbf.v4.new_markdown_cell(textwrap.dedent(s).strip("\n")))

    def code(self, s):
        self.nb.cells.append(nbf.v4.new_code_cell(textwrap.dedent(s).strip("\n")))

    def save(self, path):
        self.md(FOOTER)
        nbf.write(self.nb, path)
