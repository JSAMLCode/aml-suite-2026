import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C, FONT, IN, ease, sp} from '../theme';
import {SectionLabel, Slam, Stamp, useExit} from '../ui';
import {TL, span, wf} from '../tl';

// Apertura: línea dorada que colapsa en un punto (antes de la voz)
export const S0Open: React.FC = () => {
  const f = useCurrentFrame();
  const grow = ease(f, 0, 16);
  const collapse = ease(f, 18, 30, [0, 1], IN);
  const w = 820 * grow * (1 - collapse);
  const dot = ease(f, 26, 34);
  return (
    <AbsoluteFill style={{background: C.navy}}>
      <div style={{position: 'absolute', left: 540 - w / 2, top: 539, width: w, height: 3, background: C.gold, boxShadow: `0 0 20px ${C.gold}`}} />
      <div style={{position: 'absolute', left: 531, top: 531, width: 18, height: 18, borderRadius: 9, background: C.goldL, transform: `scale(${dot * 1.3})`, boxShadow: `0 0 36px ${C.goldL}`}} />
    </AbsoluteFill>
  );
};

const ID = '01';
const LEN = span(ID).len;

export const S1Fecha: React.FC = () => {
  const f = useCurrentFrame();
  const exit = useExit(LEN);
  // el punto de la apertura se abre en la órbita
  const orbit = sp(f, 0, {damping: 18, stiffness: 70});
  const ddmm = wf(ID, 'treinta');
  const year = wf(ID, 'veintisiete');
  const plazo = wf(ID, 'plazo');

  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: FONT}}>
      <AbsoluteFill style={{transform: `scale(${1 + exit * 0.15})`, filter: `blur(${exit * 12}px)`, opacity: 1 - exit * 0.5}}>
        <svg width="1080" height="1080" style={{position: 'absolute'}}>
          <circle cx="540" cy="540" r={9 + orbit * 351} fill="none" stroke={C.mute} strokeOpacity={0.4} strokeWidth={2} strokeDasharray="4 14" transform={`rotate(${f * 0.8} 540 540)`} />
          {[0, 1, 2].map((i) => {
            const a = ((f * 2.2 + i * 120) * Math.PI) / 180;
            const r = 9 + orbit * 351;
            return <circle key={i} cx={540 + Math.cos(a) * r} cy={540 + Math.sin(a) * r} r={i === 0 ? 9 : 6} fill={i === 0 ? C.teal : C.gold} opacity={orbit} />;
          })}
        </svg>

        {/* 30 · 06: dígito a dígito */}
        <div style={{position: 'absolute', top: 300, width: '100%', display: 'flex', justifyContent: 'center'}}>
          {'30 · 06'.split('').map((ch, i) => {
            const p = sp(f, ddmm + i * 2, {damping: 14, stiffness: 180});
            return (
              <span key={i} style={{display: 'inline-block', minWidth: ch === ' ' ? 30 : undefined, fontSize: 150, fontWeight: 900, color: C.white, opacity: Math.min(1, p * 1.4), transform: `translateY(${(1 - p) * 70}px)`, filter: `blur(${(1 - Math.min(1, p)) * 8}px)`}}>
                {ch}
              </span>
            );
          })}
        </div>

        <Slam text="2027" at={year} size={230} y={590} outline />

        <Stamp text="PLAZO LÍMITE" at={plazo} style={{left: 360, top: 790}} size={34} />
      </AbsoluteFill>
      <SectionLabel n="SBP" title="Acuerdo 1-2026" out={1 - exit} />
    </AbsoluteFill>
  );
};

export const OPEN = TL.open;
