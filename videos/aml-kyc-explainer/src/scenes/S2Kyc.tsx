import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C, FONT, IN, ease, gold, sp} from '../theme';
import {SectionLabel, Source} from '../ui';

const WORDS = [
  {t: 'KYC', sub: 'Conoce a tu cliente'},
  {t: 'CDD', sub: 'Debida diligencia'},
  {t: 'UBO', sub: 'Beneficiario final'},
];

export const S2Kyc: React.FC = () => {
  const f = useCurrentFrame();
  const exit = ease(f, 104, 120, [0, 1], IN);
  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: FONT}}>
      <SectionLabel n="01" title="Fundamento" />
      <AbsoluteFill style={{transform: `translateY(${-exit * 300}px)`, opacity: 1 - exit}}>
        {WORDS.map((w, i) => {
          const at = 14 + i * 20;
          const p = sp(f, at, {damping: 13, stiffness: 200, mass: 0.7});
          const echo = sp(f, at + 5, {damping: 16, stiffness: 140});
          return (
            <div key={w.t} style={{position: 'absolute', top: 460 + i * 340, left: 0, width: '100%', textAlign: 'center'}}>
              <div style={{position: 'absolute', width: '100%', fontSize: 250, fontWeight: 900, letterSpacing: 6, color: 'transparent', WebkitTextStroke: `2px ${C.deep}`, opacity: echo, transform: `translate(${(1 - echo) * 80}px, 14px)`}}>{w.t}</div>
              <div style={{position: 'relative', fontSize: 250, fontWeight: 900, letterSpacing: 6, lineHeight: 1, backgroundImage: i === 1 ? gold : 'none', WebkitBackgroundClip: 'text', color: i === 1 ? 'transparent' : C.white, opacity: Math.min(1, p * 1.5), transform: `translateX(${(1 - p) * (i % 2 ? 400 : -400)}px) scale(${0.85 + 0.15 * p})`}}>{w.t}</div>
              <div style={{marginTop: 4, color: C.mute, fontSize: 30, fontWeight: 700, letterSpacing: 8, textTransform: 'uppercase', opacity: ease(f, at + 8, at + 22)}}>{w.sub}</div>
            </div>
          );
        })}
      </AbsoluteFill>
      <Source text="MARCO · LEY 23 DE 27 DE ABRIL DE 2015 (PANAMÁ)" />
    </AbsoluteFill>
  );
};
