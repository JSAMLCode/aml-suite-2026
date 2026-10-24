"""Banda sonora cinematográfica + locución para "Geolocalización inferencial".

Épica e inspiracional, 120 BPM, La menor con progresión vi–IV–I–V (Am–F–C–G).
Arco dramático anclado a la línea de tiempo (src/timeline.json):
  apertura   dron grave y platillo invertido hacia el golpe del 2027
  01 fecha   cuerdas suaves + piano; braam y timbal en "veintisiete"
  02-03      entra el ostinato de cuerdas; metales graves en cada compás
  04 señales crescendo: taikos, coro, riser hasta "ubicación estimada"
  05 usos    pleno: melodía de metales sobre la progresión inspiracional
  06 plazo   tensión: reloj, ostinato a semicorcheas, timbal en redoble
  07 pregunta se vacía: piano y pad; riser al zoom
  08 fuente  respiración antes del final
  firma      clímax: tutti en Do mayor, braam, campanas y cola larga
La música baja ~10 dB bajo la voz. Sin saturación. Master a -14 LUFS.
"""
import json
import os
import subprocess
import sys
import unicodedata
import wave

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR = 44100
TL = json.load(open('src/timeline.json'))
DUR = TL['end'] / 30.0
N = int(SR * DUR)
rng = np.random.default_rng(2027)
out = np.zeros((2, N))   # orquesta
perc = np.zeros((2, N))  # percusión (menos reverb)


def fr(frame):
    return frame / 30.0


def mf(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def t_(d):
    return np.arange(int(d * SR)) / SR


def flt(x, kind, f, order=2):
    if kind == 'bp':
        sos = butter(order, [f[0] / (SR / 2), min(f[1], SR / 2 - 100) / (SR / 2)], 'bandpass', output='sos')
    else:
        sos = butter(order, f / (SR / 2), kind, output='sos')
    return sosfilt(sos, x)


def put(sig, at, gain=1.0, pan=0.0, bus=None):
    bus = out if bus is None else bus
    i = int(at * SR)
    if i >= N or i < 0:
        return
    sig = sig[: N - i]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    bus[0, i:i + len(sig)] += sig * gain * l
    bus[1, i:i + len(sig)] += sig * gain * r


def env(d, a, r):
    t = t_(d)
    return np.minimum(1, t / max(a, 1e-4)) * np.minimum(1, np.maximum(0, (d - t) / max(r, 1e-4)))


def saw(freq, d, voices=(0.0,), vib=0.0):
    t = t_(d)
    s = np.zeros(len(t))
    for k, dt in enumerate(voices):
        f = freq * (1 + dt) * (1 + vib * np.sin(2 * np.pi * (5.2 + k * 0.3) * t))
        ph = np.cumsum(f) / SR + rng.random()
        s += 2 * (ph % 1) - 1
    return s / len(voices)


# ---------- instrumentos ----------
ENS = (-0.008, -0.003, 0.0, 0.004, 0.009)


def strings(notes, d, bright=2600, a=0.35, r=0.5):
    s = sum(saw(mf(m), d, ENS, vib=0.003) for m in notes) / len(notes)
    return flt(s, 'lp', bright) * env(d, a, r)


def spiccato(m, d=0.12, bright=3200):
    s = saw(mf(m), d, (-0.004, 0.0, 0.005)) + saw(mf(m + 12), d, (0.002,)) * 0.4
    return flt(s, 'lp', bright) * env(d, 0.004, d * 0.7) * np.exp(-t_(d) * 10)


def brass(notes, d, bright=1400, a=0.25):
    s = sum(saw(mf(m), d, (-0.003, 0.003), vib=0.002) for m in notes) / len(notes)
    e = env(d, a, 0.4)
    # el brillo crece con la dinámica: los metales "se abren"
    return (flt(s, 'lp', bright) * 0.6 + flt(s, 'lp', bright * 2.2) * 0.4 * e) * e


def choir(notes, d, a=0.8):
    s = sum(saw(mf(m), d, ENS, vib=0.004) for m in notes) / len(notes)
    v = flt(s, 'bp', (600, 1100)) * 0.8 + flt(s, 'bp', (1000, 1500)) * 0.5 + flt(s, 'lp', 400) * 0.5
    return v * env(d, a, 0.8)


def piano(m, d=2.5):
    t = t_(d)
    s = sum(np.sin(2 * np.pi * mf(m) * k * t) * (0.6 ** (k - 1)) * np.exp(-t * (1.5 + k)) for k in range(1, 6))
    return s * np.minimum(1, t / 0.003)


def bell(m, d=3.5):
    t = t_(d)
    s = sum(np.sin(2 * np.pi * mf(m) * r * t) * a * np.exp(-t * dk) for r, a, dk in ((1, 1, 1.2), (2.76, 0.4, 2.5), (5.4, 0.2, 4), (2, 0.3, 1.8)))
    return s * np.minimum(1, t / 0.002)


def timpani(m=33, g=1.0):
    t = t_(1.6)
    f = mf(m) * (1 + 0.15 * np.exp(-t * 30))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.2) + flt(rng.standard_normal(len(t)), 'lp', 900) * np.exp(-t * 25) * 0.4
    return s * g


