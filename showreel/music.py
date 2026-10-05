"""Banda sonora original sintetizada: épica / inspiracional con beat moderno (120 BPM, La menor).
Estructura sincronizada con el video:
  0.0-3.0  apertura: braam, taikos en cada frase, tic-tac de urgencia, riser -> silencio
  3.0-11.0 drop: kick + clap + 808 + hats + ostinato de cuerdas + pad  (Am - F - C - G)
  11.0-13.0 build: golpe en cada palabra, redoble acelerado, riser -> silencio
  13.0-15.0 final: impacto, braam y acorde de Do mayor (add9) con cola de reverb
"""
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
import wave

SR = 44100
import sys
DUR = float(sys.argv[1]) if len(sys.argv) > 1 else 15.0
N = int(SR * DUR)
rng = np.random.default_rng(2026)

dry = np.zeros((2, N))
duck_bus = np.zeros((2, N))   # pads/cuerdas con sidechain
send = np.zeros((2, N))       # envío a reverb
kicks = []


def mf(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def tt(d):
    return np.arange(int(d * SR)) / SR


def flt(x, kind, f, order=2):
    if kind == 'bp':
        sos = butter(order, [f[0] / (SR / 2), f[1] / (SR / 2)], 'bandpass', output='sos')
    else:
        sos = butter(order, f / (SR / 2), kind, output='sos')
    return sosfilt(sos, x)


def noise(d):
    return rng.standard_normal(int(d * SR))


def saw(f, t, detune=0.0, phase=0.0):
    ph = (f * (1 + detune) * t + phase) % 1.0
    return 2 * ph - 1


def place(sig, t0, gain=1.0, pan=0.0, rev=0.0, bus=None):
    bus = dry if bus is None else bus
    i0 = int(round(t0 * SR))
    if i0 >= N:
        return
    sig = sig[: N - i0] * gain
    a = (pan + 1) * np.pi / 4
    l, r = np.cos(a) * np.sqrt(2), np.sin(a) * np.sqrt(2)
    bus[0, i0:i0 + len(sig)] += sig * l
    bus[1, i0:i0 + len(sig)] += sig * r
    if rev:
        send[0, i0:i0 + len(sig)] += sig * l * rev
        send[1, i0:i0 + len(sig)] += sig * r * rev


# ---------------- instrumentos ----------------
def kick():
    t = tt(0.5)
    f = 42 + 120 * np.exp(-t * 32)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6.5)
    click = flt(noise(0.5), 'highpass', 2500) * np.exp(-t * 250) * 0.4
    return np.tanh(1.8 * (s + click))


def sub808(m, d):
    t = tt(d)
    f = mf(m) * (1 + 0.6 * np.exp(-t * 40))
    env = np.minimum(1, t / 0.004) * np.exp(-t * 0.9) * np.minimum(1, (d - t) / 0.04)
    return np.tanh(2.2 * np.sin(2 * np.pi * np.cumsum(f) / SR) * env) * 0.45


def clap():
    t = tt(0.45)
    n = flt(noise(0.45), 'bp', (900, 6000))
    env = sum(np.exp(-np.maximum(0, t - o) * 180) * (t >= o) for o in (0, 0.011, 0.022)) + 0.6 * np.exp(-t * 14) * (t >= 0.03)
    body = np.sin(2 * np.pi * 210 * t) * np.exp(-t * 35) * 0.4
    return (n * env + body) * 1.2


def hat(open_=False):
    d = 0.35 if open_ else 0.06
    t = tt(d)
    return flt(noise(d), 'highpass', 7000) * np.exp(-t * (11 if open_ else 75)) * 0.8


def taiko(big=1.0):
    t = tt(1.2)
    f = 55 + 45 * np.exp(-t * 18)
    s = 0.7 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 5)
    sk = flt(noise(1.2), 'lowpass', 600) * np.exp(-t * 22) * 0.8
    return np.tanh(1.5 * big * (s + sk))


def snare_hit():
    t = tt(0.25)
    return (flt(noise(0.25), 'bp', (1500, 9000)) * np.exp(-t * 22) + np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30) * 0.5) * 0.7


