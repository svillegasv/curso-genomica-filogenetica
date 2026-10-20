# Datos del curso

Los datos **no** se guardan en este repositorio: están en Zenodo (DOI pendiente) y los cuadernos
los descargan con `curso.descargar()`, que verifica el md5.

`manifest.tsv` lista cada archivo: nombre, md5, tamaño, URL principal (Zenodo), espejo y descripción.

## Origen

- Genoma de referencia del ancestro *E. coli* REL606 (NCBI NC_012967.1).
- Lecturas Illumina de clones de la población Ara-3 del Experimento de Evolución a Largo Plazo (LTEE) de
  R. Lenski, publicadas en Tenaillon et al. (2016), *Nature* 536:165–170 (NCBI SRA). Aquí se usan
  **submuestreadas** para que cada paso corra en minutos en Colab.
- Resultados precalculados de los pasos pesados (elaboración propia, mismas herramientas del curso).

El paquete derivado de Zenodo se publica con licencia CC BY 4.0 y cita las fuentes originales.
