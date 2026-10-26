"""Genera notebooks/00-plantilla.ipynb: la estructura del cuaderno guiado de la sesión 1.

    python tools/crear_plantilla.py

Para empezar un cuaderno nuevo, copie la plantilla (no la regenere encima de uno existente).
"""
from pathlib import Path

from nbbuild import NB, SETUP, header, solucion

PATH = "notebooks/00-plantilla.ipynb"
nb = NB()

nb.md(header(PATH, "Semana N · Título de la sesión", "Semana N (Unidad U)",
             "RA1 — qué será capaz de hacer al final", "≈ 1,5 h", "Cuaderno de la semana anterior"))

nb.md("""
## 🧭 Dónde estamos
Una línea que conecta esta sesión con el problema del semestre (el LTEE) y con la semana anterior.
""")
nb.code(SETUP)
nb.code("""
es.mapa_curso("unix");   # cambie la clave por la etapa de la semana (ver es.ETAPAS)
""")

nb.md("""
## ❓ La pregunta biológica
¿Qué queremos saber hoy y por qué importa para el problema? Las herramientas aparecen **después** de la pregunta.
""")

nb.md("""
## 🛠️ Preparar el entorno y los datos
Instale solo lo que use la sesión y cree (o recupere) el proyecto.
""")
nb.code("""
# curso.instalar("seqkit")                 # herramientas de la sesión
p = curso.proyecto()                       # en semanas 4+: curso.proyecto(drive=True)
# curso.checkpoint("results/...")          # resultados de semanas anteriores
# curso.descargar("archivo.fastq.gz", p / "data/raw")
""")

nb.md("""
## Bloque 1 · Primera idea de la sesión
Cada bloque enseña una habilidad (una lección del outline). Un cuaderno de 1,5 h suele tener **2 o 3 bloques**.

### Ejemplo resuelto
Explicación corta con una comparación cotidiana, luego el comando o código completo.

> 🤔 **Antes de ejecutar, prediga:** ¿cuántas secuencias tiene el archivo?
""")
nb.code("""
%%bash
cd $PROYECTO
printf ">seq1\\nACGT\\n>seq2\\nGGCC\\n" > data/processed/ejemplo.fasta
grep -c ">" data/processed/ejemplo.fasta
""")
nb.md("""
> 🔎 **Qué observamos.** Interpretación en dos o tres frases: ¿coincidió con su predicción?

### Ejercicio guiado
Reemplace cada `COMPLETE` por su respuesta.
""")
nb.code("""
%%bash
# Ejercicio 1: cuente las líneas del archivo (en la versión del estudiante: wc COMPLETE data/processed/ejemplo.fasta)
cd $PROYECTO
wc -l data/processed/ejemplo.fasta
""")
# En celdas de solución, la shell va con "!" (el #@title debe ser la primera línea, antes de cualquier %%bash)
nb.code(solucion(1, """
!cd $PROYECTO && wc -l data/processed/ejemplo.fasta
"""))

nb.md("""
## Bloque 2 · Segunda idea de la sesión
El mismo ciclo: predecir → ejemplo resuelto → ejercicio guiado.

### Ejemplo resuelto
> 🤔 **Antes de ejecutar, prediga:** ¿qué longitud tiene cada secuencia?
""")
nb.code("""
from pathlib import Path
secuencias = Path(p / "data/processed/ejemplo.fasta").read_text().split()[1::2]
[len(s) for s in secuencias]
""")
nb.md("""
> 🔎 **Qué observamos.** …

### Ejercicio guiado
""")
nb.code("""
# Ejercicio 2: cuente cuántas G tiene cada secuencia (en la versión del estudiante: [COMPLETE for s in secuencias])
[s.count("G") for s in secuencias]
""")
nb.code(solucion(2, """
print([s.count("G") for s in secuencias])
"""))

nb.md("""
## ✅ Compruebe su comprensión
1. Pregunta de recuperación sobre la idea central.
2. Pregunta que conecte con la semana anterior.

## 🚀 Para ir más allá (opcional)
Un reto sin solución para quien termine antes. Admite varias respuestas.
El reto del proyecto se trabaja en la sesión 2, en el cuaderno de proyecto.

## 📚 Referencias
Solo referencias verificadas.
""")

nb.save(Path(__file__).resolve().parents[1] / PATH)
print("Plantilla escrita en", PATH)
