"""Tiempos por palabra sin Whisper (descarga de modelos bloqueada).
Se mide la voz con RMS (ventanas de 10 ms) y se buscan las pausas. Luego se
anclan las fronteras en cascada: fin de oración (. : ?) a la pausa más larga
cercana, comas a la pausa más cercana, y el resto de palabras se reparte por
sílabas entre anclas. Fronteras de oración: ±30 ms. Palabras sueltas: ±150 ms."""
import json, re, wave
import numpy as np

SRC = '../geolocalizacion-inferencial'
# Guion: script.json (actual). Audio: VOICE_DIR o la voz original
import os
req = json.load(open(os.environ.get('SCRIPT', 'script.json')))
VOICE_DIR = os.environ.get('VOICE_DIR', f'{SRC}/assets/voice')


def load(p):
    w = wave.open(p)
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)
    if w.getnchannels() == 2:
        x = x.reshape(-1, 2).mean(1)
    return x / 32768, w.getframerate()


def syl(w):
    return max(1, len(re.findall(r'[aeiouáéíóúü]+', w.lower())) + (2 if w.upper().strip(',.?:') in ('IP', 'VPN') else 0))


out = []
for line in req['lines']:
    x, sr = load(f"{VOICE_DIR}/{line['id']}.wav")
    hop = sr // 100
    db = np.array([20 * np.log10(np.sqrt(np.mean(x[i:i + hop] ** 2)) + 1e-9) for i in range(0, len(x) - hop, hop)])
    v = db > -45
    first = int(np.argmax(v)) / 100
    last = (len(v) - int(np.argmax(v[::-1]))) / 100
    # pausas: (inicio, fin) de tramos sin voz >= 50 ms dentro del habla
    gaps, s = [], None
    for i, b in enumerate(v):
        t = i / 100
        if not b and s is None and first < t < last:
            s = t
        elif b and s is not None:
            if t - s >= 0.05:
                gaps.append((s, t))
            s = None
    words = line['text'].split()
    sy = np.array([syl(w) for w in words], float)
    cum = np.concatenate([[0], np.cumsum(sy)])
    # anclas: índice de palabra -> tiempo de inicio
    anchors = {0: first, len(words): last}

    def expected(k):
        ks = sorted(anchors)
        lo = max(a for a in ks if a <= k); hi = min(a for a in ks if a >= k)
        if lo == hi:
            return anchors[lo]
        return anchors[lo] + (cum[k] - cum[lo]) / (cum[hi] - cum[lo]) * (anchors[hi] - anchors[lo])

    def snap(ks, tol, prefer_long):
        for k in ks:
            e = expected(k)
            cand = [g for g in gaps if abs((g[0] + g[1]) / 2 - e) < tol]
            if cand:
                g = max(cand, key=lambda g: g[1] - g[0]) if prefer_long else min(cand, key=lambda g: abs((g[0] + g[1]) / 2 - e))
                anchors[k] = g[1]
                gaps.remove(g)

    sent = [i + 1 for i, w in enumerate(words[:-1]) if w[-1] in '.:?']
    comma = [i + 1 for i, w in enumerate(words[:-1]) if w[-1] == ',']
    snap(sent, 1.2, True)
    snap(comma, 0.45, False)
    snap([k for k in range(1, len(words)) if k not in anchors], 0.12, False)
    res = []
    for k, w in enumerate(words):
        res.append({'w': w, 's': round(float(expected(k)), 3), 'e': round(float(expected(k + 1)), 3)})
    out.append({'id': line['id'], 'dur': round(len(x) / sr, 3), 'speech_end': round(last, 3), 'words': res})

json.dump(out, open('words.json', 'w'), ensure_ascii=False, indent=1)
for o in out:
    print(o['id'], ' '.join(f"{w['w']}@{w['s']:.2f}" for w in o['words']))
