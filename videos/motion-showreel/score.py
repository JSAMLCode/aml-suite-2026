"""Banda sonora original para el showreel de motion graphics (30 s, 120 BPM, La menor).

Cada evento está anclado a un fotograma del montaje (30 fps):
  0.00-3.00  apertura: dron grave, riser corto, impacto en "CUENTA." (f58)
  3.00-22.80 groove: bombo, palmada, hats, bajo y pad  (Am - F - C - G cada 2 s)
             acentos: inversión de color (f165), cortes (f210/330/480/600),
             alerta (f402), sello (f542), riser del zoom (f642-684)
  22.80-23.0 silencio
  23.00-30.0 resolución: pad que crece, impacto + campana en el logotipo (f752), cola
"""
import sys
import wave

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR = 44100
DUR = 30.0
N = int(SR * DUR)
rng = np.random.default_rng(7)
out = np.zeros((2, N))
duck = np.ones(N)


def fr(frame):
    return frame / 30.0


def mf(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def t_(d):
    return np.arange(int(d * SR)) / SR


def flt(x, kind, f, order=2):
    if kind == 'bp':
        sos = butter(order, [f[0] / (SR / 2), f[1] / (SR / 2)], 'bandpass', output='sos')
    else:
        sos = butter(order, f / (SR / 2), kind, output='sos')
    return sosfilt(sos, x)


def put(sig, at, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= N:
        return
    sig = sig[: N - i]
    l = np.cos((pan + 1) * np.pi / 4)
    r = np.sin((pan + 1) * np.pi / 4)
    out[0, i : i + len(sig)] += sig * gain * l
    out[1, i : i + len(sig)] += sig * gain * r


def env(n, a, d):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)
    return e


# ---------- instrumentos ----------
def kick(g=1.0):
    t = t_(0.45)
    f = 45 + 110 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 7) * g + flt(rng.standard_normal(len(t)), 'hp', 3000) * np.exp(-t * 120) * 0.15


def clap():
    t = t_(0.3)
    n = flt(rng.standard_normal(len(t)), 'bp', (900, 3500))
    e = np.zeros(len(t))
    for o in (0, 0.011, 0.022):
        e += np.where(t >= o, np.exp(-(t - o) * 60), 0)
    return n * (e * 0.4 + np.exp(-t * 18) * 0.5)


def hat(open_=False):
    t = t_(0.25 if open_ else 0.06)
    return flt(rng.standard_normal(len(t)), 'hp', 7000) * np.exp(-t * (14 if open_ else 70))


def saw(freq, d, detune=(0.0,)):
    t = t_(d)
    s = np.zeros(len(t))
    for dt in detune:
        ph = (t * freq * (1 + dt)) % 1
        s += 2 * ph - 1
    return s / len(detune)


def bass(m, d):
    s = saw(mf(m), d, (0, 0.004)) + np.sin(2 * np.pi * mf(m - 12) * t_(d)) * 0.8
    s = flt(s, 'lp', 420)
    return s * env(len(s), 0.004, d * 0.6)


def pad(notes, d, bright=1800):
    s = sum(saw(mf(m), d, (-0.006, 0, 0.006)) for m in notes)
    s = flt(s, 'lp', bright)
    a = np.minimum(1, t_(d) / 0.25) * np.minimum(1, (d - t_(d)) / 0.3)
    return s * a / len(notes)


def riser(d, f0=300, f1=6000):
    t = t_(d)
    n = rng.standard_normal(len(t))
    out_ = np.zeros(len(t))
    steps = 24
    for k in range(steps):
        a, b = k * len(t) // steps, (k + 1) * len(t) // steps
        fc = f0 * (f1 / f0) ** (k / steps)
        out_[a:b] = flt(n, 'bp', (fc * 0.7, min(fc * 1.4, 20000)))[a:b]
    return out_ * (t / d) ** 2


def impact(g=1.0):
    t = t_(2.2)
    f = 32 + 60 * np.exp(-t * 6)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.2)
    crack = flt(rng.standard_normal(len(t)), 'lp', 5000) * np.exp(-t * 14)
    return (boom * 1.1 + crack * 0.5) * g


def whoosh(d=0.6):
    t = t_(d)
    n = rng.standard_normal(len(t))
    sh = np.sin(np.pi * t / d) ** 2
    return flt(n, 'bp', (500, 4000)) * sh


def bell(m, d=3.5):
    t = t_(d)
    s = sum(np.sin(2 * np.pi * mf(m) * r * t) * a * np.exp(-t * dk) for r, a, dk in ((1, 1, 1.3), (2.76, 0.4, 2.5), (5.4, 0.2, 4), (2, 0.3, 1.8)))
    return s * np.minimum(1, t / 0.002)


