"""Genera assets/vendor/earth.js: puntos de tierra (rejilla equiespaciada) + costas (Natural Earth vía world-atlas)
y un dibujante de globo ortográfico en canvas, determinista (rotación pasada como parámetro)."""
import json, sys, math, numpy as np
src50, src110, out = sys.argv[1], sys.argv[2], sys.argv[3]

def decode(path):
    d = json.load(open(path)); sx, sy = d['transform']['scale']; tx, ty = d['transform']['translate']
    arcs = []
    for a in d['arcs']:
        x = y = 0; pts = []
        for dx, dy in a:
            x += dx; y += dy; pts.append((x*sx+tx, y*sy+ty))
        arcs.append(pts)
    def arc(i): return arcs[i] if i >= 0 else arcs[~i][::-1]
    rings = []
    for g in d['objects']['land']['geometries']:
        polys = g['arcs'] if g['type'] == 'MultiPolygon' else [g['arcs']]
        for poly in polys:
            for ring in poly:
                pts = []
                for i in ring:
                    seg = arc(i); pts.extend(seg if not pts else seg[1:])
                rings.append(np.array(pts))
    return rings

rings = decode(src50)
pts = []
step = 1.5
lat = -58.0
while lat <= 83:
    n = max(8, int(round(360*math.cos(math.radians(lat))/step)))
    lons = np.linspace(-180, 180, n, endpoint=False) + (step/2 if int(lat/step) % 2 else 0)
    inside = np.zeros(n, bool)
    for r in rings:
        if r[:,1].min() > lat or r[:,1].max() < lat: continue
        x1, y1 = r[:-1,0], r[:-1,1]; x2, y2 = r[1:,0], r[1:,1]
        cond = (y1 > lat) != (y2 > lat)
        if not cond.any(): continue
        xi = x1[cond] + (lat - y1[cond])*(x2[cond]-x1[cond])/(y2[cond]-y1[cond])
        inside ^= (lons[:,None] < xi[None,:]).sum(1) % 2 == 1
    for lo in lons[inside]: pts.append((round(lat*10), round(float(lo)*10)))
    lat += step
coast = []
for r in decode(src110):
    if len(r) < 4: continue
    coast.append([v for p in r[::1] for v in (round(p[1]*10), round(p[0]*10))])
print('land points', len(pts), 'coast rings', len(coast), file=sys.stderr)

