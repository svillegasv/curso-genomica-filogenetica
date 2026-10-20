"""Genera notebooks/00-plantilla.ipynb: la estructura que sigue todo cuaderno del curso.

    python tools/crear_plantilla.py

Para empezar un cuaderno nuevo, copie la plantilla (no la regenere encima de uno existente).
"""
from pathlib import Path

from nbbuild import NB, SETUP, header, solucion

PATH = "notebooks/00-plantilla.ipynb"
nb = NB()

nb.md(header(PATH, "Semana N · Título de la sesión", "Semana N (Unidad U)",
             "RA1 — qué será capaz de hacer al final", "≈ 2 h", "Cuaderno de la semana anterior"))

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
## 1. Ejemplo resuelto
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
""")

nb.md("""
## 2. Ejercicio guiado
Complete los huecos `___`.
""")
nb.code("""
# Ejercicio 1: cuente las bases de cada secuencia (complete el hueco)
from pathlib import Path
secuencias = Path(p / "data/processed/ejemplo.fasta").read_text().split()[1::2]
longitudes = [len(s) for s in secuencias]   # ← en la versión del estudiante: [___ for s in secuencias]
longitudes
""")
nb.code(solucion(1, """
longitudes = [len(s) for s in secuencias]
print(longitudes)
"""))

nb.md("""
## 3. Reto abierto
Una pregunta sin receta que exija combinar lo de hoy. Para trabajar en parejas (conductor/navegante).
""")

nb.md("""
## ✅ Compruebe su comprensión
1. Pregunta de recuperación sobre la idea central.
2. Pregunta que conecte con la semana anterior.

## 📓 Bitácora
- ¿Qué aprendí?
- ¿Qué no me quedó claro?
- ¿Qué hago con esto en el problema del LTEE?

## 📚 Referencias
Solo referencias verificadas.
""")

nb.save(Path(__file__).resolve().parents[1] / PATH)
print("Plantilla escrita en", PATH)
