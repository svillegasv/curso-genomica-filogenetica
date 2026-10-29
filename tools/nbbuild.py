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


def solucion(titulo, codigo: str = "", explicacion: str = "") -> str:
    """Celda de TEXTO con la solución en un desplegable cerrado (úsese con nb.md).

    No se ejecuta nada: el estudiante la abre, copia el comando en SU celda y la corre.
    `titulo` puede ser un número ("Solución del ejercicio 1") o un texto ("Respuestas").
    """
    resumen = f"Solución del ejercicio {titulo}" if isinstance(titulo, int) else titulo
    partes = [f"<details><summary>🔑 <b>{resumen}</b></summary>", ""]
    if codigo.strip():
        partes += ["```", textwrap.dedent(codigo).strip("\n"), "```", ""]
    if explicacion.strip():
        partes += [textwrap.dedent(explicacion).strip("\n"), ""]
    return "\n".join(partes + ["</details>"])


def ocultar_observaciones(md: str) -> str:
    """Convierte cada cita «> 🔎 …» en un desplegable cerrado, para no revelar la respuesta antes de ejecutar."""
    lineas, salida, i = md.split("\n"), [], 0
    while i < len(lineas):
        if not lineas[i].startswith("> 🔎"):
            salida.append(lineas[i])
            i += 1
            continue
        bloque = []
        while i < len(lineas) and lineas[i].startswith(">"):
            bloque.append(lineas[i][1:].strip())
            i += 1
        texto = " ".join(bloque).removeprefix("🔎").strip().removeprefix("**Qué observamos.**").strip()
        salida += ["<details><summary>🔎 <b>Qué observamos</b> (ábralo después de ejecutar)</summary>",
                   "", texto, "", "</details>"]
    return "\n".join(salida)


def separar_desplegables(md: str) -> list[str]:
    """Parte el texto para que cada <details>…</details> quede en su propia celda."""
    partes, resto = [], md
    while "<details>" in resto:
        antes, _, despues = resto.partition("<details>")
        dentro, _, resto = despues.partition("</details>")
        partes += [antes.strip("\n"), "<details>" + dentro + "</details>"]
    partes.append(resto.strip("\n"))
    return [x for x in partes if x.strip()]


class NB:
    def __init__(self):
        self.nb = nbf.v4.new_notebook()
        self.nb.metadata = {
            "colab": {"provenance": [], "toc_visible": True},
            "kernelspec": {"name": "python3", "display_name": "Python 3"},
            "language_info": {"name": "python"},
        }

    def md(self, s):
        # Cada desplegable va solo en su celda: Colab mete dentro del <details> el texto que lo sigue en la misma celda
        for parte in separar_desplegables(ocultar_observaciones(textwrap.dedent(s).strip("\n"))):
            self.nb.cells.append(nbf.v4.new_markdown_cell(parte))

    def code(self, s):
        self.nb.cells.append(nbf.v4.new_code_cell(textwrap.dedent(s).strip("\n")))

    def ejercicio(self, estudiante, respuesta):
        """Celda de ejercicio: el estudiante ve `estudiante` (con COMPLETE); la respuesta completa va en una
        nota interna (metadata["curso"]["respuesta"]) que solo usa tools/probar.py para ejecutar el cuaderno."""
        celda = nbf.v4.new_code_cell(textwrap.dedent(estudiante).strip("\n"))
        celda.metadata["curso"] = {"respuesta": textwrap.dedent(respuesta).strip("\n")}
        self.nb.cells.append(celda)

    def save(self, path):
        self.md(FOOTER)
        nbf.write(self.nb, path)