js = r"""
(function(){
if (window.HFEarth) return;
const P=%s, C=%s, R=Math.PI/180;
function proj(lat,lon,lam0,phi0){const f=lat*R,l=(lon-lam0)*R,f0=phi0*R;
 const cosc=Math.sin(f0)*Math.sin(f)+Math.cos(f0)*Math.cos(f)*Math.cos(l);
 return [Math.cos(f)*Math.sin(l), -(Math.cos(f0)*Math.sin(f)-Math.sin(f0)*Math.cos(f)*Math.cos(l)), cosc];}
function draw(cv,o){
 const ctx=cv.getContext('2d'), W=cv.width, r=W*0.40, cx=W/2, cy=W/2, lam0=o.lon, phi0=o.lat, t=o.t||0;
 const gold=o.gold||'#D9B26A', land=o.land||'111,200,255';
 ctx.clearRect(0,0,W,W);
 // atmósfera
 let g=ctx.createRadialGradient(cx,cy,r*0.95,cx,cy,r*1.28); g.addColorStop(0,'rgba(64,160,255,.55)'); g.addColorStop(.35,'rgba(40,110,255,.18)'); g.addColorStop(1,'rgba(20,60,200,0)');
 ctx.fillStyle=g; ctx.beginPath(); ctx.arc(cx,cy,r*1.28,0,7); ctx.fill();
 // océano
 g=ctx.createRadialGradient(cx-r*.35,cy-r*.4,r*.05,cx,cy,r); g.addColorStop(0,'#1d5fa8'); g.addColorStop(.55,'#0c2f5c'); g.addColorStop(1,'#04142a');
 ctx.fillStyle=g; ctx.beginPath(); ctx.arc(cx,cy,r,0,7); ctx.fill();
 ctx.save(); ctx.beginPath(); ctx.arc(cx,cy,r,0,7); ctx.clip();
 // retícula
 ctx.lineWidth=Math.max(1,W/700); ctx.strokeStyle='rgba(120,190,255,.16)';
 for(let lo=-180;lo<180;lo+=20){ctx.beginPath();let on=false;for(let la=-90;la<=90;la+=3){const p=proj(la,lo,lam0,phi0);if(p[2]>0){const X=cx+p[0]*r,Y=cy+p[1]*r;on?ctx.lineTo(X,Y):ctx.moveTo(X,Y);on=true}else on=false}ctx.stroke()}
 for(let la=-60;la<=60;la+=20){ctx.beginPath();let on=false;for(let lo=-180;lo<=180;lo+=3){const p=proj(la,lo,lam0,phi0);if(p[2]>0){const X=cx+p[0]*r,Y=cy+p[1]*r;on?ctx.lineTo(X,Y):ctx.moveTo(X,Y);on=true}else on=false}ctx.stroke()}
 // tierra: puntos
 const ds=W/360;
 for(let i=0;i<P.length;i+=2){const p=proj(P[i]/10,P[i+1]/10,lam0,phi0); if(p[2]<=0.02) continue;
  const a=0.25+0.75*p[2]; ctx.fillStyle='rgba('+land+','+a.toFixed(3)+')';
  const s=ds*(0.55+0.75*p[2]); ctx.fillRect(cx+p[0]*r-s/2,cy+p[1]*r-s/2,s,s);}
 // costas
 ctx.lineWidth=Math.max(1,W/500); ctx.strokeStyle='rgba(170,225,255,.55)';
 for(const ring of C){ctx.beginPath();let on=false;for(let i=0;i<ring.length;i+=2){const p=proj(ring[i]/10,ring[i+1]/10,lam0,phi0);
  if(p[2]>0){const X=cx+p[0]*r,Y=cy+p[1]*r;on?ctx.lineTo(X,Y):ctx.moveTo(X,Y);on=true}else on=false} ctx.stroke()}
 // sombra (terminador) y brillo especular
 g=ctx.createLinearGradient(cx-r,cy-r,cx+r,cy+r); g.addColorStop(0,'rgba(0,0,0,0)'); g.addColorStop(.55,'rgba(2,10,24,.05)'); g.addColorStop(1,'rgba(2,8,20,.62)');
 ctx.fillStyle=g; ctx.fillRect(cx-r,cy-r,2*r,2*r);
 g=ctx.createRadialGradient(cx-r*.45,cy-r*.5,0,cx-r*.45,cy-r*.5,r*.7); g.addColorStop(0,'rgba(255,255,255,.16)'); g.addColorStop(1,'rgba(255,255,255,0)');
 ctx.fillStyle=g; ctx.fillRect(cx-r,cy-r,2*r,2*r);
 ctx.restore();
 // borde iluminado
 ctx.lineWidth=Math.max(1.5,W/300); ctx.strokeStyle='rgba(120,200,255,.85)'; ctx.beginPath(); ctx.arc(cx,cy,r,0,7); ctx.stroke();
 // marcadores (p. ej. Panamá)
 for(const m of (o.marks||[])){const p=proj(m[0],m[1],lam0,phi0); if(p[2]<=0.05) continue; const X=cx+p[0]*r,Y=cy+p[1]*r, k=W/600, al=Math.min(1,p[2]*2)*(o.markAlpha==null?1:o.markAlpha);
  for(let j=0;j<2;j++){const ph=((t*0.8+j*0.5)%%1); ctx.strokeStyle='rgba(217,178,106,'+(al*(1-ph)).toFixed(3)+')'; ctx.lineWidth=2*k; ctx.beginPath(); ctx.arc(X,Y,(6+ph*34)*k,0,7); ctx.stroke();}
  ctx.fillStyle='rgba(217,178,106,'+al+')'; ctx.beginPath(); ctx.arc(X,Y,5*k,0,7); ctx.fill();
  if(m[2]){ctx.font='600 '+(15*k)+'px "Space Grotesk", Inter, sans-serif'; ctx.fillStyle='rgba(255,236,200,'+al+')'; ctx.fillText(m[2],X+12*k,Y-10*k);}}
}
window.HFEarth={draw:draw};
})();
""" % (json.dumps([v for p in pts for v in p], separators=(',',':')), json.dumps(coast, separators=(',',':')))
open(out, 'w').write(js)
