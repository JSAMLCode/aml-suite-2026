import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C, FONT, FPS, ease} from './theme';

// Rótulo de sección: llega con barra dorada que se estira y texto que sube por máscara
export const SectionLabel: React.FC<{n: string; title: string; dark?: boolean; at?: number}> = ({
  n,
  title,
  dark,
  at = 4,
}) => {
  const f = useCurrentFrame();
  const bar = ease(f, at, at + 14);
  const txt = ease(f, at + 4, at + 20);
  const col = dark ? C.navy : C.white;
  return (
    <div style={{position: 'absolute', left: 120, top: 104, fontFamily: FONT, display: 'flex', alignItems: 'center', gap: 22}}>
      <div style={{width: 64 * bar, height: 3, background: dark ? C.navy : C.gold}} />
      <div style={{overflow: 'hidden', height: 34}}>
        <div style={{transform: `translateY(${(1 - txt) * 34}px)`, color: col, fontSize: 24, fontWeight: 700, letterSpacing: 6, textTransform: 'uppercase'}}>
          <span style={{color: dark ? C.navy : C.gold}}>{n}</span>
          <span style={{opacity: 0.85}}> — {title}</span>
        </div>
      </div>
    </div>
  );
};

const pad = (n: number) => String(n).padStart(2, '0');

// Capa de "sala de edición": código de tiempo, esquinas de zona segura y grano
export const EditorHud: React.FC = () => {
  const f = useCurrentFrame();
  const s = Math.floor(f / FPS);
  const tc = `00:00:${pad(s)}:${pad(f % FPS)}`;
  const on = ease(f, 6, 24);
  const corner = (r: number, x: number, y: number) => (
    <div
      key={r}
      style={{
        position: 'absolute',
        left: x,
        top: y,
        width: 46,
        height: 46,
        borderTop: `2px solid ${C.mute}`,
        borderLeft: `2px solid ${C.mute}`,
        transform: `rotate(${r}deg)`,
        opacity: 0.45 * on,
      }}
    />
  );
  return (
    <AbsoluteFill style={{pointerEvents: 'none', fontFamily: FONT}}>
      {corner(0, 56, 56)}
      {corner(90, 1818, 56)}
      {corner(180, 1818, 978)}
      {corner(270, 56, 978)}
      <div style={{position: 'absolute', left: 120, bottom: 66, color: C.mute, fontSize: 20, fontWeight: 600, letterSpacing: 4, opacity: 0.8 * on, fontVariantNumeric: 'tabular-nums'}}>
        TC {tc}
      </div>
      <div style={{position: 'absolute', right: 120, bottom: 66, color: C.mute, fontSize: 20, fontWeight: 600, letterSpacing: 4, opacity: 0.8 * on, display: 'flex', alignItems: 'center', gap: 12}}>
        <div style={{width: 12, height: 12, borderRadius: 6, background: C.coral, opacity: Math.floor(f / 15) % 2 ? 0.35 : 1}} />
        1920×1080 · 30 FPS
      </div>
    </AbsoluteFill>
  );
};

export const Grain: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{pointerEvents: 'none', mixBlendMode: 'overlay', opacity: 0.16}}>
      <svg width="1920" height="1080">
        <filter id="g">
          <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed={f % 12} />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width="1920" height="1080" filter="url(#g)" />
      </svg>
    </AbsoluteFill>
  );
};

export const Vignette: React.FC = () => (
  <AbsoluteFill style={{pointerEvents: 'none', background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,0.55) 100%)'}} />
);

// Destello de corte: sube en 2 fotogramas y cae en 6
export const Flash: React.FC<{at: number; color?: string; max?: number}> = ({at, color = C.white, max = 0.7}) => {
  const f = useCurrentFrame();
  const o = f < at ? ease(f, at - 2, at, [0, max]) : ease(f, at, at + 6, [max, 0]);
  if (o <= 0) return null;
  return <AbsoluteFill style={{background: color, opacity: o, pointerEvents: 'none'}} />;
};
