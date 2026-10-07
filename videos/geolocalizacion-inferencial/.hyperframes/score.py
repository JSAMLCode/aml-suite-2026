"""Banda sonora orquestal sintetizada — inspiracional, épica y cinematográfica (La menor → Do mayor).
Cuerdas legato, coro, metales heroicos, piano, campanas, timbales y taikos. Sincronizada con los cortes
y las señales visuales; duck bajo la voz. Instrumentos base tomados de showreel/music.py."""
import re, sys, wave, os
import numpy as np
from scipy.signal import fftconvolve
P = sys.argv[1]; MUSIC = sys.argv[2]
sb = open(os.path.join(P, 'STORYBOARD.md')).read()
script = open(os.path.join(P, 'SCRIPT.md')).read()
lines = re.findall(r'\n\n    (.+)\n', script)
durs = [float(x) for x in re.findall(r'- duration: ([\d.]+)s', sb)]
S = [sum(durs[:k]) for k in range(len(durs))] + [sum(durs)]
TOTAL = sum(durs)
src = open(MUSIC).read().split('# ---------------- arreglo')[0]
sys.argv = ['music.py', str(TOTAL), 'a']
g = {}; exec(src, g)
SR, N = g['SR'], g['N']; dry, duck_bus, send = g['dry'], g['duck_bus'], g['send']
place, add_stereo, flt, tt, noise, mf, saw = (g[n] for n in 'place add_stereo flt tt noise mf saw'.split())
impact, taiko, riser, whoosh, crash, revcym, kick, snare_hit = (g[n] for n in 'impact taiko riser whoosh crash revcym kick snare_hit'.split())
rng = np.random.default_rng(7)

def cue(i, phrase, lead=0.15):
    t = lines[i].lower(); k = t.find(phrase.lower()); assert k >= 0, phrase
    return S[i] + max(0.05, durs[i]*k/len(t) - lead)

# ---------------- instrumentos orquestales ----------------
def env_adsr(t, d, a, r):
    return np.minimum(1, t/a) * np.clip((d - t)/r, 0, 1)

def strings(notes, d, a=0.7, r=0.9, bright=2600):
    t = tt(d); out = np.zeros((2, len(t)))
    vib = 1 + 0.0035*np.sin(2*np.pi*5.2*t + 1.3)
    for ch in (0, 1):
        s = np.zeros(len(t))
        for m in notes:
            for k in range(5):
                dt = (k - 2)*0.0028 + (0.0011 if ch else -0.0011)
                ph = (np.cumsum(mf(m)*(1 + dt)*vib)/SR + rng.random()) % 1.0
                s += 2*ph - 1
        s /= len(notes)*5
        out[ch] = flt(flt(s, 'lowpass', bright, 2), 'highpass', 120)
    return out*env_adsr(t, d, a, r)[None]*2.4

def choir(notes, d, a=0.9, r=1.2):
    t = tt(d); out = np.zeros((2, len(t)))
    vib = 1 + 0.006*np.sin(2*np.pi*5.6*t)
    for ch in (0, 1):
        s = np.zeros(len(t))
        for m in notes:
            for k in range(3):
                ph = (np.cumsum(mf(m)*(1 + (k-1)*0.004 + ch*0.002)*vib)/SR + rng.random()) % 1.0
                s += 2*ph - 1
        s /= len(notes)*3
        v = flt(s, 'bp', (650, 950))*1.0 + flt(s, 'bp', (1050, 1300))*0.6 + flt(s, 'bp', (2600, 3100))*0.25
        out[ch] = v
    return out*env_adsr(t, d, a, r)[None]*3.2

