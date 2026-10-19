import React from 'react';
import {AbsoluteFill, interpolateColors, useCurrentFrame} from 'remotion';
import {C, FONT, IN, ease, shake, sp} from '../theme';
import {SectionLabel, Source} from '../ui';

const N = 5;
const CELL = 150;
const GAP = 12;
const X0 = (1080 - (N * CELL + (N - 1) * GAP)) / 2;
const Y0 = 480;

const color = (score: number) => {
  const t = (score - 1) / 24;
  return t < 0.5
    ? interpolateColors(t * 2, [0, 1], [C.teal, C.gold])
    : interpolateColors((t - 0.5) * 2, [0, 1], [C.gold, C.coral]);
};

export const S4Matrix: React.FC = () => {
  const f = useCurrentFrame();
  const exit = ease(f, 134, 150, [0, 1], IN);
  const scan = ease(f, 60, 100, [0, 1]);
  const crit = 90;
  const pulse = f > crit ? 0.5 + 0.5 * Math.sin((f - crit) / 3) : 0;
  const sh = shake(f, crit, 10, 12);
  const kpi = [
    {v: '25', l: 'Escenarios P × I'},
    {v: '3', l: 'Niveles'},
    {v: '4', l: 'Factores'},
  ];
  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: FONT}}>
      <SectionLabel n="03" title="Matriz de riesgo" />
      <AbsoluteFill style={{transform: `translate(${sh.x}px, ${sh.y}px) translateY(${-exit * 200}px)`, opacity: 1 - exit}}>
        {Array.from({length: N * N}).map((_, k) => {
          const col = k % N;
          const row = Math.floor(k / N); // 0 = impacto alto
          const prob = col + 1;
          const imp = N - row;
          const score = prob * imp;
          const p = sp(f, 8 + (col + row) * 3, {damping: 14, stiffness: 180});
          const isCrit = score === 25;
          const lit = ease(f, 60 + col * 8, 74 + col * 8);
          return (
            <div key={k} style={{position: 'absolute', left: X0 + col * (CELL + GAP), top: Y0 + row * (CELL + GAP), width: CELL, height: CELL, borderRadius: 14, background: color(score), opacity: (0.28 + 0.5 * lit) * Math.min(1, p), transform: `scale(${p})`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 46, fontWeight: 900, color: C.navy, boxShadow: isCrit && pulse ? `0 0 ${60 * pulse}px ${C.coral}` : 'none', outline: isCrit && pulse ? `4px solid ${C.coral}` : 'none'}}>
              {score}
            </div>
          );
        })}
        <div style={{position: 'absolute', left: X0 + scan * (N * CELL + (N - 1) * GAP) - 3, top: Y0 - 20, width: 6, height: N * CELL + (N - 1) * GAP + 40, background: C.goldL, boxShadow: `0 0 30px ${C.goldL}`, opacity: scan > 0 && scan < 1 ? 1 : 0}} />
        <div style={{position: 'absolute', left: X0, top: Y0 + N * (CELL + GAP) + 6, width: 5 * CELL + 4 * GAP, display: 'flex', justifyContent: 'space-between', color: C.mute, fontSize: 24, fontWeight: 700, letterSpacing: 5}}>
          <span>PROBABILIDAD →</span>
          <span style={{color: C.coral, opacity: pulse ? 1 : 0}}>CRÍTICO</span>
        </div>
        <div style={{position: 'absolute', top: 1370, left: 90, right: 90, display: 'flex', justifyContent: 'space-between'}}>
          {kpi.map((k, i) => {
            const p = ease(f, 70 + i * 8, 90 + i * 8);
            return (
              <div key={k.l} style={{width: 290, textAlign: 'center', opacity: p, transform: `translateY(${(1 - p) * 40}px)`}}>
                <div style={{fontSize: 96, fontWeight: 900, color: C.goldL, lineHeight: 1}}>{k.v}</div>
                <div style={{fontSize: 22, fontWeight: 700, letterSpacing: 3, color: C.mute, textTransform: 'uppercase', marginTop: 8}}>{k.l}</div>
              </div>
            );
          })}
        </div>
      </AbsoluteFill>
      <Source text="PUNTUACIÓN = PROBABILIDAD × IMPACTO · ESQUEMA ILUSTRATIVO" />
    </AbsoluteFill>
  );
};
