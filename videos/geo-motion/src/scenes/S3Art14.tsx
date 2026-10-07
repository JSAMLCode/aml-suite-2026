import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {noise3D} from '@remotion/noise';
import {C, FONT, INOUT, ease, sp} from '../theme';
import {SectionLabel, Slam, Source, Stamp, Words, useExit} from '../ui';
import {span, wf} from '../tl';

const ID = '03';
const LEN = span(ID).len;

const PANEL = {x: 64, y: 330, w: 952, h: 560};
const COLS = 19;
const ROWS = 11;
const PINS = [
  {label: 'SOLICITANTE', x: 360, y: 600, word: 'solicitante', r: 120},
  {label: 'DISPOSITIVO', x: 720, y: 650, word: 'dispositivo', r: 95},
];

export const S3Art14: React.FC = () => {
  const f = useCurrentFrame();
  const exit = useExit(LEN);
  const n14 = wf(ID, 'catorce');
  const primaria = wf(ID, 'primaria');
  const estimar = wf(ID, 'estimar');
  const sin = wf(ID, 'sin');
  const coord = wf(ID, 'coordenadas');

  const park = ease(f, estimar - 16, estimar + 2, [0, 1], INOUT);
  const panel = sp(f, estimar - 6, {damping: 20, stiffness: 110});
  const pinT = PINS.map((p) => wf(ID, p.word));

  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: FONT}}>
      <AbsoluteFill style={{opacity: 1 - exit, filter: `blur(${exit * 10}px)`}}>
        {/* ART. 14 con golpe; se aparca arriba a la derecha */}
        <div style={{position: 'absolute', inset: 0, transformOrigin: '1068px 68px', transform: `scale(${1 - park * 0.72})`}}>
          <div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', color: C.mute, fontSize: 34, fontWeight: 800, letterSpacing: 14, opacity: ease(f, 6, 16) * (1 - park)}}>ARTÍCULO</div>
          <Slam text="14" at={n14} size={330} y={540} outline />
        </div>
        <div style={{opacity: 1 - park}}>
          <Stamp text="FUENTE PRIMARIA DE RIESGO" at={primaria} color={C.gold} rot={-6} size={30} style={{left: 250, top: 790}} />
        </div>

        {/* titular de la definición */}
        <div style={{position: 'absolute', left: 64, top: 190}}>
          <Words
            size={58}
            words={[
              {t: 'Estimar', at: estimar, color: C.gold},
              {t: 'la', at: estimar + 3},
              {t: 'ubicación', at: wf(ID, 'ubicación')},
              {t: 'sin', at: sin},
              {t: 'coordenadas', at: coord},
              {t: 'directas', at: coord + 4},
            ]}
          />
        </div>

        {/* mapa de puntos con dos estimaciones */}
        <div style={{position: 'absolute', left: PANEL.x, top: PANEL.y, width: PANEL.w, height: PANEL.h, borderRadius: 18, border: `2px solid ${C.mute}33`, background: 'rgba(255,255,255,0.03)', opacity: panel, transform: `translateY(${(1 - panel) * 80}px)`}} />
        <svg width="1080" height="1080" style={{position: 'absolute', opacity: panel}}>
          {Array.from({length: COLS * ROWS}).map((_, k) => {
            const c = k % COLS;
            const r = Math.floor(k / COLS);
            const x = PANEL.x + 46 + c * ((PANEL.w - 92) / (COLS - 1));
            const y = PANEL.y + 46 + r * ((PANEL.h - 92) / (ROWS - 1));
            const n = (noise3D('m', c * 0.15, r * 0.15, f * 0.02) + 1) / 2;
            let bump = 0;
            PINS.forEach((p, i) => {
              const age = f - pinT[i];
              if (age < 0 || age > 45) return;
              const d = Math.hypot(x - p.x, y - p.y);
              bump += Math.exp(-(((d - age * 14) / 40) ** 2)) * (1 - age / 45);
            });
            return <circle key={k} cx={x} cy={y} r={1.6 + n * 1.8 + bump * 4} fill={bump > 0.15 ? C.goldL : C.mute} opacity={0.25 + n * 0.25 + bump * 0.5} />;
          })}
          {PINS.map((p, i) => {
            const s = sp(f, pinT[i] - 4, {damping: 11, stiffness: 200});
            if (f < pinT[i] - 4) return null;
            const breathe = 1 + 0.05 * Math.sin((f - pinT[i]) / 9);
            return (
              <g key={i}>
                {/* círculo de incertidumbre: es una estimación, no un punto */}
                <circle cx={p.x} cy={p.y} r={p.r * s * breathe} fill={C.gold} fillOpacity={0.08} stroke={C.gold} strokeOpacity={0.7} strokeWidth={2} strokeDasharray="6 8" transform={`rotate(${f * 0.6} ${p.x} ${p.y})`} />
                <circle cx={p.x} cy={p.y} r={11 * s} fill={C.goldL} />
                <circle cx={p.x} cy={p.y} r={22 * s} fill="none" stroke={C.goldL} strokeWidth={3} opacity={0.6} />
              </g>
            );
          })}
        </svg>
        {PINS.map((p, i) => {
          const t = ease(f, pinT[i] + 4, pinT[i] + 16);
          return (
            <div key={i} style={{position: 'absolute', left: p.x - 120, top: p.y + p.r + 12, width: 240, textAlign: 'center', color: C.white, fontSize: 20, fontWeight: 800, letterSpacing: 4, opacity: t, transform: `translateY(${(1 - t) * 14}px)`}}>
              {p.label}
            </div>
          );
        })}

        {/* GPS tachado: sin coordenadas físicas directas */}
        {(() => {
          const a = sp(f, sin, {damping: 16, stiffness: 160});
          const strike = ease(f, coord, coord + 10);
          return (
            <div style={{position: 'absolute', right: 96, top: PANEL.y + 30, display: 'flex', alignItems: 'center', gap: 12, padding: '10px 18px', borderRadius: 12, border: `2px solid ${C.coral}`, color: C.coral, fontSize: 20, fontWeight: 900, letterSpacing: 3, opacity: a, transform: `scale(${0.6 + 0.4 * a})`}}>
              <svg width="28" height="28">
                <circle cx="14" cy="14" r="9" fill="none" stroke={C.coral} strokeWidth="3" />
                <line x1="14" y1="0" x2="14" y2="28" stroke={C.coral} strokeWidth="3" />
                <line x1="0" y1="14" x2="28" y2="14" stroke={C.coral} strokeWidth="3" />
                <line x1="2" y1="26" x2={2 + 24 * strike} y2={26 - 24 * strike} stroke={C.white} strokeWidth="4" />
              </svg>
              <span style={{position: 'relative'}}>
                COORDENADAS GPS
                <span style={{position: 'absolute', left: -4, top: 12, height: 4, width: 214 * strike, background: C.white}} />
              </span>
            </div>
          );
        })()}
      </AbsoluteFill>
      <SectionLabel n="02" title="Artículo 14" out={1 - exit} />
      <Source text="Fuente: Acuerdo 1-2026 SBP, art. 14" out={1 - exit} />
    </AbsoluteFill>
  );
};