def brass(m, d, a=0.12, r=0.35):
    t = tt(d)
    vib = 1 + 0.004*np.sin(2*np.pi*5.0*t)*np.clip((t - 0.3)/0.4, 0, 1)
    s = 0
    for dt in (-0.004, 0, 0.004):
        ph = (np.cumsum(mf(m)*(1 + dt)*vib)/SR) % 1.0
        s = s + 2*ph - 1
    s = s/3 + 0.5*np.sign(np.sin(2*np.pi*np.cumsum(mf(m - 12)*vib)/SR))*0.4
    soft, hard = flt(s, 'lowpass', 700, 2), flt(s, 'lowpass', 2800, 2)
    x = np.clip(t/0.35, 0, 1)*(0.7 + 0.3*np.exp(-t*1.5))
    return np.tanh(1.4*(soft*(1 - x) + hard*x))*env_adsr(t, d, a, r)*0.8

def piano(m, d=2.5):
    t = tt(d); f = mf(m)
    s = sum(np.sin(2*np.pi*f*k*(1 + 0.0004*k*k)*t)*np.exp(-t*(1.1 + 0.9*k))/k**1.1 for k in range(1, 7))
    ham = flt(noise(d), 'bp', (1500, 5000))*np.exp(-t*90)*0.15
    return (s + ham)*np.minimum(1, t/0.004)*0.6

def bell(m, d=3.0):
    t = tt(d); f = mf(m)
    return sum(a*np.sin(2*np.pi*f*r*t)*np.exp(-t*dc) for r, a, dc in ((1, .5, 1.2), (2.76, .25, 2.4), (5.4, .12, 4), (8.93, .06, 6)))

def timpani(m, d=1.8):
    t = tt(d); f = mf(m)*(1 + 0.08*np.exp(-t*20))
    return (np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*2.2) + flt(noise(d), 'lowpass', 400)*np.exp(-t*25)*0.5)*0.9

def snare_roll(d, g0=0.1, g1=1.0):
    t0 = 0.0; out = np.zeros(int(d*SR) + SR)
    while t0 < d:
        x = t0/d; i0 = int(t0*SR); h = snare_hit()*(g0 + (g1 - g0)*x**1.6)
        out[i0:i0+len(h)] += h[:len(out)-i0]; t0 += 0.11 - 0.06*x
    return out[:int(d*SR)]

def S2(sig2, t0, gain, rev=0.4, bus=None): add_stereo(sig2, t0, gain, rev=rev, bus=bus)

# ---------------- armonía ----------------
CH = {'Am': [45, 52, 57, 60, 64], 'F': [41, 48, 53, 57, 60], 'C': [48, 55, 60, 64, 67], 'G': [43, 50, 55, 59, 62],
      'Dm': [38, 45, 50, 53, 57], 'Em': [40, 47, 52, 55, 59], 'Cadd9': [36, 48, 55, 60, 62, 64, 67]}
ROOT = {'Am': 33, 'F': 29, 'C': 36, 'G': 31, 'Dm': 38, 'Em': 28, 'Cadd9': 36}
def split(a, b, names): w = (b - a)/len(names); return [(a + k*w, a + (k + 1)*w, n) for k, n in enumerate(names)]
plan = ([(0, S[1], 'Am')] + split(S[1], S[2], ['Am', 'F', 'C', 'G']) + split(S[2], S[3], ['Am', 'F', 'C', 'G'])
        + split(S[3], S[4], ['Am', 'F', 'C', 'G']) + split(S[4], S[5], ['F', 'G', 'Em', 'Am']) + split(S[5], S[6], ['Dm', 'F', 'G', 'G'])
        + split(S[6], S[7], ['F', 'G']) + split(S[7], S[8], ['C', 'G', 'F']) + [(S[8], TOTAL, 'Cadd9')])
MEL = {'Am': [(0, 76, .5), (.5, 74, .25), (.75, 72, .25)], 'F': [(0, 72, .62), (.62, 74, .38)], 'C': [(0, 76, .5), (.5, 79, .5)],
       'G': [(0, 74, .7), (.7, 71, .3)], 'Em': [(0, 71, .6), (.6, 74, .4)], 'Dm': [(0, 74, .5), (.5, 77, .5)], 'Cadd9': [(0, 79, 1)]}

def section(t):
    for k in range(len(S) - 1):
        if S[k] <= t < S[k + 1]: return k
    return len(S) - 2

