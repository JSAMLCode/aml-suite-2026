"""Línea de tiempo común a vídeo y sonido. Cada frase arranca en el pulso
(múltiplo de 15 fotogramas) con al menos 0,3 s de respiro tras la anterior."""
import json, math

FPS, BEAT, OPEN, SIGN = 30, 15, 45, 195
words = json.load(open('words.json'))
t, lines = OPEN, []
for l in words:
    start = t
    lines.append({'id': l['id'], 'start': start, 'dur': l['dur'],
                  'words': [{'w': w['w'], 'f': round(w['s'] * FPS)} for w in l['words']]})
    t = math.ceil((start + (l['speech_end'] + 0.3) * FPS) / BEAT) * BEAT
tl = {'fps': FPS, 'open': OPEN, 'lines': lines, 'sign': t, 'end': t + SIGN}
json.dump(tl, open('src/timeline.json', 'w'), ensure_ascii=False, indent=1)
print('cortes', [l['start'] for l in lines], 'firma', t, 'fin', t + SIGN, f'= {(t + SIGN) / FPS:.1f} s')