def impact(size=1.0):
    d = 3.0
    t = tt(d)
    boom = 0.55 * np.sin(2 * np.pi * np.cumsum(30 + 40 * np.exp(-t * 6)) / SR) * np.exp(-t * 2.2)
    body = flt(noise(d), 'lowpass', 900) * np.exp(-t * 5) * 0.7
    crack = flt(noise(d), 'highpass', 3000) * np.exp(-t * 28) * 0.5
    return np.tanh(1.6 * (boom + body + crack)) * size


def crash():
    t = tt(2.5)
    return flt(noise(2.5), 'highpass', 4500) * np.exp(-t * 2.2) * 0.35


def braam(notes, d, bright=2400):
    t = tt(d)
    s = sum(saw(mf(m), t, dt) for m in notes for dt in (-0.006, 0, 0.007))
    s /= len(notes) * 3
    dark, open_ = flt(s, 'lowpass', 280, 4), flt(s, 'lowpass', bright, 4)
    x = np.clip(t / 0.35, 0, 1) * np.exp(-t * 1.5)          # el filtro se abre y vuelve a cerrar
    env = np.minimum(1, t / 0.015) * np.exp(-t * 0.55) * np.minimum(1, (d - t) / 0.3)
    return np.tanh(2.5 * (dark * (1 - x) + open_ * x)) * env


def pad(notes, d, cutoff=2200, attack=0.4):
    t = tt(d)
    out = np.zeros((2, len(t)))
    for ch, sign in ((0, -1), (1, 1)):
        s = sum(saw(mf(m), t, sign * 0.004 * (k + 1), phase=0.17 * k) for k, m in enumerate(notes))
        out[ch] = flt(s / len(notes), 'lowpass', cutoff, 2)
    env = np.minimum(1, t / attack) * np.minimum(1, (d - t) / 0.35)
    return out * env * 2.2


def pluck(m, d=0.16):
    t = tt(d)
    s = saw(mf(m), t) + 0.5 * saw(mf(m), t, 0.005)
    bright = flt(s, 'lowpass', 4200) * np.exp(-t * 26)
    body = flt(s, 'lowpass', 1300) * np.exp(-t * 11)
    return (bright + body) * 0.9 * np.minimum(1, (d - t) / 0.01)



def lead(m, d):
    t = tt(d)
    vib = 1 + 0.004 * np.sin(2 * np.pi * 5.5 * t) * np.clip((t - 0.2) / 0.3, 0, 1)
    ph = lambda f, dt: (np.cumsum(f * vib * (1 + dt)) / SR) % 1.0
    s = sum(2 * ph(mf(m), dt) - 1 for dt in (-0.006, 0, 0.006)) / 3 + 0.4 * (2 * ph(mf(m - 12), 0.003) - 1)
    s = flt(s, 'lowpass', 3800, 2)
    env = np.minimum(1, t / 0.05) * (0.75 + 0.25 * np.exp(-t * 4)) * np.minimum(1, (d - t) / 0.08)
    return s * env * 0.9


def riser(d):
    t = tt(d)
    x = t / d
    f = 180 * (8 ** x)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.25
    ns = flt(noise(d), 'highpass', 900) * 0.6
    return (tone + ns) * x ** 2.2


def revcym(d):
    t = tt(d)
    return flt(noise(d), 'highpass', 5000) * (t / d) ** 3 * 0.6


def whoosh(d=0.4):
    t = tt(d)
    return flt(noise(d), 'bp', (400, 5000)) * np.sin(np.pi * t / d) ** 2 * 0.5


def add_stereo(sig2, t0, gain=1.0, rev=0.0, bus=None):
    bus = dry if bus is None else bus
    i0 = int(round(t0 * SR))
    L = min(sig2.shape[1], N - i0)
    bus[:, i0:i0 + L] += sig2[:, :L] * gain
    if rev:
        send[:, i0:i0 + L] += sig2[:, :L] * gain * rev


def K(t0, g=1.0):
    place(kick(), t0, g)
    kicks.append(t0)


# ---------------- arreglo ----------------
BEAT, STEP = 0.5, 0.125
AM, F, CM, G = [57, 60, 64, 69], [53, 57, 60, 65], [55, 60, 64, 67], [55, 59, 62, 67]
BASS = {'Am': 33, 'F': 29, 'C': 36, 'G': 31}
CH = {'Am': AM, 'F': F, 'C': CM, 'G': G}

