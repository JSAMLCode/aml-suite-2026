import re, json, os, sys
P = sys.argv[1]
sb = open(os.path.join(P,'STORYBOARD.md')).read()
script = open(os.path.join(P,'SCRIPT.md')).read()
lines = re.findall(r'\n\n    (.+)\n', script)
durs = [float(x) for x in re.findall(r'- duration: ([\d.]+)s', sb)]
assert len(lines)==8 and len(durs)==9, (len(lines),len(durs))
starts=[sum(durs[:k]) for k in range(9)]
TOTAL=sum(durs)
GOLD='#D9B26A'

def cue(i, phrase, lead=0.15):
    t = lines[i].lower(); k = t.find(phrase.lower())
    assert k>=0, (i, phrase)
    # proportional to character position, minus a short lead
    return round(max(0.05, durs[i]*k/len(t) - lead), 2)

FONT = "@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');"
SG = "font-family:'Space Grotesk',Inter,sans-serif;"

def base_css(fid):
    return f"""{FONT}
#root{{position:absolute;inset:0;width:1080px;height:1080px;overflow:hidden;font-family:Inter,sans-serif;color:#fff}}
.{fid}-bg{{position:absolute;inset:0;background:radial-gradient(120% 90% at 70% 20%,#0f3a5c 0%,#051C2C 55%,#030F18 100%)}}
.{fid}-grid{{position:absolute;inset:-60px;background-image:linear-gradient(rgba(255,255,255,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.045) 1px,transparent 1px);background-size:43px 43px;-webkit-mask-image:radial-gradient(60% 60% at 50% 45%,#000 20%,transparent 100%);mask-image:radial-gradient(60% 60% at 50% 45%,#000 20%,transparent 100%)}}
.{fid}-stage{{position:absolute;inset:0}}
.{fid}-a{{position:absolute}}
.{fid}-D{{{SG}letter-spacing:-.02em;line-height:1.12}}
.{fid}-ey{{position:absolute;left:65px;top:76px;{SG}text-transform:uppercase;letter-spacing:.08em;color:#2FB8FF;font-weight:600;font-size:30px}}
.{fid}-tg{{position:absolute;right:65px;top:70px;border:1px solid rgba(169,188,204,.3);color:#A9BCCC;border-radius:100px;font-size:26px;padding:8px 24px}}
.{fid}-at{{position:absolute;left:65px;width:930px;top:150px;{SG}font-weight:600;letter-spacing:-.02em;line-height:1.14;font-size:62px}}
.{fid}-at .{fid}-k{{color:#2FB8FF}}
.{fid}-w{{display:inline-block}}
.{fid}-src{{position:absolute;left:65px;top:982px;font-size:22px;color:#6F8799}}
.{fid}-hudt{{position:absolute;left:65px;top:26px;display:flex;align-items:center;gap:12px;{SG}font-size:17px;font-weight:600;letter-spacing:.16em;color:#A9BCCC;text-transform:uppercase}}
.{fid}-hudt i{{display:inline-block;width:9px;height:9px;border-radius:50%;background:#FF5C6C}}
.{fid}-tc{{position:absolute;right:65px;top:26px;{SG}font-size:17px;font-weight:600;letter-spacing:.14em;color:#A9BCCC}}
.{fid}-hudb{{position:absolute;left:65px;top:1036px;{SG}font-size:15px;font-weight:600;letter-spacing:.16em;color:#6F8799;text-transform:uppercase}}
.{fid}-ptrack{{position:absolute;right:65px;top:1044px;width:300px;height:2px;background:rgba(169,188,204,.18)}}
.{fid}-pfill{{position:absolute;left:0;top:0;width:100%;height:100%;background:#D9B26A;transform-origin:0 50%;box-shadow:0 0 10px rgba(217,178,106,.6)}}
.{fid}-pg{{position:absolute;left:0;bottom:0;height:5px;background:#2FB8FF;transform-origin:0 50%}}
.{fid}-glass{{position:absolute;background:linear-gradient(160deg,rgba(255,255,255,.08),rgba(255,255,255,.02));border:1px solid rgba(169,188,204,.24);border-radius:22px}}
.{fid}-glow{{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(34,81,255,.55),transparent 65%)}}
.{fid}-nd{{position:absolute;display:flex;align-items:center;justify-content:center;text-align:center;{SG}font-weight:500;color:#fff;padding:0 14px;box-sizing:border-box}}
.{fid}-sweep{{position:absolute;top:-20%;width:180px;height:140%;background:linear-gradient(90deg,transparent,rgba(255,255,255,.10),transparent);transform:rotate(18deg)}}
"""

def words(fid, text, keys=()):
    out=[]
    for w in text.split(' '):
        cls=f"{fid}-w" + (f" {fid}-k" if any(k in w for k in keys) else "")
        out.append(f'<span class="{cls}">{w}</span>')
    return ' '.join(out)

def wrap(fid, dur, css, body, js, final=False):
    return f"""<template>
<style>
{base_css(fid)}{css}
</style>
<div id="root" data-composition-id="{fid}" data-width="1080" data-height="1080" data-duration="{dur}">
<div class="clip {fid}-bg" id="{fid}-bgclip" data-start="0" data-duration="{dur}" data-track-index="0"></div>
<div class="{fid}-stage" id="{fid}-stage">
<div class="{fid}-grid" id="{fid}-grid"></div>
{body}
</div>
</div>
<script src="assets/vendor/gsap.min.js"></script>
<script>
(function(){{
const D={dur};
const tl=gsap.timeline({{paused:true}});
const q=(s)=>document.querySelectorAll(s);
tl.fromTo("#{fid}-grid",{{x:0,y:0}},{{x:-43,y:-22,duration:D,ease:"none"}},0);
{js}
window.__timelines["{fid}"]=tl;
}})();
</script>
</template>
"""

def hdr(fid, ey, tg=None):
    s=f'<div class="{fid}-ey" id="{fid}-ey">{ey}</div>'
    if tg: s+=f'<div class="{fid}-tg" id="{fid}-tg">{tg}</div>'
    return s