def blip(m):
    t = t_(0.12)
    return np.sin(2 * np.pi * mf(m) * t) * np.exp(-t * 35)


def drone(d):
    t = t_(d)
    s = saw(mf(33), d, (-0.003, 0.003)) + saw(mf(45), d, (0.002,)) * 0.5
    s = flt(s, 'lp', 260)
    return s * np.minimum(1, t / 1.2)


# ---------- apertura ----------
put(drone(3.0) * np.linspace(1, 0.6, int(3.0 * SR)), 0, 0.35)
put(riser(fr(58)), 0, 0.12)
put(impact(), fr(58), 0.7)
put(bell(69, 2.5), fr(58), 0.10)
put(riser(1.0, 400, 8000), 2.0, 0.14)

# ---------- groove ----------
CHORDS = [(57, [57, 60, 64, 69]), (53, [53, 57, 60, 65]), (48, [55, 60, 64, 67]), (55, [55, 59, 62, 67])]
G0, G1 = 3.0, 22.8
beat = 0.5
b = G0
i = 0
while b < G1 - 1e-6:
    put(kick(), b, 0.75)
    duck_idx = int(b * SR)
    dl = int(0.22 * SR)
    duck[duck_idx : duck_idx + dl] = np.minimum(duck[duck_idx : duck_idx + dl], 0.45 + 0.55 * np.linspace(0, 1, len(duck[duck_idx : duck_idx + dl])))
    if i % 2 == 1:
        put(clap(), b, 0.32)
    put(hat(i % 4 == 3), b + 0.25, 0.10, 0.3)
    put(hat(), b, 0.05, -0.3)
    i += 1
    b += beat

bus = np.zeros((2, N))
t0 = G0
k = 0
while t0 < G1 - 1e-6:
    root, notes = CHORDS[k % 4]
    d = min(2.0, G1 - t0)
    p = pad(notes, d)
    ii = int(t0 * SR)
    bus[0, ii : ii + len(p)] += p * 0.16
    bus[1, ii : ii + len(p)] += np.roll(p, 220) * 0.16
    for e in range(int(d / 0.25)):
        if e % 4 != 3:
            put(bass(root - 12 + (12 if e % 4 == 2 else 0), 0.24), t0 + e * 0.25, 0.30)
    t0 += 2.0
    k += 1
out += bus * duck

# acentos sincronizados con la imagen
put(impact(0.6), fr(165), 0.45)            # inversión de color
for c in (210, 330, 480, 600):
    put(whoosh(0.5), fr(c) - 0.3, 0.16, -0.4 if c % 2 else 0.4)
put(impact(0.5), fr(210), 0.25)
for j, m in enumerate((84, 88, 91)):
    put(blip(m), fr(402) + j * 0.09, 0.12)  # alerta en la matriz
put(impact(0.8), fr(542), 0.50)            # sello VERIFICADO
put(riser(fr(684) - fr(642), 300, 12000), fr(642), 0.22)
put(whoosh(1.2), fr(672), 0.22)

# ---------- resolución ----------
put(pad([45, 57, 64, 69], 7.0, 1200), 23.0, 0.10)
put(riser(fr(752) - 23.0, 200, 5000), 23.0, 0.12)
put(impact(1.0), fr(752), 0.75)
for j, m in enumerate((72, 76, 79, 83, 86)):
    put(bell(m, 4.5), fr(752) + j * 0.06, 0.07, (j - 2) * 0.25)
put(pad([48, 55, 60, 64, 67, 74], 30.0 - fr(752), 2200), fr(752), 0.13)
put(bell(60, 3.0), fr(898) - 2.6, 0.05)

# ---------- reverb y master ----------
ir_t = t_(2.4)
ir = rng.standard_normal((2, len(ir_t))) * np.exp(-ir_t * 2.6)
wet = np.stack([fftconvolve(out[c], ir[c])[:N] for c in range(2)]) * 0.012
mix = out + wet
fade = np.ones(N)
fl = int(1.2 * SR)
fade[-fl:] = np.linspace(1, 0, fl) ** 2
mix *= fade
mix = np.tanh(mix * 1.3) / np.tanh(1.3)
mix *= 0.89 / np.max(np.abs(mix))

pcm = (mix.T * 32767).astype(np.int16)
path = sys.argv[1] if len(sys.argv) > 1 else 'public/score.wav'
with wave.open(path, 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print('ok', path)