def arrange15():
    # 0-3: apertura
    place(impact(1.0), 0.0, 0.9, rev=0.5)
    place(braam([33, 45, 52], 2.8), 0.0, 0.75, rev=0.3)
    add_stereo(pad([45, 52, 57, 60], 2.88, cutoff=900, attack=1.0), 0.0, 0.35, rev=0.4)
    for i, t0 in enumerate((0.5, 1.0, 1.5)):
        place(taiko(1.0), t0, 0.85, rev=0.35)
        place(sub808(33, 0.45), t0, 0.5)
    place(taiko(1.3), 2.0, 1.0, rev=0.4)
    place(impact(0.5), 2.0, 0.5, rev=0.4)
    for k in range(int(1.0 / 0.25)):                          # tic-tac en corcheas
        place(hat(), 0.5 + k * 0.25, 0.35 + 0.1 * k, pan=0.3 if k % 2 else -0.3)
    t0 = 1.5
    while t0 < 2.86:                                          # semicorcheas crecientes
        place(hat(), t0, 0.5 + 0.4 * (t0 - 1.5), pan=0.3 if int(t0 / STEP) % 2 else -0.3)
        t0 += STEP
    t0, g = 2.25, 0.35
    while t0 < 2.86:                                          # redoble de taikos
        place(taiko(0.7), t0, g, rev=0.2)
        t0 += 0.0625
        g = min(0.9, g + 0.06)
    place(riser(1.86), 1.0, 0.55, rev=0.3)
    place(revcym(0.86), 2.0, 0.8, rev=0.2)

    # 3-11: drop (Am F C G)
    place(impact(1.2), 3.0, 1.0, rev=0.6)
    place(braam([33, 45, 52, 57], 2.0), 3.0, 0.6, rev=0.3)
    place(crash(), 3.0, 1.0, rev=0.3)
    KICK_STEPS, CLAP_STEPS = [0, 6, 10], [4, 12]
    ARP = [0, 2, 1, 3, 2, 1, 0, 2]
    for b, ch in enumerate(['Am', 'F', 'C', 'G']):
        bt = 3.0 + b * 2.0
        notes = CH[ch]
        add_stereo(pad([n - 12 for n in notes] + [notes[2]], 2.0, cutoff=2600, attack=0.05), bt, 0.32, rev=0.4, bus=duck_bus)
        for s in range(16):
            ts = bt + s * STEP
            if s in KICK_STEPS:
                K(ts)
                nxt = [k for k in KICK_STEPS if k > s]
                dur = ((nxt[0] if nxt else 16) - s) * STEP
                place(sub808(BASS[ch], dur), ts, 0.9)
            if s in CLAP_STEPS:
                place(clap(), ts, 0.85, rev=0.35)
                place(snare_hit(), ts, 0.4, rev=0.25)
            if s % 8 == 0:
                place(taiko(0.8), ts, 0.45, rev=0.3)
            place(hat(), ts, [0.5, 0.25, 0.35, 0.25][s % 4], pan=0.25 if s % 2 else -0.25)
            if s == 14 and b % 2 == 1:
                for r in range(4):
                    place(hat(), ts + r * STEP / 2, 0.3, pan=0.2)
            if s == 14 and b % 2 == 0:
                place(hat(True), ts, 0.4, pan=0.1)
            m = notes[ARP[s % 8]] + 12
            place(pluck(m), ts, 0.55 if s % 4 == 0 else 0.4, pan=-0.45 if s % 2 else 0.45, rev=0.25, bus=duck_bus)
            if s % 4 == 0:
                place(pluck(m - 12, 0.3), ts, 0.3, rev=0.2, bus=duck_bus)
        if b > 0:
            place(whoosh(0.35), bt - 0.35, 0.8, rev=0.2)
            place(impact(0.55), bt, 0.55, rev=0.5)
            place(crash(), bt, 0.6, rev=0.2)

    # 11-13: build (F -> G), golpe en cada palabra
    for i, (t0, ch) in enumerate([(11.0, 'F'), (11.5, 'F'), (12.0, 'G'), (12.5, 'G')]):
        K(t0, 1.0)
        place(sub808(BASS[ch], 0.48), t0, 0.95)
        place(taiko(1.2), t0, 0.8, rev=0.4)
        place(clap(), t0, 0.6, rev=0.4)
        place(impact(0.4), t0, 0.35, rev=0.4)
        add_stereo(pad([n - 12 for n in CH[ch]] + [CH[ch][2] + 12], 0.5, cutoff=3200, attack=0.01), t0, 0.35, rev=0.5, bus=duck_bus)
        for s in range(4):
            m = CH[ch][ARP[s]] + 12 + (12 if i >= 2 else 0)
            place(pluck(m), t0 + s * STEP, 0.5, pan=-0.4 if s % 2 else 0.4, rev=0.3, bus=duck_bus)
    for k in range(16):
        place(hat(), 11.0 + k * STEP, 0.45, pan=0.25 if k % 2 else -0.25)
    t0, iv, g = 12.0, 0.125, 0.3                             # redoble acelerado
    while t0 < 12.86:
        place(snare_hit(), t0, g, pan=0.0, rev=0.3)
        t0 += iv
        iv = max(0.03, iv * 0.85)
        g = min(0.85, g + 0.035)
    place(riser(1.86), 11.0, 0.6, rev=0.3)
    place(revcym(0.86), 12.0, 0.9, rev=0.2)

    # 13-15: final en Do mayor (add9)
    place(impact(1.3), 13.0, 1.0, rev=0.7)
    place(braam([36, 48, 55], 2.0, bright=3200), 13.0, 0.6, rev=0.4)
    place(crash(), 13.0, 1.0, rev=0.4)
    K(13.0)
    place(sub808(36, 1.9), 13.0, 0.9)
    add_stereo(pad([48, 55, 60, 62, 64, 67, 72], 2.0, cutoff=3400, attack=0.02), 13.0, 0.45, rev=0.7)
    for k, m in enumerate([72, 76, 79, 84, 86, 88]):           # arpegio ascendente luminoso
        place(pluck(m, 0.6), 13.0 + 0.125 * k, 0.32, pan=-0.5 + 0.2 * k, rev=0.7)


    # melodía heroica (lead)
    MEL = {'Am': [(69, 1), (72, 1), (76, 2)], 'F': [(77, 1.5), (76, .5), (72, 2)],
           'C': [(76, 1), (79, 1), (84, 2)], 'G': [(83, 1.5), (81, .5), (79, 2)]}
    for b, ch in enumerate(['Am', 'F', 'C', 'G']):
        tb = 3.0 + b * 2.0
        for m, beats in MEL[ch]:
            place(lead(m, beats * BEAT * 0.98), tb, 0.38, pan=0.0, rev=0.45)
            tb += beats * BEAT
    for t0, m in ((11.0, 81), (11.5, 79), (12.0, 83), (12.5, 86)):
        place(lead(m, 0.48), t0, 0.38, rev=0.5)
    place(lead(88, 1.9), 13.0, 0.4, rev=0.7)
    place(lead(84, 1.9), 13.0, 0.3, rev=0.7)



