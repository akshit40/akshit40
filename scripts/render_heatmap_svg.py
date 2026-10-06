from pathlib import Path
import json
from datetime import date,timedelta

data=json.loads(Path("data/contributions.json").read_text())
days={x["date"]:x for x in data["days"]}
pal=["#161b22","#0e4429","#006d32","#26a641","#39d353","#69f0a0"]
latest=date.fromisoformat(max(days))
start=latest-timedelta(days=latest.weekday()+364)
cells=[]
for w in range(53):
    for dow in range(7):
        d=start+timedelta(days=w*7+dow)
        x=days.get(d.isoformat(),{"level":0})
        xx=34+w*17; yy=28+dow*17; delay=(w+dow)*.012
        cells.append(f'<rect x="{xx}" y="{yy}" width="13" height="13" rx="3" fill="{pal[min(x["level"],5)]}" opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{delay:.3f}s" dur=".35s" fill="freeze"/></rect>')
st=data["stats"]
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="980" height="250" viewBox="0 0 980 250"><rect width="100%" height="100%" rx="14" fill="#0d1117" stroke="#30363d"/><text x="34" y="18" fill="#8b949e" font-family="monospace" font-size="10">LESS</text>{''.join(cells)}<text x="34" y="162" fill="#c9d1d9" font-family="monospace" font-size="14">{st["total"]:,} contributions in the last year</text><text x="34" y="184" fill="#7ee787" font-family="monospace" font-size="12">current streak: {st["current_streak"]} days</text><text x="220" y="184" fill="#8b949e" font-family="monospace" font-size="12">longest: {st["longest_streak"]} days</text><text x="34" y="214" fill="#6e7681" font-family="monospace" font-size="11">akshit@github:~$ contributions --live</text><text x="870" y="18" fill="#8b949e" font-family="monospace" font-size="10">MORE</text></svg>'''
Path("contrib-heatmap.svg").write_text(svg,encoding="utf-8")
print("Wrote contrib-heatmap.svg")
