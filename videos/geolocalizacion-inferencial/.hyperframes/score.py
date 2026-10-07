"""Banda sonora cinematográfica/épica sintetizada para el explainer de geolocalización inferencial.
Reutiliza los instrumentos de showreel/music.py (braam, taiko, impact, riser, whoosh, pad, pluck, tick, ping)
y sincroniza cada golpe con los cortes y las señales visuales de los 9 cuadros. Duck bajo la voz."""
import re, sys, wave, os
import numpy as np
P = sys.argv[1]; MUSIC = sys.argv[2]
sb = open(os.path.join(P, 'STORYBOARD.md')).read()
script = open(os.path.join(P, 'SCRIPT.md')).read()
lines = re.findall(r'\n\n    (.+)\n', script)
durs = [float(x) for x in re.findall(r'- duration: ([\d.]+)s', sb)]
S = [sum(durs[:k]) for k in range(len(durs))]
TOTAL = sum(durs)
src = open(MUSIC).read().split('# ---------------- arreglo')[0]
sys.argv = ['music.py', str(TOTAL), 'a']
g = {}
exec(src, g)
for k in list(g): globals().setdefault(k, g[k])
SR, N = g['SR'], g['N']; dry, duck_bus, send = g['dry'], g['duck_bus'], g['send']
place, add_stereo, flt, tt, noise = g['place'], g['add_stereo'], g['flt'], g['tt'], g['noise']
braam, impact, taiko, riser, whoosh, pad, pluck, crash, revcym, kick, sub808 = (g[n] for n in
    'braam impact taiko riser whoosh pad pluck crash revcym kick sub808'.split())

def tick(hi=True):
    t = tt(0.06)
    return (np.sin(2*np.pi*(2400 if hi else 1700)*t)*np.exp(-t*90) + flt(noise(0.06),'highpass',5000)*np.exp(-t*200)*0.5)*0.5
def ping(f=1320):
    t = tt(1.2)
    return np.sin(2*np.pi*f*t)*np.exp(-t*5)*0.45 + np.sin(2*np.pi*2*f*t)*np.exp(-t*9)*0.12

def cue(i, phrase, lead=0.15):
    t = lines[i].lower(); k = t.find(phrase.lower()); assert k >= 0, phrase
    return S[i] + max(0.05, durs[i]*k/len(t) - lead)

AM, F, C, G, DM = [45,52,57,60,64], [41,48,53,57,60], [48,55,60,64,67], [43,50,55,59,62], [38,45,50,53,57]
# ---- colchón armónico (pads oscuros) a lo largo de todo el video
prog = [AM, F, C, G, AM, F, DM, G]
seg = (S[8]) / len(prog)
for k, ch in enumerate(prog):
    add_stereo(pad(ch, seg + 0.6, cutoff=1300, attack=1.2), k*seg, 0.16, rev=0.5, bus=duck_bus)
    place(sub808(ch[0]-12, seg), k*seg, 0.35, bus=duck_bus)
add_stereo(pad([48,55,60,62,64,67], durs[8] + 0.2, cutoff=2600, attack=0.3), S[8], 0.22, rev=0.8)

# ---- 1. apertura: braam + impacto + reloj + riser
place(impact(1.1), 0.02, 0.9, rev=0.4)
place(braam([33,45,52], 3.4), 0.02, 0.55, rev=0.5)
for k in range(int(S[1]/0.5)):
    place(tick(k % 2 == 0), 0.5 + k*0.5, 0.35, pan=0.35 if k % 2 else -0.35, rev=0.3)
place(taiko(1.0), 1.0, 0.6, rev=0.3); place(taiko(1.0), 2.0, 0.6, rev=0.3)
place(riser(2.2), S[1]-2.2, 0.35, rev=0.4)

# ---- golpes y whooshes en cada corte
for k in range(1, len(S)):
    place(whoosh(0.5), S[k]-0.45, 0.6, pan=-0.2 if k % 2 else 0.2, rev=0.3)
    place(taiko(0.9), S[k], 0.55, rev=0.35)
    if k in (2, 6, 8): place(crash(), S[k], 0.5, rev=0.4)

# ---- pulso épico en el cuerpo (cuadros 3-6): taikos y ostinato de cuerdas
BEAT = 0.6
t = S[2]
while t < S[6] - 0.3:
    place(kick(), t, 0.35)
    place(taiko(0.6), t + 2*BEAT if t + 2*BEAT < S[6]-0.3 else t, 0.25, rev=0.3)
    t += 4*BEAT
t, n = S[2], 0
arp = [57, 64, 60, 64, 57, 64, 62, 64]
while t < S[6] - 0.3:
    place(pluck(arp[n % 8] - 12, 0.18), t, 0.16, pan=-0.4 if n % 2 else 0.4, rev=0.4, bus=duck_bus)
    t += BEAT/2; n += 1