def hdr_js(fid, tg_t=0.15):
    return (f'tl.fromTo("#{fid}-ey",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:.5,ease:"power3.out"}},0.05);\n'
            f'if(document.getElementById("{fid}-tg"))tl.fromTo("#{fid}-tg",{{opacity:0,y:-10}},{{opacity:1,y:0,duration:.5,ease:"back.out(2)"}},{tg_t});\n')
def title_js(fid, start=0.15, span=1.6):
    return f'tl.fromTo(q("#{fid}-at .{fid}-w"),{{opacity:0,y:28,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.55,ease:"power3.out",stagger:{{amount:{span}}}}},{start});\n'
def pg(fid, a, b, D):
    k=globals()['i']; st=starts[k]
    html=(f'<div class="{fid}-hudt" id="{fid}-hudt"><i></i>José Antonio Serrano · AML · Cumplimiento · GRC</div>'
          f'<div class="{fid}-tc" id="{fid}-tc">00:00:00</div>'
          f'<div class="{fid}-hudb" id="{fid}-hudb">Acuerdo SBP 1-2026 · Arts. 14 y 53</div>'
          f'<div class="{fid}-ptrack"><div class="{fid}-pfill" id="{fid}-pfill"></div></div>')
    js=(f'tl.fromTo("#{fid}-pfill",{{scaleX:{st/TOTAL:.4f}}},{{scaleX:{min(1,(st+D)/TOTAL):.4f},duration:D,ease:"none"}},0);\n'
        f'const tcp={{v:{st:.3f}}};const tce=document.getElementById("{fid}-tc");'
        f'const fmt=(x)=>{{const f=Math.floor((x%1)*30),s=Math.floor(x)%60,m=Math.floor(x/60);return [m,s,f].map(n=>String(n).padStart(2,"0")).join(":")}};'
        f'tl.fromTo(tcp,{{v:{st:.3f}}},{{v:{st+D:.3f},duration:D,ease:"none",onUpdate:()=>{{tce.textContent=fmt(tcp.v)}}}},0);\n')
    return html,js

def globe(fid, gid, size, pin=False, op=1.0):
    r=size/2-4; c=size/2; parts=[]
    parts.append(f'<circle cx="{c}" cy="{c}" r="{r}" fill="rgba(34,81,255,.10)" stroke="rgba(47,184,255,.75)" stroke-width="2"/>')
    for k,rx in enumerate([0.25,0.55,0.82]):
        parts.append(f'<ellipse cx="{c}" cy="{c}" rx="{r*rx:.1f}" ry="{r}" fill="none" stroke="rgba(47,184,255,.32)" stroke-width="1.2"/>')
    for k,yy in enumerate([-0.6,-0.3,0,0.3,0.6]):
        w=(1-yy*yy)**.5*r
        parts.append(f'<ellipse cx="{c}" cy="{c+yy*r:.1f}" rx="{w:.1f}" ry="{w*0.14:.1f}" fill="none" stroke="rgba(47,184,255,.28)" stroke-width="1.1"/>')
    import math
    pts=[(0.2,-0.35),(-0.35,-0.1),(0.45,0.15),(-0.1,0.4),(0.1,0.05),(-0.5,0.3),(0.3,-0.6),(0.55,-0.25),(-0.25,-0.55),(0.0,-0.2)]
    for k,(x,y) in enumerate(pts):
        parts.append(f'<circle class="{fid}-gd" cx="{c+x*r:.1f}" cy="{c+y*r:.1f}" r="{2.6 if k%3 else 3.6}" fill="{GOLD if k%4==0 else "#2FB8FF"}"/>')
    if pin:
        px,py=c+0.12*r,c-0.12*r
        parts.append(f'<g id="{gid}-pin"><circle cx="{px:.1f}" cy="{py:.1f}" r="{r*0.16:.1f}" fill="none" stroke="{GOLD}" stroke-width="2" opacity=".6"/>'
                     f'<path d="M{px:.1f} {py+r*0.11:.1f} C {px-r*0.09:.1f} {py:.1f}, {px-r*0.09:.1f} {py-r*0.1:.1f}, {px:.1f} {py-r*0.1:.1f} C {px+r*0.09:.1f} {py-r*0.1:.1f}, {px+r*0.09:.1f} {py:.1f}, {px:.1f} {py+r*0.11:.1f} Z" fill="{GOLD}"/>'
                     f'<circle cx="{px:.1f}" cy="{py-r*0.02:.1f}" r="{r*0.03:.1f}" fill="#051C2C"/></g>')
    return f'<svg id="{gid}" width="{size}" height="{size}" viewBox="0 0 {size} {size}" style="position:absolute;opacity:{op}">{"".join(parts)}</svg>'

def rays(fid, rid, cx, cy, size, op=.5):
    return (f'<div id="{rid}" style="position:absolute;left:{cx-size/2}px;top:{cy-size/2}px;width:{size}px;height:{size}px;border-radius:50%;opacity:{op};'
            f'background:repeating-conic-gradient(from 0deg,rgba(120,180,255,.13) 0deg 3deg,transparent 3deg 14deg);'
            f'-webkit-mask-image:radial-gradient(circle,#000 8%,transparent 70%);mask-image:radial-gradient(circle,#000 8%,transparent 70%)"></div>')

