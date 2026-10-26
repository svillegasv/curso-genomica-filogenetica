"""
curso.py — Utilidades comunes de los cuadernos de Genómica y Filogenética.

Lo usa la celda ⚙️ Configuración de cada cuaderno. Funciona igual en Colab y en un computador
local (con el entorno de `environment.yml`).

    import curso
    curso.instalar("seqkit", "fastp")          # herramientas de línea de comandos
    p = curso.proyecto()                        # carpeta del proyecto (y $PROYECTO para %%bash)
    curso.descargar("ara3_clon_a_R1.fastq.gz", p / "data/raw")
    curso.checkpoint("results/qc/fastp.json")   # restaura lo de semanas anteriores si falta
"""

from __future__ import annotations

import csv
import hashlib
import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

REPO = "svillegasv/curso-genomica-filogenetica"
RAW = f"https://raw.githubusercontent.com/{REPO}/main"

try:
    import google.colab  # noqa: F401
    IN_COLAB = True
except ImportError:
    IN_COLAB = False

# Herramienta → (vía de instalación en Colab, paquete). El nombre de la clave es el ejecutable.
# apt: repositorios de Ubuntu de Colab. mamba: bioconda (versiones en environment.yml).
HERRAMIENTAS = {
    "seqkit": ("apt", "seqkit"),
    "seqtk": ("apt", "seqtk"),
    "fastp": ("apt", "fastp"),
    "bwa": ("apt", "bwa"),
    "samtools": ("apt", "samtools"),
    "bcftools": ("apt", "bcftools"),
    "minimap2": ("apt", "minimap2"),
    "mafft": ("apt", "mafft"),
    "iqtree2": ("apt", "iqtree"),
    "spades.py": ("apt", "spades"),
    "blastn": ("apt", "ncbi-blast+"),
    "multiqc": ("mamba", "multiqc"),
    "quast.py": ("mamba", "quast"),
    "prokka": ("mamba", "prokka"),
    "bakta": ("mamba", "bakta"),
    "snpEff": ("mamba", "snpeff"),
    "kraken2": ("mamba", "kraken2"),
    "bracken": ("mamba", "bracken"),
    "flye": ("mamba", "flye"),
    "filtlong": ("mamba", "filtlong"),
    "snakemake": ("mamba", "snakemake-minimal"),
}

MAMBA_ENV = Path("/content/.mamba-env")


def _raiz_repo() -> Path | None:
    """Raíz del repositorio si el cuaderno corre dentro de una copia local."""
    for p in [Path.cwd(), *Path.cwd().parents]:
        if (p / "utils" / "curso.py").exists():
            return p
    return None


def _archivo_repo(rel: str) -> Path:
    """Devuelve un archivo del repositorio: copia local o descarga desde GitHub."""
    raiz = _raiz_repo()
    if raiz and (raiz / rel).exists():
        return raiz / rel
    destino = Path(".curso") / rel
    if not destino.exists():
        destino.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(f"{RAW}/{rel}", destino)
    return destino


def _run(cmd: str) -> None:
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"Falló: {cmd}\n{r.stderr[-2000:]}")


# ---------------------------------------------------------------------------
# Instalación
# ---------------------------------------------------------------------------
def _versiones_fijadas() -> dict[str, str]:
    """Lee las versiones fijadas de environment.yml (líneas `- paquete=versión`)."""
    versiones = {}
    for linea in _archivo_repo("environment.yml").read_text().splitlines():
        linea = linea.strip()
        if linea.startswith("- ") and "=" in linea:
            nombre, version = linea[2:].split("#")[0].strip().split("=", 1)
            versiones[nombre.split("::")[-1]] = version.strip()
    return versiones


def _instalar_mamba(paquetes: list[str]) -> None:
    if not shutil.which("micromamba"):
        _run("curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest "
             "| tar -xj -C /usr/local bin/micromamba")
    fijadas = _versiones_fijadas()
    specs = " ".join(f"'{p}={fijadas[p]}'" if p in fijadas else p for p in paquetes)
    accion = "install" if MAMBA_ENV.exists() else "create"
    _run(f"micromamba {accion} -y -q -p {MAMBA_ENV} -c conda-forge -c bioconda {specs}")
    bin_dir = str(MAMBA_ENV / "bin")
    if bin_dir not in os.environ["PATH"].split(os.pathsep):
        # Al final del PATH: no tapa el Python de Colab. Lo heredan las celdas ! y %%bash.
        os.environ["PATH"] += os.pathsep + bin_dir


def instalar(*herramientas: str) -> None:
    """Instala (solo en Colab) las herramientas que falten. Fuera de Colab, solo verifica."""
    faltan = [h for h in herramientas if not shutil.which(h)]
    desconocidas = [h for h in faltan if h not in HERRAMIENTAS]
    if desconocidas:
        raise ValueError(f"No sé instalar {desconocidas}. Agréguelas a HERRAMIENTAS en utils/curso.py")
    if faltan and not IN_COLAB:
        raise RuntimeError(f"Faltan {faltan}. Fuera de Colab, active el entorno: "
                           "conda env create -f environment.yml")
    apt = [HERRAMIENTAS[h][1] for h in faltan if HERRAMIENTAS[h][0] == "apt"]
    mamba = [HERRAMIENTAS[h][1] for h in faltan if HERRAMIENTAS[h][0] == "mamba"]
    if apt:
        print("Instalando con apt:", ", ".join(apt), "…")
        _run("apt-get -qq update && DEBIAN_FRONTEND=noninteractive apt-get -qq install -y " + " ".join(apt))
    if mamba:
        print("Instalando con micromamba (bioconda):", ", ".join(mamba), "… (puede tardar 1–3 min)")
        _instalar_mamba(mamba)
    for h in herramientas:
        print(f"  {'✔' if shutil.which(h) else '✘'} {h}")


