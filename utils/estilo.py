"""
estilo.py — Estilo gráfico común del curso y mapa «dónde estamos».

Paleta y tema adaptados de `utils/estilo_curso.py` de *Bioinformática Práctica*
(Juvenal Yosa, licencia MIT, https://github.com/juvenalyosa/bioinformatica-practica).

Uso en un cuaderno:

    import estilo as es
    es.set_style()
    fig, ax = plt.subplots()
    ...
    es.title(ax, "Título = la conclusión", "Subtítulo: qué se muestra")

La paleta categórica es apta para daltonismo (orden fijo, nunca cíclico).
Los nucleótidos usan A verde, C azul, G amarillo, T rojo, SIEMPRE acompañados de la letra.
"""

from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyBboxPatch

# ---------------------------------------------------------------------------
# Paleta
# ---------------------------------------------------------------------------
SURFACE = "#fcfcfb"   # fondo
INK = "#0b0b0b"       # texto principal
INK_2 = "#52514e"     # texto secundario
MUTED = "#898781"     # ejes, ticks
GRID = "#e1e0d9"      # rejilla
BASELINE = "#c3c2b7"  # ejes / línea base

CATEGORICAL = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100",
               "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREEN, VIOLET, RED = CATEGORICAL

NUC_COLORS = {"A": "#008300", "C": "#2a78d6", "G": "#eda100",
              "T": "#e34948", "U": "#e34948", "N": "#898781"}

SEQ_BLUE = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#2a78d6",
            "#1c5cab", "#104281", "#0d366b"]
CMAP_SEQ = LinearSegmentedColormap.from_list("curso_seq", SEQ_BLUE)
CMAP_DIV = LinearSegmentedColormap.from_list(
    "curso_div", ["#104281", "#3987e5", "#9ec5f4", "#f0efec",
                  "#f3b0ae", "#e66767", "#b8302f"])

try:
    mpl.colormaps.register(CMAP_SEQ)
    mpl.colormaps.register(CMAP_DIV)
except (ValueError, AttributeError):
    pass


def set_style(dpi: int = 110) -> None:
    """Aplica el tema del curso a matplotlib."""
    mpl.rcParams.update({
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
        "figure.dpi": dpi, "savefig.dpi": 200, "savefig.bbox": "tight",
        "figure.figsize": (8, 4.5), "figure.constrained_layout.use": True,
        "font.family": "DejaVu Sans", "font.size": 11, "text.color": INK,
        "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
        "axes.titlepad": 12, "axes.labelsize": 11, "axes.labelcolor": INK_2,
        "xtick.color": MUTED, "ytick.color": MUTED,
        "xtick.labelcolor": INK_2, "ytick.labelcolor": INK_2,
        "legend.frameon": False, "legend.fontsize": 10,
        "axes.edgecolor": BASELINE, "axes.linewidth": 1.0,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "axes.grid.axis": "y", "grid.color": GRID, "grid.linewidth": 0.8,
        "axes.axisbelow": True, "xtick.major.size": 0, "ytick.major.size": 0,
        "lines.linewidth": 2.0, "lines.markersize": 7, "patch.linewidth": 0,
        "axes.prop_cycle": mpl.cycler(color=CATEGORICAL), "image.cmap": "curso_seq",
    })


def title(ax, main: str, subtitle: str | None = None) -> None:
    """Título en negrita (la conclusión) + subtítulo gris (qué se muestra)."""
    if subtitle:
        ax.set_title(main, loc="left", pad=28)
        ax.text(0, 1.02, subtitle, transform=ax.transAxes, ha="left", va="bottom",
                fontsize=10.5, color=INK_2)
    else:
        ax.set_title(main, loc="left")


def nuc_colors(seq: str) -> list[str]:
    """Color de cada base de una secuencia (úselo siempre junto con la letra)."""
    return [NUC_COLORS.get(b.upper(), MUTED) for b in seq]


# ---------------------------------------------------------------------------
# Mapa «dónde estamos»
# ---------------------------------------------------------------------------
# Etapas del curso en orden: (clave, etiqueta, semanas)
ETAPAS = [
    ("unix", "Bootcamp\nUNIX", "Semanas 1–3"),
    ("problema", "El problema\n(LTEE)", "Semana 4"),
    ("qc", "Calidad de\nlecturas", "Semana 5"),
    ("ensamblaje", "Ensamblaje", "Semanas 6–7"),
    ("anotacion", "Anotación", "Semana 8"),
    ("taxonomia", "Contaminación", "Semana 9"),
    ("mapeo", "Mapeo", "Semana 10"),
    ("variantes", "Variantes", "Semana 11"),
    ("interes", "Variantes\nde interés", "Semana 12"),
    ("filogenia", "Filogenia", "Semanas 13–14"),
    ("pipeline", "Pipeline\n(Snakemake)", "Semana 15"),
    ("informe", "Informe y\nsustentación", "Semana 16"),
]


def mapa_curso(etapa: str, ruta: str | None = None, por_fila: int = 6):
    """Dibuja el recorrido del curso resaltando `etapa` (una clave de ETAPAS).

    Las etapas anteriores quedan marcadas como hechas; las siguientes, en gris.
    Si se da `ruta`, guarda la figura (SVG o PNG según la extensión).
    """
    claves = [k for k, _, _ in ETAPAS]
    if etapa not in claves:
        raise ValueError(f"Etapa desconocida: {etapa!r}. Use una de {claves}")
    actual = claves.index(etapa)
    filas = -(-len(ETAPAS) // por_fila)

    with mpl.rc_context({"figure.constrained_layout.use": False, "axes.grid": False}):
        fig, ax = plt.subplots(figsize=(12, 1.9 * filas))
        ax.set_xlim(0, por_fila)
        ax.set_ylim(filas, 0)
        ax.axis("off")
        for i, (_, etiqueta, semanas) in enumerate(ETAPAS):
            fila, col = divmod(i, por_fila)
            if i < actual:
                fondo, borde, texto = "#e3eefb", BLUE, INK_2
            elif i == actual:
                fondo, borde, texto = BLUE, BLUE, "white"
            else:
                fondo, borde, texto = SURFACE, BASELINE, MUTED
            ax.add_patch(FancyBboxPatch((col + 0.08, fila + 0.18), 0.84, 0.64,
                                        boxstyle="round,pad=0,rounding_size=0.08",
                                        facecolor=fondo, edgecolor=borde, linewidth=1.5))
            peso = "bold" if i == actual else "normal"
            ax.text(col + 0.5, fila + 0.46, etiqueta, ha="center", va="center",
                    fontsize=11, color=texto, weight=peso)
            ax.text(col + 0.5, fila + 0.72, semanas, ha="center", va="center",
                    fontsize=9, color=texto)
            if i < len(ETAPAS) - 1 and col < por_fila - 1:
                ax.annotate("", xy=(col + 1.08, fila + 0.5), xytext=(col + 0.92, fila + 0.5),
                            arrowprops=dict(arrowstyle="-|>", color=BASELINE, lw=1.2))
        fig.subplots_adjust(0, 0, 1, 1)
        if ruta:
            fig.savefig(ruta, bbox_inches="tight", pad_inches=0.05)
    return fig
