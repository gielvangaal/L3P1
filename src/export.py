from pathlib import Path

OUTPUT_DIR = Path("output")


def _destination(filename: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR / filename


def export_matplotlib(fig, filename: str) -> Path:
    """Save a Matplotlib figure as a PNG image."""
    path = _destination(filename)
    fig.savefig(fname=path, dpi=150, bbox_inches="tight")
    return path


def export_plotly(fig, filename: str) -> Path:
    """Save an interactive Plotly chart as self-contained HTML."""
    path = _destination(filename)
    fig.write_html(file=str(path), include_plotlyjs=True, full_html=True)
    return path


def export_folium(map_object, filename: str) -> Path:
    """Save a Folium map as HTML (map tiles generally need internet)."""
    path = _destination(filename)
    map_object.save(outfile=str(path))
    return path


def export_altair(chart, filename: str) -> Path:
    """Save an Altair chart as HTML (may load JS dependencies online)."""
    path = _destination(filename)
    chart.save(fp=str(path), format="html")
    return path


# def export_bokeh(figure, filename: str) -> Path:
#     """Save Bokeh figures/layouts as HTML with bundled JavaScript."""
#     from bokeh.embed import file_html
#     from bokeh.resources import INLINE
#
#     path = _destination(filename)
#     path.write_text(file_html(figure, INLINE, title=path.stem), encoding="utf-8")
#     return path


# def export_panel(view, filename: str) -> Path:
#     """Save a Panel/hvPlot view to HTML; Python-backed callbacks may not work offline."""
#     import panel as pn
#
#     path = _destination(filename)
#     pn.panel(view).save(str(path), embed=True, resources="inline")
#     return path