files={}
# ---------- 01 ----------
i=0; fid='01-fecha'; D=durs[i]
pgh,pgj=pg(fid,0,.12,D)
body=f"""{rays(fid,fid+'-rays',540,540,1500,.55)}<div class="{fid}-glow" id="{fid}-glow" style="left:190px;top:200px;width:700px;height:700px"></div>
<div class="{fid}-a" style="left:240px;top:240px;width:600px;height:600px">{globe(fid,fid+'-globe',600,False,.45)}</div>
<div class="{fid}-a {fid}-ring" id="{fid}-r1" style="left:110px;top:90px;width:860px;height:860px"></div>
<div class="{fid}-a {fid}-ring" id="{fid}-r2" style="left:230px;top:210px;width:620px;height:620px"></div>
<div class="{fid}-a {fid}-ring" id="{fid}-r3" style="left:350px;top:330px;width:380px;height:380px"></div>
{hdr(fid,'Acuerdo 1-2026 · SBP','PBC')}
<div class="{fid}-a {fid}-D" id="{fid}-dm" style="left:0;right:0;top:250px;text-align:center;font-weight:700;font-size:160px">30 · 06</div>
<div class="{fid}-a {fid}-D" id="{fid}-yr" style="left:0;right:0;top:470px;text-align:center;font-weight:700;font-size:270px;color:#2FB8FF;line-height:1">2027</div>
<div class="{fid}-a" id="{fid}-sub" style="left:0;right:0;top:800px;text-align:center;font-size:38px;color:#A9BCCC;font-weight:500">Plazo para incorporar la geolocalización inferencial</div>
{pgh}"""
css=f".{fid}-ring{{border-radius:50%;border:1.5px solid rgba(47,184,255,.28)}}"
js=hdr_js(fid)+pgj+f"""
tl.fromTo("#{fid}-stage",{{scale:1}},{{scale:1.06,duration:D,ease:"none",transformOrigin:"50% 52%"}},0);
tl.fromTo("#{fid}-rays",{{rotation:0,opacity:0}},{{rotation:25,opacity:.55,duration:D,ease:"none"}},0);
tl.fromTo("#{fid}-globe",{{rotation:-8,scale:.9}},{{rotation:8,scale:1.02,duration:D,ease:"none"}},0);
tl.fromTo(["#{fid}-r3","#{fid}-r2","#{fid}-r1"],{{scale:.4,opacity:0}},{{scale:1,opacity:1,duration:1.4,ease:"expo.out",stagger:.18}},0);
tl.fromTo("#{fid}-glow",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:1.6,ease:"power2.out"}},0);
tl.fromTo("#{fid}-dm",{{opacity:0,y:40,scale:1.08}},{{opacity:1,y:0,scale:1,duration:.8,ease:"power4.out"}},0.1);
const yr={{v:1990}}; const el=document.getElementById("{fid}-yr");
tl.fromTo("#{fid}-yr",{{opacity:0,scale:.85}},{{opacity:1,scale:1,duration:.7,ease:"back.out(1.6)"}},0.35);
tl.fromTo(yr,{{v:1990}},{{v:2027,duration:1.1,ease:"power3.out",onUpdate:()=>{{el.textContent=Math.round(yr.v)}}}},0.35);
tl.fromTo("#{fid}-sub",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.6,ease:"power3.out"}},{cue(i,'ese es el plazo',0.6)});
"""
files[fid]=wrap(fid,D,css,body,js)

# ---------- 02 ----------
i=1; fid='02-no-opcional'; D=durs[i]
pgh,pgj=pg(fid,.12,.25,D)
tflip=cue(i,'ya no es opcional',0.1)
body=f"""{hdr(fid,'Art. 53','Apertura digital o remota')}
<div class="{fid}-at" id="{fid}-at">{words(fid,'Para los bancos con apertura digital o remota, la geolocalización inferencial ya no es opcional',())}</div>
<div class="{fid}-glass" id="{fid}-card" style="left:65px;top:600px;width:950px;height:250px;overflow:hidden"><div class="{fid}-sweep" id="{fid}-sweep" style="left:-240px"></div></div>
<div class="{fid}-a {fid}-D" id="{fid}-l1" style="left:110px;top:650px;font-size:34px;color:#6F8799">ANTES</div>
<div class="{fid}-a {fid}-D" id="{fid}-l2" style="left:110px;top:705px;font-size:62px;color:#A9BCCC">Opcional<div id="{fid}-strike" style="position:absolute;left:0;top:52%;height:4px;width:100%;background:#FF5C6C;transform-origin:0 50%"></div></div>
<div class="{fid}-a" id="{fid}-tog" style="left:470px;top:700px;width:140px;height:68px;border-radius:100px;background:#24384a">
  <div id="{fid}-knob" style="position:absolute;left:8px;top:8px;width:52px;height:52px;border-radius:50%;background:#fff"></div></div>
<div class="{fid}-a {fid}-D" id="{fid}-r1" style="left:670px;top:650px;font-size:34px;color:#2FB8FF">AHORA</div>
<div class="{fid}-a {fid}-D" id="{fid}-r2" style="left:670px;top:705px;font-size:62px;font-weight:700">Obligatorio</div>
<div class="{fid}-src" id="{fid}-src">Fuente: Acuerdo 1-2026 SBP, art. 53</div>
{pgh}"""
js=hdr_js(fid,cue(i,'digitales o remotos'))+pgj+title_js(fid,0.15,2.2)+f"""
tl.fromTo("#{fid}-card",{{opacity:0,y:50}},{{opacity:1,y:0,duration:.8,ease:"power3.out"}},{cue(i,'obliga')});
tl.fromTo(["#{fid}-l1","#{fid}-l2","#{fid}-tog"],{{opacity:0,y:20}},{{opacity:1,y:0,duration:.6,ease:"power3.out",stagger:.12}},{cue(i,'obliga')+0.3});
tl.fromTo(["#{fid}-r1","#{fid}-r2"],{{opacity:0,x:-10}},{{opacity:.18,x:0,duration:.6,ease:"power2.out"}},{cue(i,'obliga')+0.5});
tl.fromTo("#{fid}-src",{{opacity:0}},{{opacity:1,duration:.6}},{cue(i,'incorporar')});
tl.fromTo("#{fid}-knob",{{x:0}},{{x:72,duration:.45,ease:"back.out(2)"}},{tflip});
tl.fromTo("#{fid}-tog",{{backgroundColor:"#24384a"}},{{backgroundColor:"#2251FF",duration:.3}},{tflip});
tl.fromTo("#{fid}-strike",{{scaleX:0}},{{scaleX:1,duration:.4,ease:"power2.inOut"}},{tflip});
tl.fromTo("#{fid}-l2",{{opacity:1}},{{opacity:.5,duration:.4}},{tflip});
tl.fromTo(["#{fid}-r1","#{fid}-r2"],{{opacity:.18,scale:.96}},{{opacity:1,scale:1,duration:.5,ease:"back.out(2)",transformOrigin:"0% 50%"}},{tflip+0.1});
tl.fromTo("#{fid}-sweep",{{x:0}},{{x:1400,duration:.9,ease:"power2.inOut"}},{tflip+0.05});
tl.fromTo(q("#{fid}-at .{fid}-w"),{{color:"#ffffff"}},{{color:(k)=>k>=11?"#2FB8FF":"#ffffff",duration:.4}},{tflip});
"""
files[fid]=wrap(fid,D,"",body,js)

