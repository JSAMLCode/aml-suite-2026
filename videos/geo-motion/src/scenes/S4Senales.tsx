import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {evolvePath} from '@remotion/paths';
import {C, FONT, INOUT, ease, sp} from '../theme';
import {SectionLabel, Source, useExit} from '../ui';
import {span, wf} from '../tl';

const ID = '04';
const LEN = span(ID).len;
const CX = 540;
const CY = 590;
const RX = 330;
const RY = 290;
const R = 132;

// Las ocho señales del art. 14, en el orden en que se nombran.
// Coral: señales de ocultación (VPN, proxies, anonimización).
const SIG = [
  {t: 'Dirección IP', word: 'dirección', a: -150},
  {t: 'Tipo de red', word: 'tipo', a: 180},
  {t: 'Proveedor de internet', word: 'proveedor', a: 145},
  {t: 'VPN', word: 'vpn', a: -30, hide: true},
  {t: 'Proxies', word: 'proxies', a: 0, hide: true},
  {t: 'Redes de anonimización', word: 'redes', a: 35, hide: true},
  {t: 'Zona horaria', word: 'zona', a: 90},
  {t: 'Configuración regional', word: 'configuración', a: -90},
];

const Globe: React.FC<{f: number; s: number; pulse: number}> = ({f, s, pulse}) => {
  const rot = f * 0.03;
  return (
    <svg width="1080" height="1080" style={{position: 'absolute'}}>
      <defs>
        <radialGradient id="gl" cx="0.38" cy="0.32" r="0.8">
          <stop offset="0" stopColor={C.deep} />
          <stop offset="1" stopColor={C.navy2} />
        </radialGradient>
        <clipPath id="gc">
          <circle cx={CX} cy={CY} r={R * s} />
        </clipPath>
      </defs>
      <circle cx={CX} cy={CY} r={R * s + 30 * pulse} fill="none" stroke={C.gold} strokeWidth={6 * (1 - pulse)} opacity={pulse > 0 ? 1 - pulse : 0} />
      <circle cx={CX} cy={CY} r={R * s} fill="url(#gl)" stroke={C.gold} strokeWidth={3} />
      <g clipPath="url(#gc)" stroke={C.mute} strokeOpacity={0.45} fill="none" strokeWidth={1.5}>
        {Array.from({length: 6}).map((_, i) => {
          const ph = rot + (i * Math.PI) / 6;
          return <ellipse key={i} cx={CX} cy={CY} rx={Math.abs(Math.cos(ph)) * R * s} ry={R * s} />;
        })}
        {[-0.66, -0.33, 0, 0.33, 0.66].map((k) => (
          <ellipse key={k} cx={CX} cy={CY + k * R * s} rx={Math.sqrt(1 - k * k) * R * s} ry={6 * s} />
        ))}
      </g>
    </svg>
  );
};

export const S4Senales: React.FC = () => {
  const f = useCurrentFrame();
  const exit = useExit(LEN);
  const globe = sp(f, 0, {damping: 14, stiffness: 120});
  const times = SIG.map((s) => wf(ID, s.word));
  const count = times.filter((t) => f >= t).length;
  const resolve = wf(ID, 'dispositivo') + 6;
  const pulse = f >= resolve ? ease(f, resolve, resolve + 24) : 0;
  const chip = sp(f, resolve, {damping: 14, stiffness: 180});

  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: FONT}}>
      <AbsoluteFill style={{opacity: 1 - exit, transform: `scale(${1 + exit * 0.12})`, filter: `blur(${exit * 10}px)`}}>
        {/* conectores */}
        <svg width="1080" height="1080" style={{position: 'absolute'}}>
          {SIG.map((s, i) => {
            const a = (s.a * Math.PI) / 180;
            const x = CX + Math.cos(a) * RX;
            const y = CY + Math.sin(a) * RY;
            const d = `M ${CX + Math.cos(a) * R} ${CY + Math.sin(a) * R} L ${x} ${y}`;
            const p = ease(f, times[i], times[i] + 10, [0, 1], INOUT);
            const ev = evolvePath(p, d);
            // paquete que viaja hacia el globo al resolver
            const q = ease(f, resolve - 14 + i, resolve - 2 + i, [0, 1], INOUT);
            return (
              <g key={i}>
                <path d={d} stroke={s.hide ? C.coral : C.gold} strokeOpacity={0.7} strokeWidth={2.5} strokeDasharray={ev.strokeDasharray} strokeDashoffset={ev.strokeDashoffset} fill="none" />
                {q > 0 && q < 1 && <circle cx={x + (CX + Math.cos(a) * R - x) * q} cy={y + (CY + Math.sin(a) * R - y) * q} r={7} fill={C.goldL} />}
              </g>
            );
          })}
        </svg>

        <Globe f={f} s={globe} pulse={pulse} />

        {SIG.map((s, i) => {
          const a = (s.a * Math.PI) / 180;
          const x = CX + Math.cos(a) * RX;
          const y = CY + Math.sin(a) * RY;
          const p = sp(f, times[i] + 4, {damping: 13, stiffness: 190});
          if (f < times[i] + 4) return null;
          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: x - 115,
                top: y - 36,
                width: 230,
                minHeight: 72,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                textAlign: 'center',
                padding: '8px 14px',
                boxSizing: 'border-box',
                borderRadius: 14,
                background: C.navy2,
                border: `2px solid ${s.hide ? C.coral : C.gold}`,
                color: C.white,
                fontSize: 22,
                fontWeight: 800,
                lineHeight: 1.15,
                transform: `translate(${(CX - x) * (1 - p)}px, ${(CY - y) * (1 - p)}px) scale(${p})`,
                boxShadow: '0 12px 30px rgba(0,0,0,0.35)',
              }}
            >
              {s.t}
            </div>
          );
        })}

        {/* contador de señales */}
        <div style={{position: 'absolute', right: 64, top: 160, textAlign: 'right'}}>
          <div style={{color: C.goldL, fontSize: 84, fontWeight: 900, lineHeight: 1, fontVariantNumeric: 'tabular-nums'}}>
            {count}
            <span style={{color: C.mute, fontSize: 40}}> / 8</span>
          </div>
          <div style={{color: C.mute, fontSize: 16, fontWeight: 700, letterSpacing: 4, marginTop: 6}}>SEÑALES</div>
        </div>

        <div style={{position: 'absolute', left: CX - 150, top: CY - 22, width: 300, display: 'flex', justifyContent: 'center', opacity: chip, transform: `scale(${chip})`}}>
          <div style={{padding: '10px 18px', borderRadius: 10, background: C.gold, color: C.navy, fontSize: 18, fontWeight: 900, letterSpacing: 2, whiteSpace: 'nowrap'}}>UBICACIÓN ESTIMADA</div>
        </div>
      </AbsoluteFill>
      <SectionLabel n="03" title="Las señales" out={1 - exit} />
      <Source text="Fuente: Acuerdo 1-2026 SBP, art. 14" out={1 - exit} />
    </AbsoluteFill>
  );
};