for a, b, n in plan:
    d = b - a; sec = section(a + 0.01); notes = CH[n]
    # cuerdas: presentes siempre, crecen en brillo/volumen por sección
    lvl = [0.10, 0.13, 0.15, 0.17, 0.18, 0.19, 0.26, 0.22, 0.30][sec]
    S2(strings(notes, d + 0.5, a=0.5 if sec else 1.2, bright=1800 + 350*sec), a, lvl, rev=0.5, bus=duck_bus)
    # contrabajos / sub
    t_ = tt(d + 0.3); bass = np.sin(2*np.pi*mf(ROOT[n])*t_)*env_adsr(t_, d + 0.3, 0.08, 0.3)
    place(bass*0.5, a, 0.35 if sec >= 2 else 0.2, bus=duck_bus)
    # coro desde la sección 3 (señales) y en clímax
    if sec in (2, 3, 4, 6, 7, 8):
        S2(choir([m + 12 for m in notes[1:4]], d + 0.6), a, 0.10 if sec < 6 else 0.16, rev=0.8, bus=duck_bus)
    # metales: melodía heroica en secciones 4, 5, 7, 8 y final
    if sec in (3, 4, 6, 7, 8):
        for off, m, dd in MEL[n]:
            place(brass(m - 12, dd*d + 0.15), a + off*d, 0.20 if sec < 6 else 0.28, rev=0.55, bus=duck_bus)
            if sec >= 6:
                S2(strings([m], dd*d + 0.3, a=0.15, bright=4200), a + off*d, 0.12, rev=0.6, bus=duck_bus)
    # piano arpegiado (intro y primeras secciones), corcheas a 100 BPM
    if sec in (0, 1, 2, 7):
        arp = [notes[1], notes[2], notes[3], notes[4] if len(notes) > 4 else notes[3] + 12]
        t, j = a, 0
        while t < b - 0.05:
            place(piano(arp[j % 4] + 12, 1.6), t, 0.16 if sec != 0 else 0.22, pan=-0.3 if j % 2 else 0.3, rev=0.6, bus=duck_bus)
            t += 0.3; j += 1

# ---------------- percusión y momentos ----------------
place(impact(1.0), 0.02, 0.7, rev=0.5)
place(timpani(33), 0.02, 0.6, rev=0.5)
place(bell(81), 0.4, 0.18, rev=0.9)
place(riser(2.0), S[1] - 2.0, 0.3, rev=0.5)
for k in range(1, 9):
    place(whoosh(0.55), S[k] - 0.5, 0.5, pan=-0.2 if k % 2 else 0.2, rev=0.3)
    place(taiko(1.0), S[k], 0.5, rev=0.4)
    place(timpani(ROOT[plan[[i for i, p in enumerate(plan) if p[0] <= S[k] + 0.01][-1]][2]] + 12), S[k], 0.35, rev=0.4)
# groove épico: taikos y bombo en secciones 3-5, más denso en 4-5
BEAT = 0.6
for sec in (2, 3, 4):
    t = S[sec]; j = 0
    while t < S[sec + 1] - 0.2:
        if j % 4 == 0: place(kick(), t, 0.35 if sec == 2 else 0.45)
        if j % 4 == 2: place(taiko(0.8), t, 0.3 if sec == 2 else 0.4, rev=0.3)
        if sec >= 3 and j % 8 == 7: place(taiko(0.6), t + BEAT/2, 0.25, rev=0.3)
        t += BEAT; j += 1
# interruptor "ya no es opcional"
tf = cue(1, 'ya no es opcional', 0.1)
place(impact(0.9), tf, 0.6, rev=0.5); place(bell(84), tf + 0.05, 0.16, rev=0.9)
# sonar suave en solicitante/dispositivo
for ph, m in (('solicitante', 88), ('dispositivo', 91)): place(bell(m, 2.0), cue(2, ph), 0.10, rev=0.9)
# señales: campanitas pentatónicas
for k, ph in enumerate(['dirección ip', 'tipo de red', 'proveedor', 'vpn', 'proxies', 'anonimización', 'zona horaria', 'configuración regional']):
    place(bell([81, 84, 86, 88, 91, 93, 96, 98][k], 1.6), cue(3, ph, 0.2) + 0.15, 0.07, pan=-0.5 + k*0.14, rev=0.8)
