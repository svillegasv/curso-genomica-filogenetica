# Mantenimiento (para el profesor)

## Probar todo antes de clase
```
conda env create -f environment.yml     # una sola vez
conda activate genomica-filogenetica
python tools/probar.py                  # todos los cuadernos
python tools/probar.py notebooks/semana-01/*.ipynb
```
GitHub Actions corre lo mismo en cada cambio y cada lunes (pestaña *Actions* del repositorio).

## Crear un cuaderno nuevo
Copie `notebooks/00-plantilla.ipynb` a `notebooks/semana-NN/` y edítelo. El `.ipynb` es la fuente de
verdad: `tools/crear_plantilla.py` solo regenera la plantilla.

## Editar desde Colab
Abra el cuaderno con el botón del README, edítelo y use *Archivo → Guardar una copia en GitHub*
(rama `main`). Las salidas se limpian solas si el commit se hace en local con pre-commit; desde Colab,
antes de guardar use *Editar → Borrar todas las salidas*.

## Diapositivas
Copie `slides/plantilla.html` a `slides/semana-NN.html` y cambie la etapa del mapa
(`img/mapa-<etapa>.svg`). Los mapas se regeneran con `python tools/mapas.py` (las etapas están en
`utils/estilo.py`, `ETAPAS`).

## Datos
Cada archivo del curso tiene una fila en `data/manifest.tsv` (nombre, md5, URL de Zenodo, espejo).
Los cuadernos lo descargan con `curso.descargar(nombre, destino)` y lo verifican.

## Herramientas
`utils/curso.py` (`HERRAMIENTAS`) dice cómo se instala cada una en Colab (apt o bioconda). Las versiones
de bioconda se fijan en `environment.yml`.

## Al inicio de cada semestre
1. Correr `python tools/probar.py` y abrir en Colab el cuaderno de la semana 1.
2. Revisar que las descargas de Zenodo respondan.
3. Actualizar fechas en el README y en las diapositivas.
