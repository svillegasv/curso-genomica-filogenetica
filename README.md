# Genómica y Filogenética

Curso de pregrado (16 semanas) en **Google Colab**: de la línea de comandos de UNIX a la genómica bacteriana
y la filogenética, resolviendo un problema real con datos reales.

## El problema del semestre

**El experimento.** En 1988, Richard Lenski fundó doce poblaciones de la bacteria *Escherichia coli* a partir
de un mismo ancestro (la cepa REL606) y las puso a crecer en un medio con muy poca glucosa. Cada día, una pequeña
parte de cada población pasa a un frasco con medio fresco, y así llevan decenas de miles de generaciones. Cada
cierto número de generaciones se congela una muestra: es un registro fósil vivo, porque esas bacterias se pueden
revivir y secuenciar. Se conoce como el **Experimento de Evolución a Largo Plazo** (LTEE, por sus siglas en inglés).

**Lo sorprendente.** Una de las doce poblaciones, llamada **Ara-3**, desarrolló algo que *E. coli* normalmente no
hace: usar como alimento el citrato que hay en el medio, en presencia de oxígeno. Además, en algunos de sus
linajes la tasa de mutación se disparó, y sus genomas acumulan muchas más mutaciones que los demás.

**Su tarea.** Cada equipo recibe las lecturas de secuenciación de un clon de Ara-3, aislado en una generación
distinta. A lo largo del semestre reconstruirán su genoma, lo compararán con el del ancestro y responderán:
**¿qué cambió en su genoma, cuándo y por qué?** Al juntar los resultados de todos los equipos se verá la historia
evolutiva de la población.

## Cómo usar los cuadernos

Cada semana tiene dos cuadernos:

- **Sesión 1, cuaderno guiado:** se aprende la técnica con datos de demostración, iguales para todos.
- **Sesión 2, cuaderno de proyecto:** el equipo aplica la técnica a **su** clon. En el bootcamp (semanas 1–3) la
  sesión 2 es distinta: retos en parejas (semana 1), un *escape room* (semana 2) y, en la semana 3, el primer
  contacto con el clon del equipo.

1. Haga clic en **Abrir en Colab** junto al cuaderno.
2. Ejecute primero la celda **⚙️ Configuración**.
3. Guarde su copia: *Archivo → Guardar una copia en Drive*. Los cuadernos de proyecto van en la carpeta del proyecto
   de su equipo, donde también quedan sus resultados de una semana a otra.
4. En la semana 3, registre una sola vez el clon de su equipo: `curso.equipo("…")`.

No necesita instalar nada: solo una cuenta de Google.

## Contenido

| Semanas | Unidad | Cuadernos |
|---|---|---|
| 1–3 | U0 · Bootcamp UNIX en Colab | en construcción |
| 4 | U1 · El problema, evolución y repaso de Python | en construcción |
| 5 | U2 · Datos de secuenciación y control de calidad | en construcción |
| 6–7 | U3 · Ensamblaje *de novo* | en construcción |
| 8 | U4 · Anotación | en construcción |
| 9 | U5 · Contaminación y taxonomía | en construcción |
| 10 | U6 · Mapeo de lecturas | en construcción |
| 11 | U7 · Llamado de variantes | en construcción |
| 12 | U8 · Variantes de interés | en construcción |
| 13–14 | U9 · Filogenética | en construcción |
| 15 | U10 · Del cuaderno al pipeline (Snakemake) | en construcción |
| 16 | Informe final y sustentación | — |

## Estructura del repositorio

```
notebooks/   cuadernos guiados de la sesión 1 (00-plantilla.ipynb: estructura estándar)
proyecto/    cuadernos de proyecto de la sesión 2 (00-plantilla-proyecto.ipynb)
slides/      apoyo visual semanal (HTML; se abre en el navegador)
utils/       curso.py (instalación, datos, proyecto) · estilo.py (figuras y mapa del curso)
data/        manifest.tsv: los datos están en Zenodo, no en git
tools/       crear cuadernos, generar mapas, probar todo
```

## Licencia y créditos

- Código: **MIT** (`LICENSE`). Texto, diapositivas y figuras: **CC BY 4.0** (`LICENCIA-CONTENIDO.md`).
- Adapta material de *Bioinformática Práctica* (J. Yosa, MIT) y *Bacterial Genomics Intro*
  (S. Schmeier y O. Silander, MIT). Datos del LTEE: ver `data/README.md`.
- Para citar el curso: `CITATION.cff`.
- Construido con la ayuda de Claude (Anthropic).