# ---------- 03 ----------
i=2; fid='03-definicion'; D=durs[i]
pgh,pgj=pg(fid,.25,.38,D)
body=f"""{hdr(fid,'Art. 14','Fuente primaria de riesgo')}
<div class="{fid}-at" id="{fid}-at">{words(fid,'Se estima dónde está el solicitante y su dispositivo, sin coordenadas físicas directas',())}</div>
<div class="{fid}-glass" id="{fid}-panel" style="left:65px;top:470px;width:950px;height:460px;overflow:hidden">
  <div id="{fid}-dots" style="position:absolute;inset:-60px;background-image:radial-gradient(rgba(169,188,204,.38) 1.6px,transparent 2.2px);background-size:28px 28px"></div>
  <div class="{fid}-glow" id="{fid}-h1" style="left:110px;top:60px;width:340px;height:340px"></div>
  <div class="{fid}-glow" id="{fid}-h2" style="left:520px;top:40px;width:320px;height:320px"></div>
  <div id="{fid}-c1" style="position:absolute;left:170px;top:120px;width:220px;height:220px;border-radius:50%;border:2px dashed rgba(47,184,255,.7)"></div>
  <div id="{fid}-c2" style="position:absolute;left:575px;top:95px;width:210px;height:210px;border-radius:50%;border:2px dashed rgba(47,184,255,.7)"></div>
  <div id="{fid}-p1" style="position:absolute;left:265px;top:215px;width:30px;height:30px;border-radius:50%;background:#2FB8FF"></div>
  <div id="{fid}-p2" style="position:absolute;left:665px;top:185px;width:30px;height:30px;border-radius:50%;background:#2FB8FF"></div>
  <div class="{fid}-D" id="{fid}-t1" style="position:absolute;left:160px;top:360px;width:240px;text-align:center;font-size:32px;color:#A9BCCC">Solicitante</div>
  <div class="{fid}-D" id="{fid}-t2" style="position:absolute;left:560px;top:330px;width:240px;text-align:center;font-size:32px;color:#A9BCCC">Dispositivo</div>
  <div id="{fid}-gps" style="position:absolute;right:28px;top:24px;display:flex;align-items:center;gap:10px;font-size:26px;color:#FF5C6C;{SG}font-weight:500">
    <svg width="34" height="34" viewBox="0 0 34 34"><circle cx="17" cy="17" r="10" fill="none" stroke="#FF5C6C" stroke-width="2.5"/><line x1="17" y1="1" x2="17" y2="9" stroke="#FF5C6C" stroke-width="2.5"/><line x1="17" y1="25" x2="17" y2="33" stroke="#FF5C6C" stroke-width="2.5"/><line x1="1" y1="17" x2="9" y2="17" stroke="#FF5C6C" stroke-width="2.5"/><line x1="25" y1="17" x2="33" y2="17" stroke="#FF5C6C" stroke-width="2.5"/><line x1="4" y1="30" x2="30" y2="4" stroke="#FF5C6C" stroke-width="3"/></svg>
    Sin coordenadas GPS</div>
</div>
<div class="{fid}-src" id="{fid}-src">Fuente: Acuerdo 1-2026 SBP, art. 14</div>
{pgh}"""
ts=cue(i,'solicitante'); td=cue(i,'dispositivo'); tg=cue(i,'sin necesidad')
js=hdr_js(fid,cue(i,'fuente primaria'))+pgj+title_js(fid,0.15,2.0)+f"""
tl.fromTo("#{fid}-panel",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.9,ease:"power3.out"}},0.6);
tl.fromTo("#{fid}-dots",{{x:0,y:0,scale:1.08}},{{x:-50,y:-30,scale:1,duration:D,ease:"none"}},0);
tl.fromTo("#{fid}-src",{{opacity:0}},{{opacity:1,duration:.6}},1.2);
tl.fromTo(["#{fid}-h1","#{fid}-c1"],{{opacity:0,scale:1.8}},{{opacity:1,scale:1,duration:1.1,ease:"expo.out"}},{ts});
tl.fromTo(["#{fid}-p1","#{fid}-t1"],{{opacity:0,scale:.3}},{{opacity:1,scale:1,duration:.6,ease:"back.out(2.5)"}},{ts+0.3});
tl.fromTo(["#{fid}-h2","#{fid}-c2"],{{opacity:0,scale:1.8}},{{opacity:1,scale:1,duration:1.1,ease:"expo.out"}},{td});
tl.fromTo(["#{fid}-p2","#{fid}-t2"],{{opacity:0,scale:.3}},{{opacity:1,scale:1,duration:.6,ease:"back.out(2.5)"}},{td+0.3});
tl.fromTo(["#{fid}-c1","#{fid}-c2"],{{rotation:0}},{{rotation:40,duration:D-{ts},ease:"none"}},{ts});
tl.fromTo("#{fid}-gps",{{opacity:0,x:20}},{{opacity:1,x:0,duration:.6,ease:"power3.out"}},{tg});
tl.fromTo(["#{fid}-c1","#{fid}-c2"],{{scale:1}},{{scale:1.12,duration:.9,ease:"sine.inOut"}},{tg+0.3});
tl.to(["#{fid}-c1","#{fid}-c2"],{{scale:1,duration:.9,ease:"sine.inOut"}},{tg+1.2});
"""
files[fid]=wrap(fid,D,"",body,js)