# ---- 2. el interruptor: "ya no es opcional"
tf = cue(1, 'ya no es opcional', 0.1)
place(impact(0.9), tf, 0.75, rev=0.5)
place(braam([33,45,52,57], 2.2), tf, 0.4, rev=0.5)

# ---- 3. sonar en solicitante y dispositivo
for ph, f in (('solicitante', 1320), ('dispositivo', 1568)):
    place(ping(f), cue(2, ph), 0.45, pan=-0.3 if f == 1320 else 0.3, rev=0.6)

# ---- 4. cada señal se conecta: blip
for k, ph in enumerate(['dirección ip','tipo de red','proveedor','vpn','proxies','anonimización','zona horaria','configuración regional']):
    place(ping(1760 + 110*(k % 4)), cue(3, ph, 0.2) + 0.15, 0.18, pan=-0.5 + k*0.14, rev=0.4)

# ---- 5. "frenar": golpe disonante
tfr = cue(4, 'frenar')
place(taiko(1.2), tfr, 0.7, rev=0.4)
place(braam([34, 40, 46], 1.6, bright=1600), tfr, 0.35, rev=0.5)

# ---- 6. reloj de los nueve meses + riser hacia la pregunta
for k in range(int((durs[5]-0.2)/0.5)):
    place(tick(k % 2 == 0), S[5] + 0.25 + k*0.5, 0.4, pan=0.35 if k % 2 else -0.35, rev=0.25)
place(riser(3.0), S[6]-3.0, 0.45, rev=0.5)
place(revcym(1.5), S[6]-1.5, 0.5)

# ---- 7. la pregunta: impacto + braam grande + latidos
place(impact(1.3), S[6], 1.0, rev=0.6)
place(braam([33,45,48,52,57], 4.2, bright=3200), S[6], 0.6, rev=0.6)
for k in range(4):
    place(taiko(0.7), S[6] + 1.0 + k*0.9, 0.3, rev=0.4)

# ---- 8. fuente: campana suave
place(ping(1046), S[7] + 0.3, 0.35, rev=0.8)

# ---- 9. firma: riser + impacto final + braam mayor
place(riser(1.8), S[8]-1.8, 0.45, rev=0.5)
place(impact(1.4), S[8], 1.0, rev=0.7)
place(braam([36,48,55,62,64], durs[8], bright=3600), S[8], 0.55, rev=0.8)
place(ping(1046), S[8] + 0.5, 0.35, rev=0.9); place(ping(1568), S[8] + 1.3, 0.25, rev=0.9)

# ---------------- mezcla con duck bajo la voz ----------------
tN = np.arange(N)/SR
voice = np.zeros(N)
for k in range(8):
    with wave.open(os.path.join(P, f'assets/voice/{k+1:02d}.wav')) as w:
        sr, ch = w.getframerate(), w.getnchannels()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)/32768
    if ch == 2: x = x.reshape(-1, 2).mean(1)
    if sr != SR: x = np.interp(np.arange(int(len(x)*SR/sr))*sr/SR, np.arange(len(x)), x)
    i0 = int(S[k]*SR); L = min(len(x), N-i0); voice[i0:i0+L] += x[:L]
env = np.abs(voice)
win = int(0.08*SR); env = np.convolve(env, np.ones(win)/win, 'same')
env = env/(env.max()+1e-9)
# release lento
rel = np.exp(-1/(0.35*SR)); e2 = np.empty_like(env); acc = 0.0
for j in range(0, N, 64):
    v = env[j:j+64].max(); acc = max(v, acc*rel**64); e2[j:j+64] = acc
speech = np.clip(e2*4, 0, 1)
mix = dry*(1-0.45*speech) + duck_bus*(1-0.7*speech)

ir_t = tt(2.4)
ir = np.stack([flt(noise(2.4), 'lowpass', 6000)*np.exp(-ir_t*2.6) for _ in range(2)])
from scipy.signal import fftconvolve
wet = np.stack([fftconvolve(flt(send[c], 'highpass', 200), ir[c])[:N] for c in range(2)])
wet /= np.max(np.abs(wet)) + 1e-9
mix += wet*0.35*np.max(np.abs(mix))
# silencio dramático justo antes de la pregunta y de la firma
for a in (S[6]-0.22, S[8]-0.12):
    i0, i1 = int(a*SR), int((a+0.2 if a < S[8]-1 else a+0.1)*SR)
    mix[:, i0:i1] *= 0.15
mix *= np.minimum(1, (TOTAL - tN)/1.6)
mix = flt(mix, 'highpass', 30)
mix /= np.max(np.abs(mix))
mix = np.tanh(1.5*mix)/np.tanh(1.5)*0.7
os.makedirs(os.path.join(P, 'assets/bgm'), exist_ok=True)
pcm = (np.clip(mix.T, -1, 1)*32767).astype(np.int16)
with wave.open(os.path.join(P, 'assets/bgm/score.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('score', round(TOTAL, 3), 's')
