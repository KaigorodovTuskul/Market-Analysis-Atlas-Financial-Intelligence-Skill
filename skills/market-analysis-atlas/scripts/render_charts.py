#!/usr/bin/env python3
"""Generate original illustrative SVGs; never download third-party illustrations."""
from __future__ import annotations
import json, math, random, html
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/terms.jsonl'
OUT=ROOT/'assets/charts'
PALETTES={'ink':'#152235','blue':'#2764d5','green':'#168c70','red':'#dc5261','grid':'#e5eaf0','slate':'#687a90'}
# Geometric waypoint diagrams. Independent original artwork with intentionally schematic scales.
CUSTOM={
'Head and Shoulders':[30,45,62,47,75,43,58,37,20],
'Inverse Head and Shoulders':[74,59,40,55,23,58,42,64,76,85],
'Double Top':[27,42,70,48,39,69,47,28,18],
'Double Bottom':[75,63,27,48,65,29,54,78,83],
'Triple Top':[25,60,45,62,43,61,42,21],
'Triple Bottom':[76,35,57,32,55,34,60,80],
'Rounding Top':[30,40,48,55,62,66,67,65,62,55,48,38,28],
'Rounding Bottom':[70,63,55,46,39,35,34,36,42,51,64,76,84],
'Cup and Handle':[72,65,52,42,37,40,49,62,72,66,64,74,84],
'Ascending Triangle':[35,63,45,64,51,64,56,64,61,80],
'Descending Triangle':[70,36,58,36,51,35,42,36,24],
'Symmetrical Triangle':[84,23,75,32,68,39,61,46,57,50,74],
'Rising Wedge':[16,48,32,56,46,61,54,64,59,52,40],
'Falling Wedge':[85,50,67,44,56,42,49,39,45,55,72],
'Bull Flag':[22,28,35,55,80,74,69,73,66,74,69,91],
'Bear Flag':[88,81,68,45,20,29,34,28,38,30,35,8],
'Bull Pennant':[15,24,36,76,70,75,72,73,72,85,95],
'Bear Pennant':[91,77,56,21,26,21,24,22,23,13,7],
'Rectangle Range':[54,70,45,70,45,71,46,71,48,81],
'Ascending Channel':[23,45,32,54,41,65,51,75,65,87],
'Descending Channel':[86,62,75,48,64,39,53,28,43,18],
'Horizontal Channel':[46,72,46,70,44,74,49,72,45,80],
'Broadening Formation':[48,60,43,68,34,81,23,91,18],
'Megaphone Pattern':[50,62,46,72,37,86,28,91,15],
'Diamond Top':[35,50,34,65,29,74,40,66,47,56,45,30],
'Diamond Bottom':[65,50,69,34,75,23,59,31,52,45,55,76],
'Island Reversal':[20,28,40,52,68,84,88,65,35,18],
'Gap Up':[30,38,44,48,49,77,73,81,86],
'Gap Down':[78,73,68,65,64,35,40,26,18],
'Breakaway Gap':[32,35,34,38,37,68,73,82,89],
'Runaway Gap':[20,29,38,49,51,71,78,83,94],
'Exhaustion Gap':[20,28,43,55,67,86,91,73,45],
'Dead Cat Bounce':[90,65,43,24,41,52,38,28,16],
'V Bottom':[82,69,49,18,42,68,84,93],
'V Top':[19,33,55,88,62,42,22,13],
'Bump and Run Reversal':[25,32,40,48,57,68,84,67,44,26],
'Three Drives Pattern':[20,41,34,59,45,77,60,87,68],
'ABCD Pattern':[18,66,39,81,58],
'Gartley Pattern':[70,25,49,37,64,41],
'Bat Pattern':[72,25,43,34,67,32],
'Butterfly Pattern':[68,23,49,36,81,53],
'Crab Pattern':[70,22,45,31,92,55],
'Shark Pattern':[70,31,58,19,84,39],
'Wolfe Wave':[26,62,34,71,45,82,55,91],
'Elliott Impulse Wave':[18,49,36,70,53,91],
'Elliott Corrective Wave':[85,46,67,38,53],
'Wyckoff Accumulation':[62,38,50,33,45,28,53,40,61,77,85],
'Wyckoff Distribution':[37,63,51,70,58,76,46,65,40,22,12],
'Spring (Wyckoff)':[51,63,44,63,46,64,29,55,77],
'Upthrust (Wyckoff)':[45,32,62,35,61,34,78,49,26],
'Breakout':[34,44,38,46,37,47,46,73,85],
'Breakdown':[74,64,72,65,70,63,61,37,24],
'Pullback':[22,36,50,70,62,53,70,82,91],
'Throwback':[24,34,46,56,72,59,58,78,91],
'Retest':[36,41,38,45,40,64,46,65,68,86],
'Bull Trap':[40,51,48,61,66,72,52,39,25],
'Bear Trap':[63,50,56,37,27,18,43,63,82],
'False Breakout':[50,54,49,55,60,75,57,49,53],
'Trendline Break':[17,29,44,55,66,72,60,45,26],
'Golden Cross':[29,40,44,47,56,60,63,71,81],
'Death Cross':[83,75,71,63,56,54,45,31,22],
'Support Level':[69,46,33,46,37,63,35,49,36,75],
'Resistance Level':[23,61,72,52,70,37,72,51,70,30],
}
# These triples are example candle OHLC values, not trading data.
CANDLE={
'Doji':[(40,80,20,41)],
'Long-Legged Doji':[(48,98,4,47)],
'Dragonfly Doji':[(75,79,5,76)],
'Gravestone Doji':[(23,95,20,24)],
'Hammer':[(60,70,5,67)],
'Hanging Man':[(66,72,8,68)],
'Inverted Hammer':[(32,93,24,38)],
'Shooting Star':[(35,95,27,31)],
'Bullish Engulfing':[(63,72,27,32),(24,81,18,78)],
'Bearish Engulfing':[(28,76,20,72),(78,84,14,21)],
'Bullish Harami':[(78,85,20,28),(37,68,34,62)],
'Bearish Harami':[(29,83,23,75),(67,69,37,42)],
'Harami Cross':[(78,85,20,28),(50,65,38,51)],
'Morning Star':[(82,90,36,42),(38,52,29,39),(42,88,38,83)],
'Evening Star':[(21,80,15,75),(76,86,65,73),(70,72,12,18)],
'Morning Doji Star':[(82,89,35,40),(38,47,25,39),(41,86,40,82)],
'Evening Doji Star':[(20,80,17,75),(77,87,66,78),(75,79,13,21)],
'Three White Soldiers':[(25,55,20,53),(46,70,42,68),(60,87,56,84)],
'Three Black Crows':[(83,87,54,56),(66,70,36,38),(48,53,15,17)],
'Piercing Pattern':[(80,86,25,29),(21,72,19,70)],
'Dark Cloud Cover':[(22,79,18,75),(82,86,30,35)],
'Tweezer Top':[(23,85,21,78),(79,85,27,30)],
'Tweezer Bottom':[(75,80,14,20),(19,72,14,68)],
'Marubozu':[(20,85,20,85)],
'Spinning Top':[(48,84,16,53)],
'Inside Bar':[(20,89,10,80),(48,68,34,52)],
'Outside Bar':[(48,65,36,50),(19,91,11,87)],
'Bullish Abandoned Baby':[(82,90,40,43),(27,33,19,27),(42,90,37,88)],
'Bearish Abandoned Baby':[(19,80,15,75),(89,95,82,88),(73,78,12,18)],
'Three Inside Up':[(79,86,21,26),(36,59,32,54),(54,86,51,82)],
'Three Inside Down':[(20,80,16,77),(65,69,42,47),(45,47,12,17)],
'Three Outside Up':[(65,70,27,29),(22,83,18,79),(72,95,66,91)],
'Three Outside Down':[(30,75,26,72),(81,88,17,21),(28,31,6,10)],
'Rising Three Methods':[(23,76,18,72),(68,72,55,61),(62,68,52,57),(56,64,48,53),(51,91,46,86)],
'Falling Three Methods':[(76,82,21,26),(29,44,25,40),(43,49,33,45),(46,54,37,50),(53,58,9,14)],
'Kicking Pattern':[(80,80,30,30),(38,86,38,86)],
'Belt Hold':[(22,86,22,78)],
}
def svg_start(title,subtitle):
 t=html.escape(title);s=html.escape(subtitle)
 return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 410" role="img" aria-label="{t}: original schematic chart">