# ---------- 04 ----------
i=3; fid='04-senales'; D=durs[i]
pgh,pgj=pg(fid,.38,.5,D)
nodes=[('Dirección IP','dirección ip',65,420,270,116),('Tipo de red','tipo de red',65,560,270,116),('Proveedor de internet','proveedor',65,700,270,116),
       ('VPN','vpn',745,420,270,116),('Proxies','proxies',745,560,270,116),('Redes de anonimización','anonimización',745,700,270,116),
       ('Zona horaria','zona horaria',220,860,300,96),('Configuración regional','configuración regional',560,860,300,96)]
hx,hy=540,620
svg_lines=[];nb=[];nj=[]
for k,(lab,ph,x,y,w,h) in enumerate(nodes):
    cx=x+w/2; cy=y+h/2
    ex = x+w if x<hx-100 else (x if x>hx+100 else cx)
    ey = cy if (x<hx-100 or x>hx+100) else y
    L=((ex-hx)**2+(ey-hy)**2)**.5
    svg_lines.append(f'<line id="{fid}-ln{k}" x1="{hx}" y1="{hy}" x2="{ex:.0f}" y2="{ey:.0f}" stroke="#2FB8FF" stroke-opacity=".55" stroke-width="2" stroke-dasharray="{L:.0f}" stroke-dashoffset="{L:.0f}"/>')
    nb.append(f'<div class="{fid}-glass {fid}-nd" id="{fid}-n{k}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;font-size:31px">{lab}</div>')
    t=cue(i,ph,0.2)
    nj.append(f'tl.fromTo("#{fid}-ln{k}",{{attr:{{"stroke-dashoffset":{L:.0f}}}}},{{attr:{{"stroke-dashoffset":0}},duration:.45,ease:"power2.out"}},{t});')
    nj.append(f'tl.fromTo("#{fid}-n{k}",{{opacity:0,scale:.8}},{{opacity:1,scale:1,duration:.45,ease:"back.out(2)"}},{t+0.15});')
    nj.append(f'tl.fromTo("#{fid}-hub",{{scale:1.08}},{{scale:1,duration:.35,ease:"power2.out"}},{t+0.3});')
body=f"""{hdr(fid,'Las señales','8 señales combinadas')}
<div class="{fid}-at" id="{fid}-at">{words(fid,'Ocho señales técnicas, combinadas, estiman la ubicación',())}</div>
<svg class="{fid}-a" style="left:0;top:0" width="1080" height="1080">{''.join(svg_lines)}</svg>
<div class="{fid}-glow" id="{fid}-hg" style="left:360px;top:440px;width:360px;height:360px"></div>
<div class="{fid}-nd" id="{fid}-hub" style="left:420px;top:500px;width:240px;height:240px;border-radius:50%;background:#2251FF;font-size:30px;font-weight:700;flex-direction:column;gap:6px;overflow:hidden"><div style="position:relative;width:120px;height:120px">{globe(fid,fid+'-hglobe',120,True,1)}</div><div>Ubicación estimada</div></div>
{''.join(nb)}
<div class="{fid}-src" id="{fid}-src">Fuente: Acuerdo 1-2026 SBP, art. 14</div>
{pgh}"""
js=hdr_js(fid,0.3)+pgj+title_js(fid,0.1,0.9)+f"""
tl.fromTo("#{fid}-hub",{{opacity:0,scale:.5}},{{opacity:1,scale:1,duration:.7,ease:"back.out(1.8)"}},0.4);
tl.fromTo("#{fid}-hg",{{opacity:0}},{{opacity:1,duration:1}},0.4);
tl.fromTo("#{fid}-hglobe",{{rotation:-20}},{{rotation:20,duration:D,ease:"none"}},0);
tl.fromTo("#{fid}-src",{{opacity:0}},{{opacity:1,duration:.6}},1.0);
"""+"\n".join(nj)
files[fid]=wrap(fid,D,"",body,js)

