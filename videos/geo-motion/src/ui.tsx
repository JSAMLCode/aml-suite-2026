import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C, FONT, FPS, IN, ease, gold, shake, sp} from './theme';
import {H, W} from './tl';

// Rótulo de sección: barra dorada que se estira y texto que sube por máscara
export const SectionLabel: React.FC<{n: string; title: string; at?: number; out?: number}> = ({n, title, at = 4, out = 1}) => {
  const f = useCurrentFrame();
  const bar = ease(f, at, at + 14);
  const txt = ease(f, at + 4, at + 20);
  return (
    <div style={{position: 'absolute', left: 64, top: 92, fontFamily: FONT, display: 'flex', alignItems: 'center', gap: 16, opacity: out}}>
      <div style={{width: 48 * bar, height: 3, background: C.gold}} />
      <div style={{overflow: 'hidden', height: 28}}>
        <div style={{transform: `translateY(${(1 - txt) * 28}px)`, color: C.white, fontSize: 19, fontWeight: 700, letterSpacing: 5, textTransform: 'uppercase'}}>
          <span style={{color: C.gold}}>{n}</span>
          <span style={{opacity: 0.85}}> — {title}</span>
        </div>
      </div>
    </div>
  );
};

// Nota de fuente al pie: obligatoria en cada escena con contenido normativo
export const Source: React.FC<{text: string; at?: number; out?: number}> = ({text, at = 10, out = 1}) => {
  const f = useCurrentFrame();
  const o = ease(f, at, at + 14);
  return (
    <div style={{position: 'absolute', left: 64, top: 958, fontFamily: FONT, color: C.mute, fontSize: 15, fontWeight: 600, letterSpacing: 1, opacity: o * out * 0.9}}>
      {text}
    </div>
  );
};

// Palabras que llegan una a una por máscara, cada una en su fotograma
export const Words: React.FC<{
  words: {t: string; at: number; color?: string}[];
  size: number;
  weight?: number;
  align?: 'left' | 'center';
  width?: number;
  lh?: number;
}> = ({words, size, weight = 900, align = 'left', width = 952, lh = 1.12}) => {
  const f = useCurrentFrame();
  return (
    <div style={{width, display: 'flex', flexWrap: 'wrap', justifyContent: align === 'center' ? 'center' : 'flex-start', columnGap: size * 0.26, fontFamily: FONT}}>
      {words.map((w, i) => {
        const p = sp(f, w.at, {damping: 16, stiffness: 170});
        return (
          <div key={i} style={{overflow: 'hidden', height: size * lh, lineHeight: `${size * lh}px`}}>
            <div style={{transform: `translateY(${(1 - p) * size * 1.1}px)`, fontSize: size, fontWeight: weight, color: w.color ?? C.white, whiteSpace: 'nowrap'}}>{w.t}</div>
          </div>
        );
      })}
    </div>
  );
};

// Número gigante que cae con golpe: escala 3→1, sacudida y onda expansiva
export const Slam: React.FC<{text: string; at: number; size: number; x?: number; y: number; outline?: boolean}> = ({text, at, size, x = W / 2, y, outline}) => {
  const f = useCurrentFrame();
  const p = sp(f, at - 5, {damping: 12, stiffness: 260, mass: 0.6});
  const lag = sp(f, at, {damping: 20, stiffness: 90});
  const sh = shake(f, at, 16, 14);
  if (f < at - 5) return null;
  return (
    <>
      <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0, pointerEvents: 'none'}}>
        {[0, 7].map((d) => {
          const k = ease(f, at + d, at + d + 28);
          return k > 0 && k < 1 ? <circle key={d} cx={x} cy={y} r={size * 0.45 + k * 700} fill="none" stroke={C.gold} strokeWidth={8 * (1 - k)} opacity={1 - k} /> : null;
        })}
      </svg>
      {outline && (
        <div style={{position: 'absolute', left: x - 600, top: y - size * 0.6, width: 1200, textAlign: 'center', fontFamily: FONT, fontSize: size, fontWeight: 900, lineHeight: `${size * 1.2}px`, color: 'transparent', WebkitTextStroke: `2px ${C.gold}`, opacity: 0.5, transform: `translate(${18 + sh.x}px, ${14 + sh.y}px) scale(${1.15 - 0.15 * lag})`}}>
          {text}
        </div>
      )}
      <div
        style={{
          position: 'absolute',
          left: x - 600,
          top: y - size * 0.6,
          width: 1200,
          textAlign: 'center',
          fontFamily: FONT,
          fontSize: size,
          fontWeight: 900,
          lineHeight: `${size * 1.2}px`,
          backgroundImage: gold,
          WebkitBackgroundClip: 'text',
          color: 'transparent',
          transform: `translate(${sh.x}px, ${sh.y}px) scale(${3 - 2 * p})`,
          opacity: Math.min(1, p * 2),
        }}
      >
        {text}
      </div>
    </>
  );
};