<title>{t}</title><desc>Original educational diagram, synthetic data, not a prediction or chart of a real security.</desc>
<rect width="800" height="410" fill="#ffffff"/><rect x="34" y="28" width="732" height="348" rx="16" fill="#f8fafc" stroke="#dfe6ed"/>
<text x="60" y="66" font-family="Arial,sans-serif" font-size="23" font-weight="bold" fill="#152235">{t}</text>
<text x="60" y="90" font-family="Arial,sans-serif" font-size="12" fill="#687a90">{s}</text>
'''
def svg_end():return '<text x="60" y="362" fill="#687a90" font-family="Arial,sans-serif" font-size="12">Synthetic schematic · Not market data · Not a trading signal</text></svg>\n'
def poly(points):
 result=[]
 for i,p in enumerate(points):
  x=65+(i/(len(points)-1))*660
  y=317-p/100*198
  result.append((x,y))
 return ' '.join(f'{x:.1f},{y:.1f}' for x,y in result)
def pattern_svg(term):
 arr=CUSTOM[term]
 s=svg_start(term,'Price-structure illustration · relative level vs sequence')
 for y in (120,169,218,267,316): s+=f'<line x1="60" y1="{y}" x2="740" y2="{y}" stroke="#e5eaf0"/>'
 s+='<polyline points="'+poly(arr)+'" fill="none" stroke="#2764d5" stroke-width="4.2" stroke-linejoin="round" stroke-linecap="round"/>'
 if term in {'Ascending Triangle','Descending Triangle','Rectangle Range','Support Level','Resistance Level','Double Top','Double Bottom','Breakout','Breakdown','Bull Trap','Bear Trap'}:
  v=42 if term in {'Descending Triangle','Double Bottom','Support Level','Breakdown','Bear Trap'} else 70
  y=317-v/100*198
  s+=f'<line x1="65" y1="{y:.1f}" x2="725" y2="{y:.1f}" stroke="#dc5261" stroke-width="2" stroke-dasharray="7 7"/>'
 # Illustrative boundary pairs, not fitted statistical regressions.
 BOUNDS={
  'Ascending Triangle':[(190,190),(247,192)],
  'Descending Triangle':[(178,232),(246,246)],
  'Symmetrical Triangle':[(150,209),(269,211)],
  'Ascending Channel':[(255,123),(295,163)],
  'Descending Channel':[(150,271),(185,306)],
  'Rising Wedge':[(224,188),(286,199)],
  'Falling Wedge':[(148,226),(218,243)],
 }
 if term in BOUNDS:
  for left,right in BOUNDS[term]:
   s+=f'<path d="M65 {left} L700 {right}" stroke="#168c70" stroke-width="2" stroke-dasharray="5 6" fill="none" opacity=".8"/>'
 s+=svg_end()
 return s

def candle_svg(term):
 candles=CANDLE[term]
 s=svg_start(term,'Original OHLC sketch · green = close above open')
 for y in (120,170,220,270,320):s+=f'<line x1="60" y1="{y}" x2="740" y2="{y}" stroke="#e5eaf0"/>'
 spacing=640/max(5,len(candles)+1)
 # Center one or multiple candles for visual legibility.
 gap=min(95,590/max(len(candles),1));x0=400-gap*(len(candles)-1)/2
 for i,(op,hi,lo,cl) in enumerate(candles):
  x=x0+i*gap
  yy=lambda v:316-v*2.07
  color='#168c70' if cl>=op else '#dc5261'
  s+=f'<line x1="{x:.1f}" y1="{yy(hi):.1f}" x2="{x:.1f}" y2="{yy(lo):.1f}" stroke="{color}" stroke-width="3.1"/>'
  top=min(yy(op),yy(cl));height=max(5,abs(yy(op)-yy(cl)))
  s+=f'<rect x="{x-19:.1f}" y="{top:.1f}" width="38" height="{height:.1f}" rx="2" fill="{color}"/>'
 s+=svg_end();return s

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 terms=[json.loads(x) for x in DATA.read_text(encoding='utf-8').splitlines()]
 examples=[]
 for record in terms:
  cat=record['category'];term=record['term']
  if cat not in ('chart_patterns','candlesticks'):continue
  if cat=='chart_patterns' and term not in CUSTOM:raise SystemExit('missing chart geometry: '+term)
  if cat=='candlesticks' and term not in CANDLE:raise SystemExit('missing candle geometry: '+term)
  svg=pattern_svg(term) if cat=='chart_patterns' else candle_svg(term)
  dest=OUT/(record['id']+'.svg');dest.write_text(svg,encoding='utf-8')
  examples.append({'id':record['id'],'term':term,'category':cat,'image':'../assets/charts/'+dest.name,'kind':'original_schematic',
                   'warning':'Stylized illustration; not real price data and not a validated pattern detector.'})
 (ROOT/'data/patterns.json').write_text(json.dumps(examples,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 print('Generated',len(examples),'original SVG diagrams')
if __name__=='__main__':main()