def taiko(g=1.0):
    t = t_(0.9)
    f = 55 + 70 * np.exp(-t * 20)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6) + flt(rng.standard_normal(len(t)), 'bp', (150, 1800)) * np.exp(-t * 35) * 0.6
    return s * g


def braam(notes, d=2.6):
    s = sum(saw(mf(m), d, (-0.01, 0, 0.01)) for m in notes) / len(notes)
    sweep = np.linspace(300, 2400, len(s)) ** 1
    y = np.zeros(len(s))
    blk = 2048
    for i in range(0, len(s), blk):
        y[i:i + blk] = flt(s, 'lp', float(sweep[min(i, len(s) - 1)]))[i:i + blk]
    return y * env(d, 0.02, 1.2)


def sub_drop(d=1.8):
    t = t_(d)
    f = 70 * np.exp(-t * 1.5) + 28
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.6)


def riser(d, f0=300, f1=8000):
    t = t_(d)
    n = rng.standard_normal(len(t))
    y = np.zeros(len(t))
    steps = 24
    for k in range(steps):
        a, b = k * len(t) // steps, (k + 1) * len(t) // steps
        fc = f0 * (f1 / f0) ** (k / steps)
        y[a:b] = flt(n, 'bp', (fc * 0.7, fc * 1.4))[a:b]
    return y * (t / d) ** 2


def revcym(d=1.5):
    t = t_(d)
    return flt(rng.standard_normal(len(t)), 'hp', 4000) * (t / d) ** 3


def tick():
    t = t_(0.05)
    return flt(rng.standard_normal(len(t)), 'bp', (2500, 6000)) * np.exp(-t * 120)


def roll(d, g=1.0):
    """Redoble de timbal que crece."""
    y = np.zeros(int(d * SR) + SR)
    step = 0.0625
    k = 0
    while k * step < d:
        tm = timpani(33, 0.25 + 0.75 * (k * step / d))
        i = int(k * step * SR)
        y[i:i + len(tm)] += tm[: len(y) - i] * 0.5
        k += 1
    return y * g


# ---------- utilidades de la línea de tiempo ----------
def norm(s):
    s = unicodedata.normalize('NFD', s.lower())
    return ''.join(c for c in s if c.isalnum() and unicodedata.category(c) != 'Mn')


def cue(lid, word, nth=0):
    """Fotograma global de una palabra; mismo cálculo que wf() en src/tl.ts (admite 'a|b')."""
    l = next(x for x in TL['lines'] if x['id'] == lid)
    for alt in word.split('|'):
        hits = [w for w in l['words'] if norm(w['w']).startswith(norm(alt))]
        if len(hits) > nth:
            return l['start'] + hits[nth]['f']
    raise KeyError(word)


def start(lid):
    return next(x for x in TL['lines'] if x['id'] == lid)['start']


SIGN, END = TL['sign'], TL['end']
S = {lid: fr(start(lid)) for lid in ('01', '02', '03', '04', '05', '06', '07', '08')}
BAR = 2.0  # 4 pulsos a 120 BPM
PROG = [  # (bajo, acorde) vi–IV–I–V
    (45, [57, 60, 64]),
    (41, [53, 57, 60]),
    (48, [55, 60, 64]),
    (43, [55, 59, 62]),
]


def section(t0, t1, fn):
    """Llama fn(t, k, bajo, acorde, dur) en cada compás de [t0, t1)."""
    t, k = t0, 0
    while t < t1 - 0.05:
        bass, chord = PROG[k % 4]
        fn(t, k, bass, chord, min(BAR, t1 - t))
        t += BAR
        k += 1


# ---------- apertura ----------
put(strings([33, 45], fr(TL['open']) + 1.5, 900, a=1.0), 0, 0.30)
put(revcym(fr(cue('01', 'veintisiete'))), 0, 0.10)

# ---------- 01: la fecha ----------
put(strings([57, 60, 64], S['02'] - S['01'] + 0.5, 1800, a=0.8), S['01'], 0.16, -0.2)
for j, m in enumerate((69, 72, 76, 74)):
    put(piano(m), S['01'] + 0.2 + j * 0.5, 0.10, 0.2)
