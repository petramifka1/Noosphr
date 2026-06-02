#!/usr/bin/env python3
"""Regenerate the noosphr logo kit. No uploads needed.
Usage:  python3 make_logo.py [output_dir]   (default: ./public/noosphr-logo)
Requires internet (downloads the Jost font from Google Fonts on GitHub).
"""
import os, sys, json, tempfile, urllib.request, subprocess

OUT = sys.argv[1] if len(sys.argv) > 1 else "public/noosphr-logo"
os.makedirs(OUT, exist_ok=True)

def pipinstall(pkg):
    subprocess.run([sys.executable,"-m","pip","install",pkg,"-q",
                    "--break-system-packages"], check=False)

try:
    import fontTools  # noqa
except ImportError:
    pipinstall("fonttools")

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

FONT_URL = "https://raw.githubusercontent.com/google/fonts/main/ofl/jost/Jost%5Bwght%5D.ttf"
ttf = os.path.join(tempfile.gettempdir(), "Jost-noosphr.ttf")
if not os.path.exists(ttf):
    urllib.request.urlretrieve(FONT_URL, ttf)

UPM = 1000
def instance(w):
    f = TTFont(ttf); instantiateVariableFont(f, {"wght": w}, inplace=True); return f
def string_path(font, text, ls=0):
    gs=font.getGlyphSet(); hmtx=font["hmtx"]; cmap=font.getBestCmap()
    pen=SVGPathPen(gs); bp=BoundsPen(gs); x=0
    for ch in text:
        gn=cmap[ord(ch)]; adv=hmtx[gn][0]
        gs[gn].draw(TransformPen(pen,(1,0,0,1,x,0)))
        gs[gn].draw(TransformPen(bp,(1,0,0,1,x,0)))
        x+=adv+ls
    return pen.getCommands(), x-ls, bp.bounds

fw=instance(360); WORD_D,_,WB = string_path(fw,"noosphr",int(0.10*UPM))
fn=instance(440); N_D,_,NB   = string_path(fn,"n",0)

WHITE="#FFFFFF"; BLACK="#0A0A0A"
CX,CY,R,RING="50","50","34","3.2"
NXH=44.0; s_n=NXH/(NB[3]-NB[1]); n_cx=(NB[0]+NB[2])/2; n_cy=(NB[1]+NB[3])/2
tx_n=50-s_n*n_cx; ty_n=50+s_n*n_cy
s_w=60.0/470.0
W_inkW=(WB[2]-WB[0])*s_w; W_asc=WB[3]*s_w; W_desc=-WB[1]*s_w; W_h=W_asc+W_desc

def icon_inner(c):
    return (f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="{c}" stroke-width="{RING}"/>'
            f'<g transform="translate({tx_n:.4f},{ty_n:.4f}) scale({s_n:.6f},{-s_n:.6f})">'
            f'<path d="{N_D}" fill="{c}"/></g>')
def wm_group(X0,Yb,c):
    return (f'<g transform="translate({X0-s_w*WB[0]:.4f},{Yb:.4f}) scale({s_w:.6f},{-s_w:.6f})">'
            f'<path d="{WORD_D}" fill="{c}"/></g>')
def svg(w,h,body,title="noosphr"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.1f}" height="{h:.1f}" '
            f'viewBox="0 0 {w:.2f} {h:.2f}" role="img"><title>{title}</title>{body}</svg>')
def icon(c,s=512): return svg(s,s,icon_inner(c)).replace(f'width="512.0" height="512.0"',f'width="{s}" height="{s}"')
def wordmark(c,p=10):
    cw=W_inkW+2*p; ch=W_h+2*p; return svg(cw,ch,wm_group(p,p+W_asc,c))
def stacked(c,d=150,gap=40,p=40):
    cw=max(d,W_inkW)+2*p; ch=p+d+gap+W_h+p; ix=(cw-d)/2; sc=d/100
    g=f'<g transform="translate({ix:.3f},{p}) scale({sc:.5f})">{icon_inner(c)}</g>'
    return svg(cw,ch,g+wm_group((cw-W_inkW)/2,p+d+gap+W_asc,c))
def horizontal(c,d=128,gap=34,p=34):
    cw=p+d+gap+W_inkW+p; ch=p+max(d,W_h)+p; mid=ch/2; sc=d/100
    g=f'<g transform="translate({p},{mid-d/2:.3f}) scale({sc:.5f})">{icon_inner(c)}</g>'
    return svg(cw,ch,g+wm_group(p+d+gap,mid+235.0*s_w,c))
def favicon(s=512):
    bg=f'<rect width="100" height="100" rx="22" fill="{BLACK}"/>'
    return svg(s,s,bg+icon_inner(WHITE))

files={
 "noosphr-icon-white.svg":icon(WHITE),"noosphr-icon-black.svg":icon(BLACK),
 "noosphr-wordmark-white.svg":wordmark(WHITE),"noosphr-wordmark-black.svg":wordmark(BLACK),
 "noosphr-logo-stacked-white.svg":stacked(WHITE),"noosphr-logo-stacked-black.svg":stacked(BLACK),
 "noosphr-logo-horizontal-white.svg":horizontal(WHITE),"noosphr-logo-horizontal-black.svg":horizontal(BLACK),
 "noosphr-favicon.svg":favicon(),
}
for n,s in files.items(): open(os.path.join(OUT,n),"w").write(s)
print(f"Wrote {len(files)} SVGs to {OUT}/")

# PNG favicons (optional; needs cairosvg). Skips gracefully if unavailable.
try:
    import cairosvg
except ImportError:
    pipinstall("cairosvg")
    try: import cairosvg
    except Exception: cairosvg=None
if cairosvg:
    try:
        for px in (32,180,512):
            cairosvg.svg2png(url=os.path.join(OUT,"noosphr-favicon.svg"),
                write_to=os.path.join(OUT,f"noosphr-favicon-{px}.png"),
                output_width=px,output_height=px)
        print("Wrote favicon PNGs (32, 180, 512).")
    except Exception as e:
        print("PNG step skipped:",e)
else:
    print("cairosvg unavailable - SVG favicon written; generate PNGs separately if needed.")