# ---------------------------------------------------------------------------
# Proyecto y datos
# ---------------------------------------------------------------------------
SUBCARPETAS = ["data/raw", "data/processed", "results", "scripts", "notebooks"]


def proyecto(drive: bool = False) -> Path:
    """Crea (si no existe) la carpeta del proyecto y la deja en $PROYECTO.

    drive=True guarda el proyecto en Google Drive para que sobreviva entre sesiones
    (se usa desde la semana 4). Sin Drive, en Colab el proyecto se pierde al cerrar la sesión.
    """
    if "CURSO_PROYECTO" in os.environ:          # p. ej. en las pruebas automáticas
        base = Path(os.environ["CURSO_PROYECTO"])
    elif IN_COLAB and drive:
        from google.colab import drive as gdrive
        gdrive.mount("/content/drive")
        base = Path("/content/drive/MyDrive/genomica-filogenetica")
    elif IN_COLAB:
        base = Path("/content/proyecto")
    else:
        base = Path.home() / "genomica-filogenetica-proyecto"
    for sub in SUBCARPETAS:
        (base / sub).mkdir(parents=True, exist_ok=True)
    os.environ["PROYECTO"] = str(base)          # las celdas %%bash pueden hacer: cd $PROYECTO
    print("Proyecto en:", base)
    return base


# Clones de Ara-3 del curso (uno por equipo). Ver plan/03_datos_ltee.md del taller del docente.
CLONES = ["REL1166B", "REL2181A", "REL4538A", "REL7179B", "ZDB478", "ZDB17", "ZDB25", "REL11365"]


def equipo(clon: str | None = None) -> str:
    """Guarda (una sola vez, en la semana 4) o lee el clon asignado al equipo.

        curso.equipo("REL7179B")   # primera vez: queda guardado en la carpeta del proyecto
        CLON = curso.equipo()      # semanas siguientes: lo lee
    """
    ruta = Path(os.environ.get("PROYECTO") or proyecto()) / "equipo.txt"
    if clon:
        if clon not in CLONES:
            raise ValueError(f"{clon!r} no es un clon del curso. Opciones: {', '.join(CLONES)}")
        ruta.write_text(clon + "\n")
        print(f"✔ Clon del equipo guardado: {clon}")
        return clon
    if ruta.exists():
        clon = ruta.read_text().strip()
    elif os.environ.get("CURSO_EQUIPO"):        # pruebas automáticas
        clon = os.environ["CURSO_EQUIPO"]
    else:
        raise RuntimeError('Aún no ha registrado su clon. Ejecute una vez: curso.equipo("CLON_ASIGNADO")')
    print("Clon del equipo:", clon)
    return clon


def _md5(ruta: Path) -> str:
    h = hashlib.md5()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def manifiesto() -> dict[str, dict]:
    """Archivos de datos del curso (data/manifest.tsv): nombre → {md5, url, descripcion}."""
    with open(_archivo_repo("data/manifest.tsv"), newline="") as f:
        return {fila["archivo"]: fila for fila in csv.DictReader(f, delimiter="\t")}


def descargar(nombre: str, destino: str | Path = ".") -> Path:
    """Descarga un archivo del manifiesto a `destino` y verifica su md5 (no repite si ya está)."""
    m = manifiesto()
    if nombre not in m:
        raise KeyError(f"{nombre!r} no está en data/manifest.tsv")
    info = m[nombre]
    ruta = Path(destino) / nombre
    ruta.parent.mkdir(parents=True, exist_ok=True)
    if ruta.exists() and _md5(ruta) == info["md5"]:
        print(f"✔ {nombre} ya estaba")
        return ruta
    for url in filter(None, (info["url"], info.get("espejo", ""))):
        try:
            urllib.request.urlretrieve(url, ruta)
            if _md5(ruta) == info["md5"]:
                print(f"✔ {nombre} descargado")
                return ruta
            print(f"⚠ md5 distinto desde {url}; pruebo el espejo")
        except OSError as e:
            print(f"⚠ No se pudo descargar desde {url}: {e}")
    raise RuntimeError(f"No se pudo obtener {nombre}. Avísele al profesor.")


def checkpoint(*rutas: str) -> None:
    """Verifica que existan los resultados de semanas anteriores (rutas relativas al proyecto).

    Si alguno falta, descarga la versión precalculada del manifiesto para que nadie quede
    bloqueado por una semana perdida.
    """
    base = Path(os.environ.get("PROYECTO") or proyecto())
    for rel in rutas:
        ruta = base / rel
        if ruta.exists():
            print(f"✔ {rel}")
        else:
            print(f"↻ {rel} no está: uso la versión precalculada")
            descargar(Path(rel).name, ruta.parent)


def versiones(*herramientas: str) -> None:
    """Imprime las versiones (registro de reproducibilidad)."""
    print("Python", sys.version.split()[0], "· Colab" if IN_COLAB else "· local")
    for h in herramientas:
        r = subprocess.run(f"{h} --version", shell=True, capture_output=True, text=True)
        salida = (r.stdout or r.stderr).strip().splitlines()
        print(f"  {h}: {salida[0] if salida else '¿?'}")