c = fr(cue('01', 'veintisiete'))
put(braam([33, 45, 52]), c, 0.30)
put(timpani(33, 1.0), c, 0.45, bus=perc)
put(sub_drop(), c, 0.35, bus=perc)
put(timpani(40, 0.6), fr(cue('01', 'plazo')), 0.30, bus=perc)


# ---------- 02-03: ostinato y metales ----------
def ost(t, k, bass, chord, d, g=0.06, density=8):
    pat = [chord[0], chord[1], chord[2], chord[1]]
    for i in range(int(d * density / 2)):
        put(spiccato(pat[i % 4] + 12), t + i * (2 / density), g, 0.35 if i % 2 else -0.35)


def low(t, k, bass, chord, d, g=0.14):
    put(strings([bass - 12, bass], d + 0.3, 700, a=0.3), t, g)


def horns(t, k, bass, chord, d, g=0.07):
    put(brass([chord[0] - 12, chord[1] - 12], d, 1100, a=0.6), t, g, 0.1)


section(S['02'], S['04'], lambda *a: (ost(*a, g=0.045), low(*a)))
section(S['03'], S['04'], lambda *a: horns(*a))
for w in [cue('02', 'cincuenta'), cue('03', 'catorce')]:
    put(braam([33, 45, 52], 2.0), fr(w), 0.22)
    put(timpani(33), fr(w), 0.40, bus=perc)
put(taiko(1.0), fr(cue('02', 'ya')), 0.35, bus=perc)
put(bell(76, 2.0), fr(cue('02', 'ya')), 0.05)
put(timpani(40, 0.6), fr(cue('03', 'primaria')), 0.25, bus=perc)
for w in ('solicitante', 'dispositivo'):
    put(bell(81, 1.5), fr(cue('03', w)) + 0.1, 0.035, 0.3)

# ---------- 04: crescendo de las señales ----------
section(S['04'], S['05'], lambda *a: (ost(*a, g=0.06, density=16), low(*a, g=0.16), horns(*a, g=0.09)))
section(S['04'], S['05'], lambda t, k, b, c_, d: put(choir([c_[0], c_[1] + 12, c_[2]], d + 0.4, a=0.5), t, 0.07))
t = S['04']
while t < S['05'] - 0.1:
    put(taiko(0.8), t, 0.22, -0.2, bus=perc)
    put(taiko(0.5), t + 0.75, 0.14, 0.2, bus=perc)
    t += BAR
for j, w in enumerate(('dirección', 'tipo', 'proveedor', 'vpn', 'proxies', 'redes', 'zona', 'configuración')):
    put(bell(76 + [0, 3, 7, 10, 12, 15, 19, 22][j], 1.4), fr(cue('04', w)) + 0.13, 0.03, ((j % 3) - 1) * 0.4)
res = fr(cue('04', 'dispositivo')) + 0.2
put(riser(res - S['04'] - 4.0, 400, 9000), S['04'] + 4.0, 0.10)
put(braam([33, 45, 52, 57]), res, 0.28)
put(timpani(33, 1.0), res, 0.45, bus=perc)

# ---------- 05: pleno, melodía inspiracional ----------
MEL = [(76, 1.0), (74, 0.5), (72, 0.5), (72, 1.0), (69, 1.0), (72, 1.0), (74, 1.0), (79, 1.5), (76, 0.5)]


def full(t, k, bass, chord, d):
    ost(t, k, bass, chord, d, g=0.06, density=16)
    low(t, k, bass, chord, d, g=0.18)
    put(strings([chord[0] + 12, chord[1] + 12, chord[2] + 12], d + 0.3, 3000, a=0.2), t, 0.08, 0.2)
    put(brass([chord[0], chord[1], chord[2]], d, 1600, a=0.15), t, 0.08, -0.15)
    put(taiko(1.0), t, 0.24, bus=perc)
    put(timpani(bass - 12 + 24, 0.6), t + 1.0, 0.18, bus=perc)


section(S['05'], S['06'], full)
t = S['05'] + 0.5
for m, d in MEL * 2:
    if t + d > S['06']:
        break
    put(brass([m - 12], d * 0.98, 2000, a=0.08), t, 0.10, 0.1)
    t += d
put(braam([33, 45, 52]), fr(cue('05', 'dos')), 0.20)
put(timpani(33), fr(cue('05', 'frenar')), 0.30, bus=perc)

# ---------- 06: tensión del plazo ----------
section(S['06'], S['07'], lambda *a: (ost(*a, g=0.055, density=16), low(*a, g=0.15)))
put(braam([33, 45, 52]), fr(cue('06', 'nueve')), 0.26)
put(timpani(33), fr(cue('06', 'nueve')), 0.42, bus=perc)
t = S['06']
while t < S['07'] - 0.1:
    put(tick(), t, 0.10, 0.4, bus=perc)
    t += 0.5
