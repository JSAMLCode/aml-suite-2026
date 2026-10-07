import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C, FONT, IN, ease, shake, sp} from '../theme';
import {SectionLabel} from '../ui';

const WORDS = [
  {t: 'RITMO', dir: -1},
  {t: 'PRECISIÓN', dir: 1},
  {t: 'IMPACTO', dir: -1},
];

const BEAT = 75; // inversión de color en el pulso
const BEAT_END = 99;

export const S2Kinetic: React.FC = () => {
  const f = useCurrentFrame();
  const inverted = f >= BEAT && f < BEAT_END;
  const bg = inverted ? C.gold : C.navy;
  const fg = inverted ? C.navy : C.white;
  const sh = shake(f, BEAT, 14, 10);

  return (
    <AbsoluteFill style={{background: bg, fontFamily: FONT}}>
      {/* franjas diagonales que barren el fondo */}
      <AbsoluteFill style={{overflow: 'hidden', opacity: inverted ? 0.12 : 0.06}}>
        {Array.from({length: 14}).map((_, i) => (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: -400 + i * 190 + ((f * 3) % 190),
              top: -200,
              width: 60,
              height: 1600,
              background: fg,
              transform: 'rotate(24deg)',
            }}
          />
        ))}
      </AbsoluteFill>

      <AbsoluteFill style={{transform: `translate(${sh.x}px, ${sh.y}px)`, justifyContent: 'center'}}>
        {WORDS.map((w, i) => {
          const p = sp(f, 6 + i * 12, {damping: 18, stiffness: 140});
          const lag = sp(f, 12 + i * 12, {damping: 26, stiffness: 70});
          const out = ease(f, 104 + i * 3, 116 + i * 3, [0, 1], IN);
          const underline = ease(f, BEAT + i * 3, BEAT + 12 + i * 3);
          return (
            <div key={w.t} style={{position: 'relative', height: 236, overflow: 'hidden', margin: '0 auto', width: 1700}}>
              {/* eco en contorno, con retardo: da profundidad */}
              <div
                style={{
                  position: 'absolute',
                  inset: 0,
                  textAlign: 'center',
                  fontSize: 230,
                  fontWeight: 900,
                  lineHeight: '236px',
                  color: 'transparent',
                  WebkitTextStroke: `2px ${inverted ? C.navy : C.gold}`,
                  opacity: 0.55,
                  transform: `translateX(${(1 - lag) * w.dir * 1900 + 26}px) translateY(${-out * 240}px)`,
                }}
              >
                {w.t}
              </div>
              <div
                style={{
                  position: 'absolute',
                  inset: 0,
                  textAlign: 'center',
                  fontSize: 230,
                  fontWeight: 900,
                  lineHeight: '236px',
                  color: i === 1 && !inverted ? C.gold : fg,
                  transform: `translateX(${(1 - p) * w.dir * 1900}px) translateY(${-out * 240}px) skewX(${(1 - p) * w.dir * -18}deg)`,
                }}
              >
                {w.t}
              </div>
              <div style={{position: 'absolute', bottom: 10, left: 850 - 300 * underline, width: 600 * underline, height: 8, background: fg}} />
            </div>
          );
        })}
      </AbsoluteFill>

      <SectionLabel n="01" title="Tipografía cinética" dark={inverted} />
    </AbsoluteFill>
  );
};
