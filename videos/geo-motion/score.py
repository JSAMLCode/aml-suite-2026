"""Banda sonora + locución para "Geolocalización inferencial" (120 BPM, La menor).

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
import json, unicodedata
TL = json.load(open('src/timeline.json'))
DUR = TL['end'] / 30.0
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



def norm(s):
    s = unicodedata.normalize('NFD', s.lower())
    return ''.join(c for c in s if c.isalnum() and unicodedata.category(c) != 'Mn')


def cue(lid, word, nth=0):
    """Fotograma global de una palabra: el mismo cálculo que wf() en src/tl.ts."""
    l = next(x for x in TL['lines'] if x['id'] == lid)
    hits = [w for w in l['words'] if norm(w['w']).startswith(norm(word))]
    return l['start'] + hits[nth]['f']


def start(lid):
    return next(x for x in TL['lines'] if x['id'] == lid)['start']


SIGN, END = TL['sign'], TL['end']

# ---------- apertura ----------
put(drone(fr(TL['open']) + 0.5) , 0, 0.25)
put(riser(fr(TL['open']), 300, 5000), 0, 0.08)

# ---------- cama musical bajo la voz ----------
G0, G1 = fr(start('02')), fr(SIGN) - 0.5
CHORDS = [(57, [57, 60, 64, 69]), (53, [53, 57, 60, 65]), (48, [55, 60, 64, 67]), (55, [55, 59, 62, 67])]
b, i = G0, 0
while b < G1 - 1e-6:
    if i % 2 == 0:
        put(kick(), b, 0.45)
        di = int(b * SR); dl = int(0.22 * SR)
        duck[di:di + dl] = np.minimum(duck[di:di + dl], 0.5 + 0.5 * np.linspace(0, 1, len(duck[di:di + dl])))
    if i % 4 == 2:
        put(clap(), b, 0.12)
    put(hat(i % 4 == 3), b + 0.25, 0.05, 0.3)
    i += 1
    b += 0.5
bus = np.zeros((2, N))
t0, k = fr(start('01')), 0
while t0 < G1 - 1e-6:
    root, notes = CHORDS[k % 4]
    d = min(2.0, G1 - t0)
    p = pad(notes, d, 1400)
    ii = int(t0 * SR)
    bus[0, ii:ii + len(p)] += p * 0.14
    bus[1, ii:ii + len(p)] += np.roll(p, 220) * 0.14
    if t0 >= G0:
        for e in range(int(d / 0.5)):
            put(bass(root - 12, 0.45), t0 + e * 0.5, 0.20)
    t0 += 2.0
    k += 1
out += bus * duck

# ---------- acentos anclados a eventos visibles ----------
HIT = [cue('01', 'veintisiete'), cue('02', 'cincuenta'), cue('03', 'catorce'), cue('05', 'dos'), cue('06', 'nueve')]
for c in HIT:
    put(impact(0.7), fr(c), 0.32)
for c in [cue('01', 'plazo'), cue('03', 'primaria'), cue('02', 'ya')]:
    put(impact(0.4), fr(c), 0.18)
put(bell(76, 2.0), fr(cue('02', 'ya')), 0.05)
BLIPS = [cue('03', 'solicitante'), cue('03', 'dispositivo'), cue('03', 'coordenadas')]
BLIPS += [cue('04', w) for w in ('dirección', 'tipo', 'proveedor', 'vpn', 'proxies', 'redes', 'zona', 'configuración')]
BLIPS += [cue('05', w) for w in ('verificar', 'frenar', 'alto', 'sancionadas', 'cuadran')]
BLIPS += [cue('06', w) for w in ('decidir', 'integrar', 'calibrar', 'documentar')]
BLIPS += [cue('07', 'tecnología'), cue('07', 'cumplimiento'), cue('08', 'catorce'), cue('08', 'cincuenta')]
for j, c in enumerate(BLIPS):
    put(blip(84 + (j % 4) * 3), fr(c) + 4 / 30, 0.06, ((j % 3) - 1) * 0.3)
put(bell(69, 2.5), fr(cue('04', 'dispositivo')) + 0.2, 0.05)
for lid in ('02', '03', '04', '05', '06'):
    put(whoosh(0.5), fr(start(lid)) - 0.3, 0.07)
z = start('08')
put(riser(22 / 30, 300, 12000), fr(z - 22), 0.12)
put(whoosh(0.9), fr(z - 12), 0.12)

# ---------- firma ----------
put(pad([45, 57, 64, 69], fr(END - SIGN), 1100), fr(SIGN), 0.16)
put(impact(0.9), fr(SIGN + 42), 0.6)
for j, m in enumerate((72, 76, 79, 83, 86)):
    put(bell(m, 4.0), fr(SIGN + 42) + j * 0.06, 0.09, (j - 2) * 0.25)
put(pad([48, 55, 60, 64, 67, 74], fr(END - SIGN - 42), 2000), fr(SIGN + 42), 0.18)

# ---------- locución ----------
voice = np.zeros(N)
for l in TL['lines']:
    w = wave.open(f"../geolocalizacion-inferencial/assets/voice/{l['id']}.wav")
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
    if w.getnchannels() == 2:
        x = x.reshape(-1, 2).mean(1)
    if w.getframerate() != SR:
        x = np.interp(np.arange(int(len(x) * SR / w.getframerate())) * w.getframerate() / SR, np.arange(len(x)), x)
    i0 = int(fr(l['start']) * SR)
    voice[i0:i0 + len(x)] += x[:N - i0]
voice *= 0.9 / np.max(np.abs(voice))
# la música baja ~10 dB bajo la voz (envolvente suavizada de 150 ms)
envl = np.convolve(np.abs(voice), np.ones(int(0.15 * SR)) / int(0.15 * SR), mode='same')
gate = np.clip(envl / 0.02, 0, 1)
out *= 1 - 0.68 * gate
# ---------- reverb y master ----------
ir_t = t_(2.4)
ir = rng.standard_normal((2, len(ir_t))) * np.exp(-ir_t * 2.6)
wet = np.stack([fftconvolve(out[c], ir[c])[:N] for c in range(2)]) * 0.012
mix = (out + wet) * 0.55 + voice[None, :] * 1.0
fade = np.ones(N)
fl = int(1.2 * SR)
fade[-fl:] = np.linspace(1, 0, fl) ** 2
mix *= fade
# sin saturación: la voz debe quedar limpia
mix *= 0.89 / np.max(np.abs(mix))

pcm = (mix.T * 32767).astype(np.int16)
path = sys.argv[1] if len(sys.argv) > 1 else 'public/mix.wav'
with wave.open(path, 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print('ok', path)

# Sonoridad de redes sociales: -14 LUFS, pico real -1,5 dBTP
import os, subprocess
tmp = path + '.tmp.wav'
os.replace(path, tmp)
subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', tmp, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', str(SR), path], check=True)
os.remove(tmp)