def arrange30():
    # 0-5: apertura (frases en 1, 2, 3; "IMPORTA" en 4)
    place(impact(1.0), 0.0, 0.9, rev=0.5)
    place(braam([33, 45, 52], 4.8), 0.0, 0.7, rev=0.3)
    add_stereo(pad([45, 52, 57, 60], 4.88, cutoff=900, attack=1.5), 0.0, 0.35, rev=0.4)
    for t0 in (1.0, 2.0, 3.0):
        place(taiko(1.0), t0, 0.85, rev=0.35)
        place(sub808(33, 0.9), t0, 0.5)
    place(taiko(1.3), 4.0, 1.0, rev=0.4)
    place(impact(0.5), 4.0, 0.5, rev=0.4)
    for k in range(8):                                      # pulso de corcheas
        place(hat(), 1.0 + k * 0.25, 0.3 + 0.04 * k, pan=0.3 if k % 2 else -0.3)
        place(pluck(45 + 12, 0.2), 1.0 + k * 0.25, 0.25, rev=0.2, bus=duck_bus)
    t0 = 3.0
    while t0 < 4.86:                                        # semicorcheas crecientes
        place(hat(), t0, 0.45 + 0.25 * (t0 - 3.0), pan=0.3 if int(t0 / STEP) % 2 else -0.3)
        place(pluck(57 if int(t0 / STEP) % 2 else 64, 0.12), t0, 0.22 + 0.1 * (t0 - 3.0), rev=0.2, bus=duck_bus)
        t0 += STEP
    t0, g = 4.25, 0.35
    while t0 < 4.86:                                        # redoble de taikos
        place(taiko(0.7), t0, g, rev=0.2)
        t0 += 0.0625
        g = min(0.9, g + 0.06)
    place(riser(2.88), 2.0, 0.55, rev=0.3)
    place(revcym(0.88), 4.0, 0.8, rev=0.2)

    # 5-21: cuerpo (2 vueltas de Am F C G)
    place(impact(1.2), 5.0, 1.0, rev=0.6)
    place(braam([33, 45, 52, 57], 2.0), 5.0, 0.6, rev=0.3)
    place(crash(), 5.0, 1.0, rev=0.3)
    KICK_STEPS, CLAP_STEPS = [0, 6, 10], [4, 12]
    ARP = [0, 2, 1, 3, 2, 1, 0, 2]
    MEL = {'Am': [(69, 1), (72, 1), (76, 2)], 'F': [(77, 1.5), (76, .5), (72, 2)],
           'C': [(76, 1), (79, 1), (84, 2)], 'G': [(83, 1.5), (81, .5), (79, 2)]}
    for b, ch in enumerate(['Am', 'F', 'C', 'G'] * 2):
        bt = 5.0 + b * 2.0
        notes = CH[ch]
        second = b >= 4
        add_stereo(pad([n - 12 for n in notes] + [notes[2]], 2.0, cutoff=2600 if not second else 3400, attack=0.05), bt, 0.32, rev=0.4, bus=duck_bus)
        for s in range(16):
            ts = bt + s * STEP
            if s in KICK_STEPS or (second and s == 14):
                K(ts)
                ks = KICK_STEPS + ([14] if second else [])
                nxt = [k for k in ks if k > s]
                place(sub808(BASS[ch], ((nxt[0] if nxt else 16) - s) * STEP), ts, 0.9)
            if s in CLAP_STEPS:
                place(clap(), ts, 0.85, rev=0.35)
                place(snare_hit(), ts, 0.4, rev=0.25)
            if s % 8 == 0:
                place(taiko(0.8), ts, 0.45, rev=0.3)
            place(hat(), ts, [0.5, 0.25, 0.35, 0.25][s % 4], pan=0.25 if s % 2 else -0.25)
            if s == 14 and b % 2 == 1:
                for r in range(4):
                    place(hat(), ts + r * STEP / 2, 0.3, pan=0.2)
            if (s == 14 and b % 2 == 0) or (second and s in (2, 10)):
                place(hat(True), ts, 0.35, pan=0.1)
            m = notes[ARP[s % 8]] + 12
            place(pluck(m), ts, 0.55 if s % 4 == 0 else 0.4, pan=-0.45 if s % 2 else 0.45, rev=0.25, bus=duck_bus)
            if s % 4 == 0:
                place(pluck(m - 12, 0.3), ts, 0.3, rev=0.2, bus=duck_bus)
        tb = bt
        for m, beats in MEL[ch]:
            place(lead(m, beats * BEAT * 0.98), tb, 0.38, rev=0.45)
            if second:
                place(lead(m - 4 if ch in ('C', 'Am') else m - 3, beats * BEAT * 0.98), tb, 0.2, pan=0.3, rev=0.5)
            tb += beats * BEAT
        if b in (2, 4, 6):                                   # cambios de escena: 9, 13, 17
            place(whoosh(0.35), bt - 0.35, 0.8, rev=0.2)
            place(impact(0.55), bt, 0.55, rev=0.5)
        if b > 0:
            place(crash(), bt, 0.6 if b in (2, 4, 6) else 0.35, rev=0.2)

    # 21-25: build, una palabra por segundo (F G Am G -> C)
    for i, (t0, ch, lm) in enumerate([(21.0, 'F', 81), (22.0, 'G', 83), (23.0, 'Am', 84), (24.0, 'G', 86)]):
        K(t0, 1.0)
        K(t0 + 0.5, 0.7)
        place(sub808(BASS[ch], 0.95), t0, 0.95)
        place(taiko(1.2), t0, 0.8, rev=0.4)
        place(clap(), t0, 0.6, rev=0.4)
        place(clap(), t0 + 0.5, 0.5, rev=0.4)
        place(impact(0.45), t0, 0.4, rev=0.4)
        add_stereo(pad([n - 12 for n in CH[ch]] + [CH[ch][2] + 12], 1.0, cutoff=3200, attack=0.01), t0, 0.35, rev=0.5, bus=duck_bus)
        for s in range(8):
            m = CH[ch][ARP[s]] + 12 + (12 if i >= 2 else 0)
            place(pluck(m), t0 + s * STEP, 0.5, pan=-0.4 if s % 2 else 0.4, rev=0.3, bus=duck_bus)
        place(lead(lm, 0.95), t0, 0.38, rev=0.5)
    for k in range(32):
        place(hat(), 21.0 + k * STEP, 0.45, pan=0.25 if k % 2 else -0.25)
    t0, iv, g = 23.0, 0.25, 0.25                            # redoble acelerado
    while t0 < 24.86:
        place(snare_hit(), t0, g, rev=0.3)
        t0 += iv
        iv = max(0.03, iv * 0.88)
        g = min(0.85, g + 0.025)
    place(riser(3.88), 21.0, 0.6, rev=0.3)
    place(revcym(0.88), 24.0, 0.9, rev=0.2)

    # 25-30: final en Do mayor (add9)
    place(impact(1.3), 25.0, 1.0, rev=0.7)
    place(braam([36, 48, 55], 3.0, bright=3200), 25.0, 0.6, rev=0.4)
    place(crash(), 25.0, 1.0, rev=0.4)
    K(25.0)
    place(sub808(36, 3.0), 25.0, 0.9)
    add_stereo(pad([48, 55, 60, 62, 64, 67, 72], 4.9, cutoff=3400, attack=0.02), 25.0, 0.45, rev=0.7)
    for k, m in enumerate([72, 76, 79, 84, 86, 88]):
        place(pluck(m, 0.8), 25.0 + 0.125 * k, 0.32, pan=-0.5 + 0.2 * k, rev=0.7)
    for k, m in enumerate([84, 79, 76, 72]):                # eco descendente
        place(pluck(m, 0.8), 27.0 + 0.5 * k, 0.18, pan=0.4 - 0.25 * k, rev=0.8)
    place(lead(88, 4.0), 25.0, 0.4, rev=0.7)
    place(lead(84, 4.0), 25.0, 0.3, rev=0.7)
    place(taiko(0.9), 27.0, 0.4, rev=0.6)

