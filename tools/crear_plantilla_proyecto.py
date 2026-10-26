"""Genera proyecto/00-plantilla-proyecto.ipynb: el cuaderno de proyecto de una semana (sesión 2).

    python tools/crear_plantilla_proyecto.py

Cada semana el equipo abre su cuaderno de proyecto desde el README y lo guarda en la carpeta del proyecto
de su Drive. Los resultados quedan en esa carpeta y pasan de una semana a la siguiente.
"""
from pathlib import Path

from nbbuild import NB, SETUP, header

PATH = "proyecto/00-plantilla-proyecto.ipynb"
nb = NB()

nb.md(header(PATH, "Proyecto · Semana N · Título", "Semana N (Unidad U) · Sesión 2",
             "RA de la semana", "≈ 1,5 h", "Cuaderno guiado de la semana (sesión 1)"))

nb.md("""
## 🧬 Dónde va nuestro clon
Una línea que conecta lo aprendido en la sesión 1 con el problema: ¿qué cambió en el genoma de su clon, cuándo y por qué?

**Antes de empezar:** *Archivo → Guardar una copia en Drive* y muévala a la carpeta de su proyecto.
""")
nb.code(SETUP)
nb.code("""
p = curso.proyecto(drive=True)     # la carpeta del proyecto del equipo, en su Drive
# Solo la primera vez (semana 4): escriba el clon asignado a su equipo y quite el # de la línea siguiente.
# curso.equipo("REL7179B")
CLON = curso.equipo()
""")

nb.md("""
## ↻ Checkpoint
Verifica que estén los resultados de semanas anteriores. Si falta alguno, usa la versión precalculada de su clon.
""")
nb.code("""
# curso.checkpoint(f"results/{CLON}/...")   # una línea por resultado que esta semana necesita
""")

nb.md("""
## ❓ Pregunta 1
Una pregunta del problema que se responde con la técnica de la sesión 1, aplicada a **su** clon.

> 💡 **Pista:** al inicio del semestre, el comando casi completo; hacia el final, solo la idea.
""")
nb.code("""
# Su código aquí
""")
nb.md("""
**Respuesta del equipo:** (dos o tres frases: qué encontraron y qué significa para su clon)
""")

nb.md("""
## ❓ Pregunta 2
Otra pregunta, idealmente de interpretación o de comparación con lo que encontraron otros equipos.
""")
nb.code("""
# Su código aquí
""")
nb.md("""
**Respuesta del equipo:**

---

## 📓 Bitácora del equipo
- ¿Qué aprendimos?
- ¿Qué no nos quedó claro?
- ¿Qué hacemos con esto en el problema?

## 🎯 Reflexión individual (solo en semanas de hito)
Cada integrante escribe un párrafo propio: qué aprendió, qué le costó y qué aportó al equipo.
- **Integrante 1:**
- **Integrante 2:**
- **Integrante 3:**

**Entrega:** guarde este cuaderno en la carpeta de su equipo en la carpeta compartida del curso.
""")

nb.save(Path(__file__).resolve().parents[1] / PATH)
print("Plantilla escrita en", PATH)
