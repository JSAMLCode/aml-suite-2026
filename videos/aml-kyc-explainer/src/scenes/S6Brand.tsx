import React from 'react';
import {AbsoluteFill, random, useCurrentFrame} from 'remotion';
import {C, FONT, H, INOUT, IN, W, ease, gold, sp} from '../theme';

const PARTS = 90;
const CY = 820;
const RY = 190;
const RX = 1.55 * RY;

export const S6Brand: React.FC = () => {
  const f = useCurrentFrame();
  const conv = ease(f, 6, 70, [0, 1], INOUT);
  const txt = sp(f, 60, {damping: 18, stiffness: 120});
  const track = 56 - 36 * ease(f, 60, 120);
  const sweep = ease(f, 110, 170, [-0.3, 1.3]);
  const end = ease(f, 250, 300, [0, 1], IN);
  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: FONT, opacity: 1 - end * 0.0}}>
      <svg width={W} height={H} style={{position: 'absolute'}}>
        {Array.from({length: PARTS}).map((_, i) => {
          const a = (i / PARTS) * Math.PI * 2;
          const sx = random(`x${i}`) * W;
          const sy = random(`y${i}`) * H;
          const tx = W / 2 + Math.cos(a) * RX * 1.55;
          const ty = CY + Math.sin(a) * RY * 1.55;
          return <circle key={i} cx={sx + (tx - sx) * conv} cy={sy + (ty - sy) * conv} r={3 + 3 * conv} fill={C.goldL} opacity={0.3 + 0.7 * conv} />;
        })}
        <ellipse cx={W / 2} cy={CY} rx={RX * 1.55} ry={RY * 1.55} fill="none" stroke="url(#gg)" strokeWidth={4} opacity={ease(f, 60, 90)} />
        <defs>
          <linearGradient id="gg" x1="0" x2="1">
            <stop offset="0" stopColor={C.goldL} /><stop offset="1" stopColor={C.goldD} />
          </linearGradient>
        </defs>
      </svg>
      <div style={{position: 'absolute', top: CY - 100, width: '100%', textAlign: 'center', fontSize: 140, fontWeight: 900, letterSpacing: track, paddingLeft: track, color: 'transparent', backgroundImage: `linear-gradient(105deg, ${C.goldD} ${sweep * 100 - 40}%, ${C.cream} ${sweep * 100}%, ${C.goldD} ${sweep * 100 + 40}%), ${gold}`, WebkitBackgroundClip: 'text', opacity: txt, transform: `scale(${0.9 + 0.1 * txt})`}}>
        SELENE
      </div>
      <div style={{position: 'absolute', top: 1180, width: '100%', textAlign: 'center', color: C.white, fontSize: 46, fontWeight: 800, lineHeight: 1.2, opacity: ease(f, 100, 124)}}>
        Gestión de riesgo<br />AML / KYC
      </div>
      <div style={{position: 'absolute', top: 1400, width: '100%', textAlign: 'center', color: C.gold, fontSize: 26, fontWeight: 700, letterSpacing: 6, opacity: ease(f, 130, 154), lineHeight: 1.7}}>
        SERRANO LAWYERS &amp; CONSULTANTS<br />PROCOMPLIANCE
      </div>
    </AbsoluteFill>
  );
};
