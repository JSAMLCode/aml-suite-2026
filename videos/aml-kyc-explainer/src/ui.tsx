import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C, FONT, FPS, H, W, ease} from './theme';

export const SectionLabel: React.FC<{n: string; title: string; at?: number}> = ({n, title, at = 4}) => {
  const f = useCurrentFrame();
  const bar = ease(f, at, at + 14);
  const txt = ease(f, at + 4, at + 20);
  return (
    <div style={{position: 'absolute', left: 90, top: 250, fontFamily: FONT, display: 'flex', alignItems: 'center', gap: 20}}>
      <div style={{width: 56 * bar, height: 3, background: C.gold}} />
      <div style={{overflow: 'hidden', height: 30}}>
        <div style={{transform: `translateY(${(1 - txt) * 30}px)`, color: C.white, fontSize: 21, fontWeight: 700, letterSpacing: 5, textTransform: 'uppercase'}}>
          <span style={{color: C.gold}}>{n}</span>
          <span style={{opacity: 0.85}}> — {title}</span>
        </div>
      </div>
    </div>
  );
};

export const Source: React.FC<{text: string; at?: number}> = ({text, at = 20}) => {
  const f = useCurrentFrame();
  return (
    <div style={{position: 'absolute', left: 90, right: 90, bottom: 250, fontFamily: FONT, color: C.mute, fontSize: 20, fontWeight: 600, letterSpacing: 3, opacity: ease(f, at, at + 14) * 0.9}}>
      {text}
    </div>
  );
};

const pad = (n: number) => String(n).padStart(2, '0');

export const EditorHud: React.FC = () => {
  const f = useCurrentFrame();
  const on = ease(f, 6, 24);
  const corner = (r: number, x: number, y: number) => (
    <div key={r} style={{position: 'absolute', left: x, top: y, width: 40, height: 40, borderTop: `2px solid ${C.mute}`, borderLeft: `2px solid ${C.mute}`, transform: `rotate(${r}deg)`, opacity: 0.45 * on}} />
  );
  const t = {position: 'absolute', bottom: 170, color: C.mute, fontSize: 18, fontWeight: 600, letterSpacing: 4, opacity: 0.8 * on, fontFamily: FONT} as const;
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {corner(0, 48, 150)}
      {corner(90, W - 88, 150)}
      {corner(180, W - 88, H - 190)}
      {corner(270, 48, H - 190)}
      <div style={{...t, left: 90, fontVariantNumeric: 'tabular-nums'}}>TC 00:{pad(Math.floor(f / FPS))}:{pad(f % FPS)}</div>
      <div style={{...t, right: 90, display: 'flex', alignItems: 'center', gap: 10}}>
        <div style={{width: 10, height: 10, borderRadius: 5, background: C.coral, opacity: Math.floor(f / 15) % 2 ? 0.35 : 1}} />
        1080×1920 · 30 FPS
      </div>
    </AbsoluteFill>
  );
};

export const Grain: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{pointerEvents: 'none', mixBlendMode: 'overlay', opacity: 0.16}}>
      <svg width={W} height={H}>
        <filter id="g">
          <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed={f % 12} />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width={W} height={H} filter="url(#g)" />
      </svg>
    </AbsoluteFill>
  );
};

export const Vignette: React.FC = () => (
  <AbsoluteFill style={{pointerEvents: 'none', background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,0.55) 100%)'}} />
);

export const Flash: React.FC<{at: number; color?: string; max?: number}> = ({at, color = C.white, max = 0.7}) => {
  const f = useCurrentFrame();
  const o = f < at ? ease(f, at - 2, at, [0, max]) : ease(f, at, at + 6, [max, 0]);
  if (o <= 0) return null;
  return <AbsoluteFill style={{background: color, opacity: o, pointerEvents: 'none'}} />;
};