put(roll(S['07'] - S['06'] - 0.4, 0.5), S['06'] + 0.2, 0.20, bus=perc)
for w in ('decidir', 'integrar', 'calibrar', 'documentar'):
    put(taiko(0.7), fr(cue('06', w)), 0.20, bus=perc)

# ---------- 07: vacío y pregunta ----------
put(strings([45, 57, 64], S['08'] - S['07'], 1200, a=0.4), S['07'], 0.12)
for j, m in enumerate((69, 72, 76, 72, 74, 71)):
    put(piano(m, 2.0), S['07'] + 0.25 + j * 0.75, 0.09, 0.15)
put(bell(76, 2.0), fr(cue('07', 'tecnología')), 0.04, -0.4)
put(bell(79, 2.0), fr(cue('07', 'cumplimiento')), 0.04, 0.4)
zoom = start('08')
put(riser(22 / 30 + 0.6, 300, 12000), fr(zoom) - 22 / 30 - 0.6, 0.14)
put(revcym(0.9), fr(zoom) - 0.9, 0.10)

# ---------- 08: respiración ----------
put(strings([48, 55, 64, 67], fr(SIGN) - S['08'] + 0.4, 1600, a=0.6), S['08'], 0.12)
put(choir([60, 64, 67], fr(SIGN) - S['08'] + 0.4, a=1.2), S['08'], 0.05)
put(roll(1.6, 0.6), fr(SIGN + 42) - 1.6, 0.25, bus=perc)

# ---------- firma: clímax ----------
B = fr(SIGN + 42)
tail = DUR - B
put(braam([36, 48, 55, 60]), B, 0.32)
put(timpani(36, 1.0), B, 0.5, bus=perc)
put(taiko(1.0), B, 0.4, bus=perc)
put(sub_drop(2.5), B, 0.35, bus=perc)
put(strings([36, 48, 55, 60, 64, 67, 72], tail, 3200, a=0.15, r=2.0), B, 0.22)
put(brass([48, 55, 60, 64], tail, 2200, a=0.2), B, 0.12)
put(choir([60, 64, 67, 72], tail, a=0.5), B, 0.08)
for j, m in enumerate((72, 76, 79, 84, 88)):
    put(bell(m, 4.0), B + j * 0.08, 0.05, (j - 2) * 0.3)
put(piano(72, 3.0), DUR - 3.2, 0.06)

# ---------- reverb de sala ----------
ir_t = t_(3.4)
ir = rng.standard_normal((2, len(ir_t))) * np.exp(-ir_t * 1.9)
ir[:, : int(0.02 * SR)] *= np.linspace(0, 1, int(0.02 * SR))
wet = np.stack([fftconvolve(out[c] + perc[c] * 0.4, ir[c])[:N] for c in range(2)]) * 0.010
music = out + perc + wet

# ---------- locución ----------
VOICE_DIR = os.environ.get('VOICE_DIR', '../geolocalizacion-inferencial/assets/voice')
voice = np.zeros(N)
for l in TL['lines']:
    w = wave.open(f"{VOICE_DIR}/{l['id']}.wav")
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
    if w.getnchannels() == 2:
        x = x.reshape(-1, 2).mean(1)
    if w.getframerate() != SR:
        x = np.interp(np.arange(int(len(x) * SR / w.getframerate())) * w.getframerate() / SR, np.arange(len(x)), x)
    i0 = int(fr(l['start']) * SR)
    voice[i0:i0 + len(x)] += x[: N - i0]
voice *= 0.9 / np.max(np.abs(voice))

# la música baja bajo la voz (envolvente de 150 ms) y respira entre frases
envl = np.convolve(np.abs(voice), np.ones(int(0.15 * SR)) / int(0.15 * SR), mode='same')
gate = np.clip(envl / 0.02, 0, 1)
music *= 1 - 0.66 * gate
music *= 0.5 / (np.max(np.abs(music)) + 1e-9)

mix = music * 0.9 + voice[None, :]
fade = np.ones(N)
fl = int(1.5 * SR)
fade[-fl:] = np.linspace(1, 0, fl) ** 2
mix *= fade
mix *= 0.89 / np.max(np.abs(mix))

path = sys.argv[1] if len(sys.argv) > 1 else 'public/mix.wav'
tmp = path + '.tmp.wav'
with wave.open(tmp, 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix.T * 32767).astype(np.int16).tobytes())
# sonoridad de redes: -14 LUFS, pico real -1,5 dBTP
subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', tmp, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', str(SR), path], check=True)
os.remove(tmp)
print('ok', path)
