#!/usr/bin/env python3
"""Generate first-party bilingual aggregate-only bird notebook figures.
No API requests, individual record positions, species, observers, or photos.
Run: python3 scripts/render_eds_notebook_grid.py --snapshot /path/to/data/first-page-grids-20261026.json
"""
from collections import Counter
from hashlib import sha256
from html import escape
from pathlib import Path
import argparse
import json

SOURCE_SHA="0fb26d2974897882ff3cc952727c1449026e982faa51fbda3854d7229bf40ab4"
SOURCE_COMMIT="6c411e0b7159897b164621143bb863537a606994"
SOURCE_URL=("https://github.com/saramjh/bird-records-not-absence-notebook/blob/"
            +SOURCE_COMMIT+"/data/first-page-grids-20261026.json")
OUT=Path(__file__).resolve().parents[1]/"assets/images/dev/eds-notebook-grid-20261115"
INK="#153549"
COLORS=("#acd9d3","#5ab3a9","#277b84","#173c67")

LABELS={
 "ko":dict(title="같은 기록, 서로 다른 격자",lead="2024년 GBIF 첫 조회 100건 · 좌표 불확실성 예시 기준 1 km",
  fine="10 km 격자",coarse="50 km 격자",occupied="표시된 칸",
  accepted="기준 통과",missing="불확실성 누락",excluded="기준 초과",
  note="빈 칸은 새가 없다는 증거가 아닙니다. 실제 조사 범위는 표시되지 않았습니다.",
  source="작성자 측 파생 격자 · 비무작위 첫 페이지 · 관측 다운로드 DOI 없음",
  desc="같은 50건의 첫 페이지 조류 관측 기록을 10 km 격자와 50 km 격자로 집계했습니다. 기록이 표시된 칸은 각각 12개와 8개입니다. 빈 칸은 새의 부재를 뜻하지 않습니다."),
 "en":dict(title="Same records, different grids",lead="First 100 GBIF search rows (2024) · illustrative 1 km uncertainty screen",
  fine="10 km grid",coarse="50 km grid",occupied="occupied cells",
  accepted="Retained",missing="Missing uncertainty",excluded="Above threshold",
  note="Blank cells are not evidence of biological absence. Sampling effort is not shown.",
  source="Author-derived grid · non-random first page · no occurrence-download DOI",
  desc="The same 50 screened occurrence records from a non-random GBIF search page are aggregated to 10 km and 50 km grids. Twelve and eight cells contain records respectively. Empty cells do not demonstrate absence.")
}

def color(c):
 return COLORS[0 if c==1 else 1 if c<=4 else 2 if c<=9 else 3]