# ---------- 05 ----------
i=4; fid='05-dos-usos'; D=durs[i]
pgh,pgj=pg(fid,.5,.62,D)
tv=cue(i,'verificar'); tf=cue(i,'frenar'); ta=cue(i,'alto riesgo'); ts_=cue(i,'sancionadas'); tn=cue(i,'no cuadran')
body=f"""{hdr(fid,'Dos usos','KYC · PBC')}
<div class="{fid}-at" id="{fid}-at">{words(fid,'La estimación sirve para dos controles: validar el domicilio y frenar aperturas de riesgo',())}</div>
<svg class="{fid}-a" style="left:0;top:0" width="1080" height="1080">
 <line id="{fid}-e1" x1="315" y1="640" x2="390" y2="640" stroke="#2FB8FF" stroke-opacity=".6" stroke-width="2.5" stroke-dasharray="75" stroke-dashoffset="75"/>
 <path id="{fid}-e2" d="M640 640 C 680 640, 680 545, 720 545" fill="none" stroke="#2ED8A3" stroke-opacity=".8" stroke-width="2.5" stroke-dasharray="140" stroke-dashoffset="140"/>
 <path id="{fid}-e3" d="M640 640 C 680 640, 680 740, 720 740" fill="none" stroke="#FF5C6C" stroke-opacity=".8" stroke-width="2.5" stroke-dasharray="140" stroke-dashoffset="140"/>
</svg>
<div class="{fid}-glass {fid}-nd" id="{fid}-n1" style="left:65px;top:580px;width:250px;height:120px;font-size:30px">Solicitud de apertura</div>
<div class="{fid}-glow" id="{fid}-g" style="left:330px;top:460px;width:380px;height:360px"></div>
<div class="{fid}-nd" id="{fid}-n2" style="left:390px;top:560px;width:250px;height:160px;background:#2251FF;border-radius:22px;font-size:32px;font-weight:600">Ubicación estimada</div>
<div class="{fid}-glass" id="{fid}-ok" style="left:720px;top:480px;width:295px;height:130px;padding:20px 24px;box-sizing:border-box">
  <div class="{fid}-D" style="font-size:28px;color:#2ED8A3;font-weight:600">✓ Validar</div>
  <div style="font-size:24px;color:#A9BCCC;margin-top:8px;line-height:1.3">domicilio declarado</div></div>
<div class="{fid}-glass" id="{fid}-no" style="left:720px;top:650px;width:295px;height:250px;padding:20px 24px;box-sizing:border-box">
  <div class="{fid}-D" style="font-size:28px;color:#FF5C6C;font-weight:600">✕ Frenar apertura</div>
  <div id="{fid}-x1" style="font-size:24px;color:#fff;margin-top:16px">• Alto riesgo</div>
  <div id="{fid}-x2" style="font-size:24px;color:#fff;margin-top:10px">• Sancionada</div>
  <div id="{fid}-x3" style="font-size:24px;color:#fff;margin-top:10px;line-height:1.3">• No cuadra con lo declarado</div></div>
<div class="{fid}-src" id="{fid}-src">Fuente: Acuerdo 1-2026 SBP, arts. 14 y 53</div>
{pgh}"""
js=hdr_js(fid,0.3)+pgj+title_js(fid,0.1,1.4)+f"""
tl.fromTo("#{fid}-n1",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:.6,ease:"power3.out"}},0.5);
tl.fromTo("#{fid}-e1",{{attr:{{"stroke-dashoffset":75}}}},{{attr:{{"stroke-dashoffset":0}},duration:.4}},0.9);
tl.fromTo(["#{fid}-n2","#{fid}-g"],{{opacity:0,scale:.8}},{{opacity:1,scale:1,duration:.6,ease:"back.out(1.8)"}},1.1);
tl.fromTo("#{fid}-src",{{opacity:0}},{{opacity:1,duration:.6}},1.4);
tl.fromTo("#{fid}-e2",{{attr:{{"stroke-dashoffset":140}}}},{{attr:{{"stroke-dashoffset":0}},duration:.5}},{tv});
tl.fromTo("#{fid}-ok",{{opacity:0,x:30}},{{opacity:1,x:0,duration:.6,ease:"power3.out"}},{tv+0.3});
tl.fromTo("#{fid}-e3",{{attr:{{"stroke-dashoffset":140}}}},{{attr:{{"stroke-dashoffset":0}},duration:.5}},{tf});
tl.fromTo("#{fid}-no",{{opacity:0,x:30}},{{opacity:1,x:0,duration:.6,ease:"power3.out"}},{tf+0.3});
tl.fromTo("#{fid}-x1",{{opacity:0,x:12}},{{opacity:1,x:0,duration:.4}},{max(ta,tf+0.6)});
tl.fromTo("#{fid}-x2",{{opacity:0,x:12}},{{opacity:1,x:0,duration:.4}},{max(ts_,tf+0.9)});
tl.fromTo("#{fid}-x3",{{opacity:0,x:12}},{{opacity:1,x:0,duration:.4}},{max(tn,tf+1.2)});
"""
files[fid]=wrap(fid,D,"",body,js)

# ---------- 06 ----------
i=5; fid='06-nueve-meses'; D=durs[i]
pgh,pgj=pg(fid,.62,.75,D)
bars=[('Construir o comprar','construye',65,575,330,'#2251FF','#fff'),('Integrar con la plataforma','integrar',300,668,430,'#2251FF','#fff'),
      ('Calibrar','calibrar',600,761,230,'#2251FF','#fff'),('Documentar en el manual','documentar',600,854,415,'#2FB8FF','#051C2C')]
bb=[];bj=[]
for k,(lab,ph,x,y,w,c,tc) in enumerate(bars):
    t=cue(i,ph,0.25)
    bb.append(f'<div class="{fid}-a" id="{fid}-b{k}" style="left:{x}px;top:{y}px;width:{w}px;height:72px;background:{c};border-radius:12px;transform-origin:0 50%"></div>')
    bb.append(f'<div class="{fid}-a {fid}-D" id="{fid}-bl{k}" style="left:{x+20}px;top:{y+18}px;font-size:31px;font-weight:600;color:{tc};white-space:nowrap">{lab}</div>')
    bj.append(f'tl.fromTo("#{fid}-b{k}",{{scaleX:0}},{{scaleX:1,duration:.6,ease:"power3.out"}},{t});')
    bj.append(f'tl.fromTo("#{fid}-bl{k}",{{opacity:0,x:-10}},{{opacity:1,x:0,duration:.4}},{t+0.25});')
body=f"""{hdr(fid,'Nueve meses','Esquema ilustrativo')}
<div class="{fid}-at" id="{fid}-at">{words(fid,'Nueve meses parecen muchos, pero hay cuatro frentes de trabajo',())}</div>
<div class="{fid}-a {fid}-D" id="{fid}-hoy" style="left:65px;top:462px;font-size:26px;color:#6F8799">HOY</div>
<div class="{fid}-a {fid}-D" id="{fid}-dl" style="right:65px;top:462px;font-size:26px;color:#2FB8FF;font-weight:600">30·06·2027</div>
<div class="{fid}-a" id="{fid}-ax" style="left:65px;top:512px;width:950px;height:2px;background:rgba(169,188,204,.35);transform-origin:0 50%"></div>
<div class="{fid}-a" id="{fid}-dline" style="left:1012px;top:512px;width:5px;height:420px;background:#2FB8FF;transform-origin:50% 0;box-shadow:0 0 24px rgba(47,184,255,.7)"></div>
{''.join(bb)}
{''.join(f'<div class="{fid}-a {fid}-mt" style="left:{65+k*950/8-30:.0f}px;top:528px;width:60px;text-align:center;font-size:17px;letter-spacing:.1em;color:#A9BCCC;font-weight:600">{m}</div><div class="{fid}-a {fid}-mt" style="left:{65+k*950/8:.0f}px;top:514px;width:2px;height:14px;background:rgba(169,188,204,.5)"></div>' for k,m in enumerate(['OCT','NOV','DIC','ENE','FEB','MAR','ABR','MAY','JUN']))}
<div class="{fid}-src" id="{fid}-src">Duraciones no a escala · Fuente: Acuerdo 1-2026 SBP, art. 53</div>
{pgh}"""
js=hdr_js(fid,0.3)+pgj+title_js(fid,0.1,1.2)+f"""
tl.fromTo("#{fid}-ax",{{scaleX:0}},{{scaleX:1,duration:1,ease:"power3.inOut"}},0.4);
tl.fromTo(q(".{fid}-mt"),{{opacity:0,y:-6}},{{opacity:1,y:0,duration:.3,stagger:.06}},0.6);
tl.fromTo(["#{fid}-hoy","#{fid}-dl"],{{opacity:0,y:10}},{{opacity:1,y:0,duration:.5,stagger:.4}},0.5);
tl.fromTo("#{fid}-dline",{{scaleY:0}},{{scaleY:1,duration:.8,ease:"power3.out"}},1.0);
tl.fromTo("#{fid}-src",{{opacity:0}},{{opacity:1,duration:.6}},1.2);
"""+"\n".join(bj)+f"""
tl.fromTo("#{fid}-dline",{{opacity:1}},{{opacity:.45,duration:.25}},{D-1.2});
tl.to("#{fid}-dline",{{opacity:1,duration:.25}},{D-0.95});
"""
files[fid]=wrap(fid,D,"",body,js)

