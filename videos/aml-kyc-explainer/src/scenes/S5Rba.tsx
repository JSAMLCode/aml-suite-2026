import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C, FONT, IN, OUT, ease, sp} from '../theme';
import {SectionLabel, Source} from '../ui';

const LV = [
  {k: 'BAJO', d: 'Diligencia simplificada', c: C.teal, h: 260},
  {k: 'MEDIO', d: 'Diligencia estándar', c: C.gold, h: 440},
  {k: 'ALTO', d: 'Diligencia reforzada', c: C.coral, h: 620},
];

export const S5Rba: React.FC = () => {
  const f = useCurrentFrame();
  const exit = ease(f, 104, 120, [0, 1], IN);
  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: FONT}}>
      <SectionLabel n="04" title="Enfoque basado en riesgo" />
      <AbsoluteFill style={{opacity: 1 - exit, transform: `scale(${1 + exit * 0.5})`, transformOrigin: '50% 60%'}}>
        <div style={{position: 'absolute', top: 440, width: '100%', textAlign: 'center', color: C.white, fontSize: 78, fontWeight: 900, lineHeight: 1.05, opacity: ease(f, 4, 20)}}>
          A mayor riesgo,<br /><span style={{color: C.goldL}}>mayor diligencia.</span>
        </div>
        {LV.map((l, i) => {
          const p = ease(f, 18 + i * 14, 52 + i * 14, [0, 1], OUT);
          const x = 110 + i * 300;
          return (
            <div key={l.k}>
              <div style={{position: 'absolute', left: x, width: 260, bottom: 1920 - 1400, height: l.h * p, borderRadius: '18px 18px 0 0', background: `linear-gradient(${l.c}, ${C.navy2})`, boxShadow: `0 0 40px ${l.c}55`}} />
              <div style={{position: 'absolute', left: x, width: 260, top: 1420, textAlign: 'center', opacity: ease(f, 40 + i * 14, 56 + i * 14)}}>
                <div style={{fontSize: 44, fontWeight: 900, letterSpacing: 6, color: l.c}}>{l.k}</div>
                <div style={{fontSize: 22, fontWeight: 600, color: C.mute, marginTop: 6, lineHeight: 1.2}}>{l.d}</div>
              </div>
            </div>
          );
        })}
      </AbsoluteFill>
      <Source text="DILIGENCIA SIMPLIFICADA · ESTÁNDAR · REFORZADA" />
    </AbsoluteFill>
  );
};