def render(snapshot,lang):
 t=LABELS[lang]
 fine=Counter({(int(a),int(b)):int(c) for a,b,c in snapshot["cells_10km"]})
 coarse=Counter()
 for (gx,gy),n in fine.items():coarse[(gx//5,gy//5)]+=n
 assert (len(fine),len(coarse),sum(fine.values()),sum(coarse.values()))==(12,8,50,50)
 assert snapshot["rows_in_page"]==100 and snapshot["accepted_count"]==50
 assert snapshot["excluded"]=={"above_illustrative_threshold":11,"uncertainty_missing":39}
 assert snapshot["projected_crs"]=="EPSG:32652" and snapshot["grid_m"]==10000
 xmin=min(gx*step for step,cells in [(10000,fine),(50000,coarse)] for gx,gy in cells)
 xmax=max((gx+1)*step for step,cells in [(10000,fine),(50000,coarse)] for gx,gy in cells)
 ymin=min(gy*step for step,cells in [(10000,fine),(50000,coarse)] for gx,gy in cells)
 ymax=max((gy+1)*step for step,cells in [(10000,fine),(50000,coarse)] for gx,gy in cells)
 scale=min(280/(xmax-xmin),347/(ymax-ymin))
 safe=lambda s:escape(str(s),quote=True)
 a=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1152" height="680" viewBox="0 0 1152 680" lang="{lang}" role="img" aria-labelledby="figtitle figdesc" data-source-sha256="{SOURCE_SHA}" data-selection-first-page-records="100" data-records-accepted="50" data-unknown-uncertainty="39" data-over-threshold="11">',
   f'<title id="figtitle">{safe(t["title"])}</title>',
   f'<desc id="figdesc">{safe(t["desc"])}</desc>',
   f'<metadata>Derived exclusively from first-party aggregated snapshot {SOURCE_URL}, commit {SOURCE_COMMIT}; nonrandom mutable first-page trial, UTM zone 52N, no occurrence-download DOI.</metadata>',
   '<rect x="0" y="0" width="1152" height="680" rx="15" fill="#f8fafc"/>',
   f'<text x="40" y="56" font-family="Arial,Apple SD Gothic Neo,sans-serif" font-size="30" font-weight="700" fill="{INK}">{safe(t["title"])}</text>',
   f'<text x="40" y="89" font-family="Arial,Apple SD Gothic Neo,sans-serif" font-size="17" fill="#48616d">{safe(t["lead"])}</text>']
 for i,(number,lab,bg) in enumerate(((50,t["accepted"],"#e0f3ec"),(39,t["missing"],"#f9eed7"),(11,t["excluded"],"#f6e5e1"))):
  x=40+i*367
  a+= [f'<rect x="{x}" y="106" width="342" height="62" rx="8" fill="{bg}"/>',
       f'<text x="{x+15}" y="144" font-size="28" font-weight="700" font-family="Arial,sans-serif" fill="#153e4d">{number}</text>',
       f'<text x="{x+89}" y="143" font-size="16" font-family="Arial,Apple SD Gothic Neo,sans-serif" fill="#27424f">{safe(lab)}</text>']
 for i,(label,step,cells) in enumerate(((t["fine"],10000,fine),(t["coarse"],50000,coarse))):
  left=40+548*i
  center=left+262
  pw=(xmax-xmin)*scale;ph=(ymax-ymin)*scale
  xs=center-pw/2;ys=228+(345-ph)/2
  a+= [f'<rect x="{left}" y="185" width="524" height="408" rx="9" fill="#ffffff" stroke="#dbe7ea"/>',
       f'<text x="{left+18}" y="222" font-size="23" font-weight="700" fill="{INK}" font-family="Arial,Apple SD Gothic Neo,sans-serif">{safe(label)}</text>',
       f'<text x="{left+504}" y="222" text-anchor="end" font-size="16" fill="#287282" font-family="Arial,Apple SD Gothic Neo,sans-serif">{len(cells)} {safe(t["occupied"])}</text>',
       f'<rect x="{xs:.2f}" y="{ys:.2f}" width="{pw:.2f}" height="{ph:.2f}" fill="#f1f5f7"/>']
  for x in range((xmin//50000)*50000,xmax+50000,50000):
   px=xs+(x-xmin)*scale
   if xs<=px<=xs+pw:a.append(f'<path d="M{px:.2f} {ys:.2f}v{ph:.2f}" stroke="#d6e3e8" stroke-width="0.7"/>')
  for y in range((ymin//50000)*50000,ymax+50000,50000):
   py=ys+(ymax-y)*scale
   if ys<=py<=ys+ph:a.append(f'<path d="M{xs:.2f} {py:.2f}h{pw:.2f}" stroke="#d6e3e8" stroke-width="0.7"/>')
  a.append(f'<g data-grid-km="{step//1000}" data-occupied-cells="{len(cells)}">')
  for (gx,gy),count in sorted(cells.items()):
   px=xs+(gx*step-xmin)*scale
   py=ys+(ymax-(gy+1)*step)*scale
   width=step*scale
   a.append(f'<rect x="{px:.2f}" y="{py:.2f}" width="{width:.2f}" height="{width:.2f}" fill="{color(count)}" stroke="#254d60" stroke-width="0.8" data-count="{count}"/>')
   if step==50000:
    fg="#ffffff" if count>=10 else "#123342"
    a.append(f'<text x="{px+width/2:.2f}" y="{py+width/2+5:.2f}" text-anchor="middle" font-size="13" font-weight="700" fill="{fg}" font-family="Arial,sans-serif">{count}</text>')
  a += ['</g>',f'<text x="{center}" y="578" text-anchor="middle" font-size="12" fill="#677d87" font-family="Arial,sans-serif">UTM zone 52N · aggregate cells</text>']
 a.append('<text x="40" y="616" font-size="14" fill="#415d68" font-family="Arial,Apple SD Gothic Neo,sans-serif">Records / cell:</text>')
 for i,label in enumerate(("1","2–4","5–9","10+")):
  xx=175+i*125
  a.append(f'<rect x="{xx}" y="601" width="21" height="17" fill="{COLORS[i]}" stroke="#254d60" stroke-width="0.5"/>')
  a.append(f'<text x="{xx+30}" y="615" font-size="14" fill="#415d68" font-family="Arial,sans-serif">{label}</text>')
 a += [f'<text x="40" y="641" font-size="17" font-weight="700" fill="{INK}" font-family="Arial,Apple SD Gothic Neo,sans-serif">{safe(t["note"])}</text>',
       f'<text x="40" y="666" font-size="13" fill="#596b79" font-family="Arial,Apple SD Gothic Neo,sans-serif">{safe(t["source"])}</text>',
       '</svg>']
 return "\n".join(a)+"\n"


def render_mobile(snapshot,lang):
    """Native 390px layout, not a scaled-down desktop chart."""
    t=LABELS[lang]
    fine=Counter({(int(a),int(b)):int(c) for a,b,c in snapshot['cells_10km']})
    coarse=Counter()
    for (gx,gy),n in fine.items():coarse[(gx//5,gy//5)]+=n
    assert len(fine)==12 and len(coarse)==8
    assert sum(fine.values())==sum(coarse.values())==50
    xmin=min(gx*step for step,cs in ((10000,fine),(50000,coarse)) for gx,gy in cs)
    xmax=max((gx+1)*step for step,cs in ((10000,fine),(50000,coarse)) for gx,gy in cs)
    ymin=min(gy*step for step,cs in ((10000,fine),(50000,coarse)) for gx,gy in cs)
    ymax=max((gy+1)*step for step,cs in ((10000,fine),(50000,coarse)) for gx,gy in cs)
    scale=min(210/(xmax-xmin),280/(ymax-ymin))
    safe=lambda v:escape(str(v),quote=True)
    a=[f'<svg xmlns="http://www.w3.org/2000/svg" width="390" height="1000" viewBox="0 0 390 1000" lang="{lang}" role="img" aria-labelledby="figtitle figdesc" data-source-sha256="{SOURCE_SHA}" data-selection-first-page-records="100" data-records-accepted="50" data-unknown-uncertainty="39" data-over-threshold="11">',
       f'<title id="figtitle">{safe(t["title"])}</title>',
       f'<desc id="figdesc">{safe(t["desc"])}</desc>',
       f'<metadata>Source {SOURCE_URL} commit {SOURCE_COMMIT}; derived aggregate only; unrepresentative first page, not an occurrence-download DOI.</metadata>',
       '<rect width="390" height="1000" rx="10" fill="#f8fafc"/>',
       f'<text x="17" y="35" font-family="Arial,Apple SD Gothic Neo,sans-serif" font-size="21" font-weight="700" fill="{INK}">{safe(t["title"])}</text>',
       f'<text x="17" y="59" font-family="Arial,Apple SD Gothic Neo,sans-serif" font-size="12" fill="#46606e">{"2024 GBIF · first 100 search records" if lang=="en" else "2024년 GBIF 첫 조회 100건"}</text>',
       f'<text x="17" y="76" font-family="Arial,Apple SD Gothic Neo,sans-serif" font-size="12" fill="#46606e">{"Illustrative 1 km uncertainty screen" if lang=="en" else "좌표 불확실성 예시 기준 1 km"}</text>']
    for i,(number,label,bg) in enumerate(((50,t['accepted'],'#e0f3ec'),(39,t['missing'],'#f9eed7'),(11,t['excluded'],'#f6e5e1'))):
        xx=12+127*i
        a += [f'<rect x="{xx}" y="91" width="112" height="55" rx="6" fill="{bg}"/>',
              f'<text x="{xx+9}" y="126" font-family="Arial,sans-serif" font-size="22" font-weight="700" fill="{INK}">{number}</text>',
              f'<text x="{xx+43}" y="122" font-family="Arial,Apple SD Gothic Neo,sans-serif" font-size="11" fill="#2c4b56">{safe(label)}</text>']
    for ystart,(label,step,counts) in ((161,(t['fine'],10000,fine)),(527,(t['coarse'],50000,coarse))):
        a.extend([f'<rect x="12" y="{ystart}" width="366" height="355" rx="9" fill="#ffffff" stroke="#dbe7ea"/>',
                  f'<text x="26" y="{ystart+35}" font-family="Arial,Apple SD Gothic Neo,sans-serif" font-size="19" font-weight="700" fill="{INK}">{safe(label)}</text>',
                  f'<text x="364" y="{ystart+35}" text-anchor="end" font-family="Arial,Apple SD Gothic Neo,sans-serif" font-size="15" fill="#267282">{len(counts)} {safe(t["occupied"])}</text>'])
        plotw=(xmax-xmin)*scale;ploth=(ymax-ymin)*scale
        xs=195-plotw/2;ys=ystart+48+(284-ploth)/2
        a.append(f'<rect x="{xs:.2f}" y="{ys:.2f}" width="{plotw:.2f}" height="{ploth:.2f}" fill="#f1f5f7"/>')
        a.append(f'<g data-grid-km="{step//1000}" data-occupied-cells="{len(counts)}">')
        for (gx,gy),c in sorted(counts.items()):
            x=xs+(gx*step-xmin)*scale
            y=ys+(ymax-(gy+1)*step)*scale
            w=step*scale
            a.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{w:.2f}" fill="{color(c)}" stroke="#254d60" stroke-width="0.65" data-count="{c}"/>')
            if step==50000:
                a.append(f'<text x="{x+w/2:.2f}" y="{y+w/2+4:.2f}" text-anchor="middle" font-size="12" font-weight="700" fill="{"#ffffff" if c>=10 else "#153549"}" font-family="Arial,sans-serif">{c}</text>')
        a.extend(['</g>',f'<text x="195" y="{ystart+343}" text-anchor="middle" font-family="Arial,sans-serif" font-size="12" fill="#667d86">UTM zone 52N</text>'])
    a.append('<text x="17" y="906" font-family="Arial,sans-serif" font-size="13" fill="#3c5866">Records / cell:</text>')
    for i,label in enumerate(('1','2–4','5–9','10+')):
        xx=132+i*61
        a.extend([f'<rect x="{xx}" y="894" width="17" height="17" fill="{COLORS[i]}" stroke="#254d60" stroke-width="0.5"/>',
                  f'<text x="{xx+20}" y="907" font-family="Arial,sans-serif" font-size="12" fill="#3c5866">{label}</text>'])
    note=('빈 칸은 새가 없다는 증거가 아닙니다.' if lang=='ko' else 'Blank does not mean species absence.')
    caution=('실제 조사 범위가 없는 비무작위 예시입니다.' if lang=='ko' else 'No sampling-effort layer; non-random page.')
    source=('원본: 파생 격자 · 관측 다운로드 DOI 없음' if lang=='ko' else 'Source: derived grids · no occurrence-download DOI')
    a += [f'<text x="17" y="943" font-family="Arial,Apple SD Gothic Neo,sans-serif" font-size="15" font-weight="700" fill="{INK}">{safe(note)}</text>',
          f'<text x="17" y="966" font-family="Arial,Apple SD Gothic Neo,sans-serif" font-size="13" fill="#506875">{safe(caution)}</text>',
          f'<text x="17" y="987" font-family="Arial,Apple SD Gothic Neo,sans-serif" font-size="12" fill="#506875">{safe(source)}</text>','</svg>']
    return '\n'.join(a)+'\n'

if __name__=="__main__":
 p=argparse.ArgumentParser()
 p.add_argument("--snapshot",type=Path,required=True)
 arg=p.parse_args()
 content=arg.snapshot.read_bytes()
 if sha256(content).hexdigest()!=SOURCE_SHA:raise SystemExit("SNAPSHOT_SOURCE_HASH_MISMATCH")
 snap=json.loads(content)
 OUT.mkdir(parents=True,exist_ok=True)
 for lang in ("ko","en"):
  for suffix,draw in (("",render),( "-mobile",render_mobile)):
   dest=OUT/("grid-comparison-"+lang+suffix+".svg")
   dest.write_text(draw(snap,lang),encoding="utf8")
   print(dest)