# "frenar"
place(timpani(29), cue(4, 'frenar'), 0.5, rev=0.4)
# construcción hacia la pregunta: redoble + timbales + riser
roll = snare_roll(durs[5] - 0.3, 0.05, 0.7); place(roll, S[5] + 0.1, 0.35, rev=0.4)
for k in range(6): place(timpani(38 if k % 2 else 33), S[5] + durs[5]*(k/6), 0.25 + 0.05*k, rev=0.4)
place(riser(3.2), S[6] - 3.2, 0.4, rev=0.5); place(revcym(1.6), S[6] - 1.6, 0.5)
# clímax
place(impact(1.4), S[6], 1.0, rev=0.7); place(crash(), S[6], 0.6, rev=0.5)
for k in range(6): place(taiko(1.0), S[6] + 0.6 + k*0.6, 0.35 if k % 2 else 0.45, rev=0.4)
# resolución mayor y final
place(crash(), S[7], 0.35, rev=0.6); place(bell(84), S[7] + 0.2, 0.16, rev=0.9)
place(riser(1.8), S[8] - 1.8, 0.4, rev=0.5)
place(impact(1.5), S[8], 1.0, rev=0.8); place(crash(), S[8], 0.6, rev=0.6); place(timpani(36), S[8], 0.7, rev=0.6)
for k, m in enumerate([79, 84, 88, 91]): place(bell(m, 3.5), S[8] + 0.4 + k*0.35, 0.12, rev=0.95)

# ---------------- mezcla ----------------
tN = np.arange(N)/SR; voice = np.zeros(N)
for k in range(8):
    with wave.open(os.path.join(P, f'assets/voice/{k+1:02d}.wav')) as w:
        sr, chn = w.getframerate(), w.getnchannels()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)/32768
    if chn == 2: x = x.reshape(-1, 2).mean(1)
    if sr != SR: x = np.interp(np.arange(int(len(x)*SR/sr))*sr/SR, np.arange(len(x)), x)
    i0 = int(S[k]*SR); L = min(len(x), N - i0); voice[i0:i0+L] += x[:L]
win = int(0.08*SR); env = np.convolve(np.abs(voice), np.ones(win)/win, 'same'); env /= env.max() + 1e-9
rel = np.exp(-1/(0.4*SR)); e2 = np.empty_like(env); acc = 0.0
for j in range(0, N, 64):
    v = env[j:j+64].max(); acc = max(v, acc*rel**64); e2[j:j+64] = acc
speech = np.clip(e2*4, 0, 1)
mix = dry*(1 - 0.35*speech) + duck_bus*(1 - 0.55*speech)
ir_t = tt(3.2)
ir = np.stack([flt(noise(3.2), 'lowpass', 7000)*np.exp(-ir_t*2.0) for _ in range(2)])
ir[:, :int(0.03*SR)] *= np.linspace(0, 1, int(0.03*SR))
wet = np.stack([fftconvolve(flt(send[c], 'highpass', 180), ir[c])[:N] for c in range(2)])
wet /= np.max(np.abs(wet)) + 1e-9
mix += wet*0.45*np.max(np.abs(mix))
i0 = int((S[6] - 0.25)*SR); mix[:, i0:i0 + int(0.22*SR)] *= 0.12          # silencio dramático antes de la pregunta
mix *= np.minimum(1, (TOTAL - tN)/2.2)
mix = flt(mix, 'highpass', 42)
mix = mix + 0.35*flt(mix, 'highpass', 4000)
mix /= np.max(np.abs(mix)); mix = np.tanh(1.4*mix)/np.tanh(1.4)*0.75
os.makedirs(os.path.join(P, 'assets/bgm'), exist_ok=True)
with wave.open(os.path.join(P, 'assets/bgm/score.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(mix.T, -1, 1)*32767).astype(np.int16).tobytes())
print('score', round(TOTAL, 3))