// Sello que cae girado con muelle rígido
export const Stamp: React.FC<{text: string; at: number; color?: string; rot?: number; size?: number; style?: React.CSSProperties}> = ({text, at, color = C.coral, rot = -8, size = 30, style}) => {
  const f = useCurrentFrame();
  const p = sp(f, at - 5, {damping: 10, stiffness: 320, mass: 0.7});
  if (f < at - 5) return null;
  return (
    <div style={{position: 'absolute', padding: `${size * 0.3}px ${size * 0.6}px`, border: `${Math.max(3, size / 8)}px solid ${color}`, borderRadius: 10, color, fontFamily: FONT, fontSize: size, fontWeight: 900, letterSpacing: size * 0.12, whiteSpace: 'nowrap', transform: `rotate(${rot}deg) scale(${3 - 2 * p})`, opacity: Math.min(1, p * 2), ...style}}>
      {text}
    </div>
  );
};

const pad = (n: number) => String(n).padStart(2, '0');

// Capa de sala de edición: esquinas, timecode, punto REC y firma
export const EditorHud: React.FC<{offset?: number}> = ({offset = 0}) => {
  const f = useCurrentFrame() + offset;
  const s = Math.floor(f / FPS);
  const tc = `00:${pad(Math.floor(s / 60))}:${pad(s % 60)}:${pad(f % FPS)}`;
  const on = ease(f - offset, 6, 24);
  const corner = (r: number, x: number, y: number) => (
    <div key={r} style={{position: 'absolute', left: x, top: y, width: 36, height: 36, borderTop: `2px solid ${C.mute}`, borderLeft: `2px solid ${C.mute}`, transform: `rotate(${r}deg)`, opacity: 0.45 * on}} />
  );
  const chrome: React.CSSProperties = {position: 'absolute', bottom: 46, color: C.mute, fontSize: 15, fontWeight: 600, letterSpacing: 3, opacity: 0.8 * on, fontFamily: FONT};
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {corner(0, 36, 36)}
      {corner(90, W - 72, 36)}
      {corner(180, W - 72, H - 72)}
      {corner(270, 36, H - 72)}
      <div style={{...chrome, left: 64, fontVariantNumeric: 'tabular-nums'}}>TC {tc}</div>
      <div style={{...chrome, right: 64, display: 'flex', alignItems: 'center', gap: 10}}>
        <div style={{width: 10, height: 10, borderRadius: 5, background: C.coral, opacity: Math.floor(f / 15) % 2 ? 0.35 : 1}} />
        J. A. SERRANO · AML · GRC
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

export const Flash: React.FC<{at: number; color?: string; max?: number}> = ({at, color = C.white, max = 0.6}) => {
  const f = useCurrentFrame();
  const o = f < at ? ease(f, at - 2, at, [0, max]) : ease(f, at, at + 6, [max, 0]);
  if (o <= 0) return null;
  return <AbsoluteFill style={{background: color, opacity: o, pointerEvents: 'none'}} />;
};

// Salida estándar de escena: empuje y desenfoque en los últimos fotogramas
export const useExit = (len: number, n = 12) => {
  const f = useCurrentFrame();
  return ease(f, len - n, len, [0, 1], IN);
};