# ---------- 07 ----------
i=6; fid='07-pregunta'; D=durs[i]
pgh,pgj=pg(fid,.75,.88,D)
tt=cue(i,'tecnología',0.1); tc=cue(i,'cumplimiento',0.1)
body=f"""<div class="{fid}-a" id="{fid}-beam" style="left:90px;top:-120px;width:900px;height:1260px;background:conic-gradient(from 180deg at 50% 0%,transparent 160deg,rgba(47,184,255,.22) 180deg,transparent 200deg);transform-origin:50% 0"></div>
{hdr(fid,'Gobernanza','Dueño del proyecto')}
<div class="{fid}-at" id="{fid}-at" style="top:170px;text-align:center">{words(fid,'¿Quién es el dueño de este proyecto?',())}</div>
<div class="{fid}-glass {fid}-nd" id="{fid}-c1" style="left:85px;top:480px;width:410px;height:280px;font-size:56px;font-weight:600">Tecnología</div>
<div class="{fid}-glass {fid}-nd" id="{fid}-c2" style="left:585px;top:480px;width:410px;height:280px;font-size:56px;font-weight:600">Cumplimiento</div>
<div class="{fid}-a {fid}-D" id="{fid}-qm" style="left:490px;top:545px;width:100px;text-align:center;font-size:120px;color:#2FB8FF;font-weight:700;line-height:1">?</div>
<div class="{fid}-a" id="{fid}-sub" style="left:0;right:0;top:830px;text-align:center;font-size:38px;color:#A9BCCC">¿Su banco ya lo definió?</div>
{pgh}"""
js=hdr_js(fid,0.2)+pgj+title_js(fid,0.1,0.8)+f"""
tl.fromTo("#{fid}-beam",{{rotation:-28,opacity:0}},{{rotation:0,opacity:1,duration:2.2,ease:"power2.out"}},0);
tl.fromTo(["#{fid}-c1","#{fid}-c2"],{{opacity:0,y:30}},{{opacity:.55,y:0,duration:.7,ease:"power3.out",stagger:.15}},0.5);
tl.fromTo("#{fid}-qm",{{opacity:0,scale:.3}},{{opacity:1,scale:1,duration:.7,ease:"back.out(2.4)"}},1.0);
tl.fromTo("#{fid}-sub",{{opacity:0}},{{opacity:1,duration:.6}},1.3);
tl.fromTo("#{fid}-c1",{{opacity:.55,borderColor:"rgba(169,188,204,.24)"}},{{opacity:1,borderColor:"rgba(47,184,255,.9)",duration:.4}},{tt});
tl.fromTo("#{fid}-c2",{{opacity:.55,borderColor:"rgba(169,188,204,.24)"}},{{opacity:1,borderColor:"rgba(47,184,255,.9)",duration:.4}},{tc});
tl.fromTo("#{fid}-stage",{{scale:1}},{{scale:1.03,duration:D,ease:"none"}},0);
"""
files[fid]=wrap(fid,D,"",body,js)

# ---------- 08 (final) ----------
i=7; fid='08-fuente'; D=durs[i]
pgh,pgj=pg(fid,.88,1,D)
body=f"""<div class="{fid}-glow" id="{fid}-glow" style="left:-120px;top:-120px;width:760px;height:760px"></div>
<div class="{fid}-a" id="{fid}-acc" style="left:65px;top:330px;width:65px;height:6px;background:#2FB8FF;transform-origin:0 50%"></div>
<div class="{fid}-ey" id="{fid}-ey" style="top:360px">Fuente</div>
<div class="{fid}-a" id="{fid}-tw" style="left:65px;top:420px;width:950px;height:110px;overflow:hidden">
 <div class="{fid}-D" id="{fid}-ttl" style="font-weight:700;font-size:76px;white-space:nowrap">Acuerdo 1-2026 de la SBP</div>
 <div class="{fid}-sweep" id="{fid}-sweep" style="left:-240px"></div></div>
<div class="{fid}-a {fid}-D" id="{fid}-art" style="left:65px;top:560px;font-size:54px;color:#2FB8FF;font-weight:600">Artículo 14 · Artículo 53</div>
<div class="{fid}-a" id="{fid}-rule" style="left:65px;top:760px;width:950px;height:1px;background:rgba(169,188,204,.3);transform-origin:0 50%"></div>
<div class="{fid}-a" id="{fid}-sig" style="left:65px;top:785px;font-size:30px;color:#A9BCCC;line-height:1.4">¿Tecnología o Cumplimiento?<br><span style="color:#fff">Cuéntenos en los comentarios.</span></div>
<div class="{fid}-a {fid}-D" id="{fid}-hs" style="left:65px;top:895px;font-size:32px;color:#2FB8FF;font-weight:600">#PBC  #Cumplimiento</div>
{pgh}"""
js=pgj+f"""
tl.fromTo("#{fid}-glow",{{opacity:0,scale:.7}},{{opacity:.8,scale:1,duration:1.6,ease:"power2.out"}},0);
tl.fromTo("#{fid}-acc",{{scaleX:0}},{{scaleX:1,duration:.5,ease:"power3.out"}},0.1);
tl.fromTo("#{fid}-ey",{{opacity:0,x:-15}},{{opacity:1,x:0,duration:.5}},0.2);
tl.fromTo("#{fid}-ttl",{{yPercent:110}},{{yPercent:0,duration:.8,ease:"power4.out"}},0.3);
tl.fromTo("#{fid}-art",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.6,ease:"power3.out"}},{cue(i,'artículos',0.3)});
tl.fromTo("#{fid}-sweep",{{x:0}},{{x:1400,duration:1.1,ease:"power2.inOut"}},1.0);
tl.fromTo("#{fid}-rule",{{scaleX:0}},{{scaleX:1,duration:.8,ease:"power3.inOut"}},1.6);
tl.fromTo("#{fid}-sig",{{opacity:0,y:16}},{{opacity:1,y:0,duration:.6,ease:"power3.out"}},2.0);
tl.fromTo("#{fid}-hs",{{opacity:0}},{{opacity:1,duration:.6}},2.6);
tl.fromTo("#{fid}-stage",{{scale:1}},{{scale:1.035,duration:D,ease:"none",transformOrigin:"30% 50%"}},0);
"""
files[fid]=wrap(fid,D,"",body,js)

