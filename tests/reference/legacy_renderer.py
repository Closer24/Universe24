"""Diagnostic HTML renderer for the 3D integer simulator.

Policy: every simulator run should call this diagnostic layer and produce an HTML
artifact. The physical simulator core remains integer-only; this file is output-only.
"""
from pathlib import Path
import base64
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

def render_xy_run(frames, z0, xmin, xmax, ymin, ymax, html_path, gif_path):
    """frames: iterable of dicts with tick, field {(x,y):phi}, particles tuples,
    and total_momentum. Produces a GIF embedded inside standalone HTML."""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    def draw(i):
        ax.clear()
        f = frames[i]
        grid = [[0]*(xmax-xmin+1) for _ in range(ymax-ymin+1)]
        for (x,y),v in f["field"].items():
            if xmin <= x <= xmax and ymin <= y <= ymax:
                grid[y-ymin][x-xmin] = v
        ax.imshow(grid, origin="lower",
                  extent=(xmin-.5,xmax+.5,ymin-.5,ymax+.5),
                  interpolation="nearest", aspect="equal")
        for pid,x,y,px,py,pz in f["particles"]:
            ax.scatter([x],[y],s=110)
            mag=max(1,abs(px)+abs(py))
            ax.arrow(x,y,1.6*px/mag,1.6*py/mag,width=.04,length_includes_head=True)
            ax.text(x+.4,y+.3,str(pid))
        ax.set_xlim(xmin-.5,xmax+.5); ax.set_ylim(ymin-.5,ymax+.5)
        ax.grid(True,alpha=.2)
        ax.set_title(f"3D simulator, XY slice z={z0} | tick={f['tick']} | Ptot={f['total_momentum']}")
        ax.set_xlabel("x"); ax.set_ylabel("y")
    ani=FuncAnimation(fig,draw,frames=len(frames),interval=120)
    ani.save(gif_path,writer=PillowWriter(fps=8))
    plt.close(fig)
    b64=base64.b64encode(Path(gif_path).read_bytes()).decode()
    Path(html_path).write_text(f"""<!doctype html><html><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<style>body{{margin:0;background:#111;color:#eee;font-family:system-ui;text-align:center}}
main{{max-width:960px;margin:auto;padding:18px}}img{{width:100%;height:auto;border-radius:10px}}</style></head>
<body><main><h2>3D integer simulator run</h2>
<p>Full physics is 3D; this is the XY diagnostic slice z={z0}.</p>
<img src="data:image/gif;base64,{b64}"></main></body></html>""",encoding="utf-8")
    return str(html_path)
