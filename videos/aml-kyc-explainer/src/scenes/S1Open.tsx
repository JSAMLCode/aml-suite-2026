import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C, FONT, H, IN, W, ease, gold, shake, sp} from '../theme';

const IMPACT = 58;

export const S1Open: React.FC = () => {
  const f = useCurrentFrame();
  const grow = ease(f, 0, 18);
  const collapse = ease(f, 20, 32, [0, 1], IN);
  const lineW = 900 * grow * (1 - collapse);
  const dot = ease(f, 26, 34) * (1 - ease(f, 34, 42));
  const slam = sp(f, IMPACT - 6, {damping: 12, stiffness: 260, mass: 0.6});
  const sh = shake(f, IMPACT, 18, 16);
  const exit = ease(f, 78, 90, [0, 1], IN);
  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: FONT}}>
      <AbsoluteFill style={{transform: `translate(${sh.x}px, ${sh.y}px) scale(${1 + exit * 0.18})`, filter: `blur(${exit * 14}px)`, opacity: 1 - exit * 0.6}}>
        <div style={{position: 'absolute', left: W / 2 - lineW / 2, top: H / 2 - 2, width: lineW, height: 3, background: gold, boxShadow: `0 0 24px ${C.gold}`}} />
        <div style={{position: 'absolute', left: W / 2 - 9, top: H / 2 - 10, width: 18, height: 18, borderRadius: 9, background: C.goldL, transform: `scale(${dot * 1.4})`, boxShadow: `0 0 40px ${C.goldL}`}} />
        {f >= IMPACT && (
          <svg width={W} height={H} style={{position: 'absolute'}}>
            {[0, 7].map((d) => {
              const w = ease(f, IMPACT + d, IMPACT + d + 30);
              return <circle key={d} cx={W / 2} cy={H / 2 + 60} r={60 + w * 800} fill="none" stroke={C.gold} strokeWidth={9 * (1 - w)} opacity={1 - w} />;
            })}
          </svg>
        )}
        <div style={{position: 'absolute', top: 640, width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
          {['CONOCE', 'A TU'].map((w, r) => (
            <div key={w} style={{display: 'flex'}}>
              {w.split('').map((ch, i) => {
                const p = sp(f, 30 + r * 8 + i * 1.5, {damping: 14, stiffness: 180});
                return (
                  <span key={i} style={{display: 'inline-block', minWidth: ch === ' ' ? 30 : undefined, fontSize: 140, fontWeight: 900, letterSpacing: 4, color: C.white, opacity: Math.min(1, p * 1.4), transform: `translateY(${(1 - p) * 70}px) rotate(${(1 - p) * 8}deg)`, filter: `blur(${(1 - Math.min(1, p)) * 10}px)`}}>
                    {ch}
                  </span>
                );
              })}
            </div>
          ))}
        </div>
        <div style={{position: 'absolute', top: 960, width: '100%', textAlign: 'center', fontSize: 190, fontWeight: 900, letterSpacing: 2, backgroundImage: gold, WebkitBackgroundClip: 'text', color: 'transparent', opacity: f < IMPACT - 6 ? 0 : 1, transform: `scale(${3 - 2 * slam})`}}>
          CLIENTE.
        </div>
        <div style={{position: 'absolute', top: 1230, width: '100%', textAlign: 'center', color: C.mute, fontSize: 24, fontWeight: 600, letterSpacing: 9, opacity: ease(f, 64, 76)}}>
          EXPLAINER · AML / KYC
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