# ---------- 09 firma (final, silent) ----------
i=8; fid='09-firma'; D=durs[i]
pgh,pgj=pg(fid,0,1,D)
creds=['CP/AML FIBA · ISO 37301 · 37001 · 37000 · 31000','AI Compliance Expert · LegalTech Architect','Lean Six Sigma Green Belt · Docente · Speaker']
body=f"""{rays(fid,fid+'-rays',540,250,1400,.7)}
<div class="{fid}-glow" id="{fid}-glow" style="left:340px;top:50px;width:400px;height:400px"></div>
<div class="{fid}-a" id="{fid}-gw" style="left:420px;top:130px;width:240px;height:240px">{globe(fid,fid+'-globe',240,True,1)}</div>
<div class="{fid}-a {fid}-D" id="{fid}-name" style="left:0;right:0;top:450px;text-align:center;font-size:74px;font-weight:700;letter-spacing:.06em">JOSÉ ANTONIO SERRANO</div>
<div class="{fid}-a" id="{fid}-rule" style="left:290px;top:552px;width:500px;height:2px;background:{GOLD};transform-origin:50% 50%;box-shadow:0 0 14px rgba(217,178,106,.6)"></div>
<div class="{fid}-a {fid}-D" id="{fid}-role" style="left:0;right:0;top:580px;text-align:center;font-size:36px;font-weight:600;letter-spacing:.24em;color:{GOLD}">AML · CUMPLIMIENTO · GRC</div>
{''.join(f'<div class="{fid}-a {fid}-cr" style="left:0;right:0;top:{650+k*44}px;text-align:center;font-size:24px;letter-spacing:.14em;color:#A9BCCC;text-transform:uppercase;{SG}font-weight:500">{c}</div>' for k,c in enumerate(creds))}
<div class="{fid}-a" id="{fid}-src2" style="left:0;right:0;top:820px;text-align:center;font-size:19px;letter-spacing:.14em;color:#6F8799;text-transform:uppercase;{SG}font-weight:600">Fuente: Acuerdo 1-2026 de la SBP · Artículos 14 y 53</div>
<div class="{fid}-a" id="{fid}-mg" style="left:0;right:0;top:880px;text-align:center;font-size:18px;letter-spacing:.3em;color:#2FB8FF;text-transform:uppercase;{SG}font-weight:600">Motion Graphics · #PBC #Cumplimiento</div>
{pgh}"""
js=pgj+f"""
tl.fromTo("#{fid}-rays",{{rotation:0,opacity:0}},{{rotation:18,opacity:.7,duration:D,ease:"none"}},0);
tl.fromTo("#{fid}-glow",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:1.2,ease:"power2.out"}},0);
tl.fromTo("#{fid}-gw",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:1,ease:"back.out(1.6)"}},0.1);
tl.fromTo("#{fid}-globe",{{rotation:-15}},{{rotation:15,duration:D,ease:"none"}},0);
tl.fromTo("#{fid}-globe-pin",{{y:-30,opacity:0}},{{y:0,opacity:1,duration:.6,ease:"bounce.out"}},0.7);
tl.fromTo("#{fid}-name",{{opacity:0,y:30,filter:"blur(10px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.9,ease:"power3.out"}},0.5);
tl.fromTo("#{fid}-rule",{{scaleX:0}},{{scaleX:1,duration:.8,ease:"power3.inOut"}},1.0);
tl.fromTo("#{fid}-role",{{opacity:0,y:10}},{{opacity:1,y:0,duration:.7}},1.3);
tl.fromTo(q(".{fid}-cr"),{{opacity:0,y:12}},{{opacity:1,y:0,duration:.5,stagger:.2}},1.7);
tl.fromTo("#{fid}-src2",{{opacity:0}},{{opacity:1,duration:.6}},2.5);
tl.fromTo("#{fid}-mg",{{opacity:0}},{{opacity:1,duration:.6}},2.8);
tl.fromTo("#{fid}-stage",{{opacity:1}},{{opacity:0,duration:.6,ease:"power2.in"}},D-0.6);
"""
files[fid]=wrap(fid,D,"",body,js,final=True)

os.makedirs(os.path.join(P,'compositions/frames'),exist_ok=True)
for fid,html in files.items():
    html=html.replace(fid+'-','f'+fid+'-')
    open(os.path.join(P,'compositions/frames',fid+'.html'),'w').write(html)
print('wrote',list(files))
