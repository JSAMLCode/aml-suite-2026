import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C, FONT, IN, ease, gold, shake, sp} from '../theme';

const LINE1 = 'CADA FOTOGRAMA';
const IMPACT = 58;

export const S1ColdOpen: React.FC = () => {
  const f = useCurrentFrame();

  // Línea dorada: crece desde el centro y colapsa a un punto
  const grow = ease(f, 0, 18);
  const collapse = ease(f, 20, 32, [0, 1], IN);
  const lineW = 1400 * grow * (1 - collapse);
  const dot = ease(f, 26, 34) * (1 - ease(f, 34, 42));

  // Golpe de "CUENTA."
  const slam = sp(f, IMPACT - 6, {damping: 12, stiffness: 260, mass: 0.6});
  const sh = shake(f, IMPACT, 22, 16);
  const wave = ease(f, IMPACT, IMPACT + 26);

  // Salida hacia el corte
  const exit = ease(f, 78, 90, [0, 1], IN);

  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: FONT}}>
      <AbsoluteFill
        style={{
          transform: `translate(${sh.x}px, ${sh.y}px) scale(${1 + exit * 0.18})`,
          filter: `blur(${exit * 14}px)`,
          opacity: 1 - exit * 0.6,
        }}
      >
        {/* línea y punto */}
        <div style={{position: 'absolute', left: 960 - lineW / 2, top: 539, width: lineW, height: 3, background: gold, boxShadow: `0 0 24px ${C.gold}`}} />
        <div style={{position: 'absolute', left: 960 - 9, top: 531, width: 18, height: 18, borderRadius: 9, background: C.goldL, transform: `scale(${dot * 1.4})`, boxShadow: `0 0 40px ${C.goldL}`}} />

        {/* onda expansiva */}
        {f >= IMPACT && (
          <svg width="1920" height="1080" style={{position: 'absolute'}}>
            {[0, 7].map((d) => {
              const w = ease(f, IMPACT + d, IMPACT + d + 30);
              return <circle key={d} cx="960" cy="610" r={80 + w * 1000} fill="none" stroke={C.gold} strokeWidth={10 * (1 - w)} opacity={1 - w} />;
            })}
          </svg>
        )}

        {/* CADA FOTOGRAMA: letra a letra */}
        <div style={{position: 'absolute', top: 360, width: '100%', display: 'flex', justifyContent: 'center'}}>
          {LINE1.split('').map((ch, i) => {
            const p = sp(f, 30 + i * 1.5, {damping: 14, stiffness: 180});
            return (
              <span
                key={i}
                style={{
                  display: 'inline-block',
                  minWidth: ch === ' ' ? 40 : undefined,
                  fontSize: 120,
                  fontWeight: 900,
                  letterSpacing: 6,
                  color: C.white,
                  opacity: Math.min(1, p * 1.4),
                  transform: `translateY(${(1 - p) * 70}px) rotate(${(1 - p) * 8}deg)`,
                  filter: `blur(${(1 - Math.min(1, p)) * 10}px)`,
                }}
              >
                {ch}
              </span>
            );
          })}
        </div>

        {/* CUENTA. */}
        <div
          style={{
            position: 'absolute',
            top: 500,
            width: '100%',
            textAlign: 'center',
            fontSize: 210,
            fontWeight: 900,
            letterSpacing: 4,
            backgroundImage: gold,
            WebkitBackgroundClip: 'text',
            color: 'transparent',
            opacity: f < IMPACT - 6 ? 0 : 1,
            transform: `scale(${3 - 2 * slam})`,
          }}
        >
          CUENTA.
        </div>
        <div style={{position: 'absolute', top: 760, width: '100%', textAlign: 'center', color: C.mute, fontSize: 26, fontWeight: 600, letterSpacing: 10, opacity: ease(f, 64, 76)}}>
          MOTION GRAPHICS · SHOWREEL
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