(arrange15 if DUR == 15 else arrange30)()

# ---------------- mezcla ----------------
duck = np.ones(N)
tN = np.arange(N) / SR
for tk in kicks:
    i0 = int(tk * SR)
    seg = tN[i0:] - tk
    duck[i0:] = np.minimum(duck[i0:], 1 - 0.55 * np.exp(-seg * 9))
mix = dry + duck_bus * duck

# reverb por convolución (IR sintética estéreo, 2.2 s)
ir_t = tt(2.2)
ir = np.stack([flt(noise(2.2), 'lowpass', 6000) * np.exp(-ir_t * 3.0) for _ in range(2)])
ir[:, : int(0.02 * SR)] *= np.linspace(0, 1, int(0.02 * SR))
wet = np.stack([fftconvolve(flt(send[c], 'highpass', 200), ir[c])[:N] for c in range(2)])
wet /= np.max(np.abs(wet)) + 1e-9
mix += wet * 0.35 * np.max(np.abs(mix))

# compuertas de silencio dramático antes de cada drop
gate = np.ones(N)
for a, b in (((2.88, 3.0), (12.88, 13.0)) if DUR == 15 else ((4.88, 5.0), (24.88, 25.0))):
    i0, i1 = int(a * SR), int(b * SR)
    gate[i0:i1] = 0
    r = int(0.004 * SR)
    gate[i0 - r:i0] = np.linspace(1, 0, r)
mix *= gate
mix *= np.minimum(1, (DUR - tN) / (1.2 if DUR == 15 else 1.6))                   # fundido final

mix = flt(mix, 'highpass', 28)
mix = mix + 0.6 * flt(mix, 'highpass', 3500)            # realce de brillo (shelf)
mix /= np.max(np.abs(mix))
mix = np.tanh(1.6 * mix) / np.tanh(1.6)                  # saturación/limitación suave
mix *= 0.93

pcm = (np.clip(mix.T, -1, 1) * 32767).astype(np.int16)
with wave.open('snd/music.wav' if DUR == 15 else f'snd/music{int(DUR)}.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print('ok', pcm.shape)
