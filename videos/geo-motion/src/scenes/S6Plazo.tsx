import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C, FONT, INOUT, ease, sp} from '../theme';
import {SectionLabel, Slam, Source, useExit} from '../ui';
import {span, wf} from '../tl';

const ID = '06';
const LEN = span(ID).len;

const X0 = 90;
const X1 = 990;
const AXIS = 400;
const MONTHS = ['OCT', 'NOV', 'DIC', 'ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN'];
// Frentes de trabajo: posiciones ilustrativas, no a escala
const BARS = [
  {t: 'Construir o comprar', word: 'decidir', a: 0, b: 0.34},
  {t: 'Integrar con la plataforma', word: 'integrar', a: 0.24, b: 0.66},
  {t: 'Calibrar', word: 'calibrar', a: 0.56, b: 0.84},
  {t: 'Documentar en el manual', word: 'documentar', a: 0.62, b: 1},
];

export const S6Plazo: React.FC = () => {
  const f = useCurrentFrame();
  const exit = useExit(LEN);
  const nueve = wf(ID, 'nueve');
  const pero = wf(ID, 'pero');
  const park = ease(f, pero - 10, pero + 6, [0, 1], INOUT);
  const axis = ease(f, pero - 4, pero + 18, [0, 1], INOUT);
  // cursor "hoy" que avanza: el tiempo corre mientras se enumeran los frentes
  const today = ease(f, pero, LEN, [0, 0.18]);
  const xOf = (k: number) => X0 + k * (X1 - X0);

  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: FONT}}>
      <AbsoluteFill style={{opacity: 1 - exit, filter: `blur(${exit * 10}px)`}}>
        {/* 9 meses: golpe y se aparca como titular */}
        <div style={{position: 'absolute', inset: 0, transformOrigin: '64px 150px', transform: `scale(${1 - park * 0.66})`}}>
          <Slam text="9" at={nueve} size={360} x={330} y={520} outline />
          <div style={{position: 'absolute', left: 480, top: 430, color: C.white, fontSize: 110, fontWeight: 900, lineHeight: 1, opacity: ease(f, wf(ID, 'meses'), wf(ID, 'meses') + 8)}}>
            MESES
          </div>
        </div>
        <div style={{position: 'absolute', left: 352, top: 250, color: C.mute, fontSize: 30, fontWeight: 700, opacity: ease(f, pero + 4, pero + 16)}}>
          cuatro frentes de trabajo
        </div>

        {/* eje temporal */}
        <svg width="1080" height="1080" style={{position: 'absolute'}}>
          <line x1={X0} x2={X0 + (X1 - X0) * axis} y1={AXIS} y2={AXIS} stroke={C.mute} strokeOpacity={0.5} strokeWidth={2} />
          {MONTHS.map((m, i) => {
            const x = xOf(i / (MONTHS.length - 1));
            const o = ease(f, pero + i * 2, pero + 8 + i * 2);
            return (
              <g key={m} opacity={o}>
                <line x1={x} x2={x} y1={AXIS - 8} y2={AXIS + 8} stroke={C.mute} strokeWidth={2} />
                <text x={x} y={AXIS - 22} fill={C.mute} fontSize={16} fontWeight={700} textAnchor="middle" fontFamily="Nunito Sans" letterSpacing={2}>
                  {m}
                </text>
              </g>
            );
          })}
          {/* fecha límite */}
          <line x1={X1} x2={X1} y1={AXIS - 60} y2={AXIS - 60 + 520 * axis} stroke={C.coral} strokeWidth={4} />
          {/* hoy */}
          <line x1={xOf(today)} x2={xOf(today)} y1={AXIS - 14} y2={AXIS + 460 * axis} stroke={C.goldL} strokeWidth={2} strokeDasharray="6 8" opacity={axis} />
        </svg>
        <div style={{position: 'absolute', left: X1 - 160, top: AXIS - 100, width: 160, textAlign: 'right', color: C.coral, fontSize: 20, fontWeight: 900, letterSpacing: 2, opacity: axis}}>30·06·2027</div>
        <div style={{position: 'absolute', left: xOf(today) - 40, top: AXIS + 462 * axis, width: 80, textAlign: 'center', color: C.goldL, fontSize: 15, fontWeight: 800, letterSpacing: 3, opacity: axis}}>HOY</div>

        {BARS.map((b, i) => {
          const at = wf(ID, b.word);
          const p = sp(f, at, {damping: 18, stiffness: 150});
          const y = AXIS + 46 + i * 100;
          return (
            <div key={i} style={{position: 'absolute', left: xOf(b.a), top: y, width: (xOf(b.b) - xOf(b.a)) * p, height: 66, borderRadius: 10, background: i === 3 ? C.gold : C.deep, border: `2px solid ${C.gold}`, overflow: 'hidden', opacity: f >= at ? 1 : 0}}>
              <div style={{padding: '0 18px', lineHeight: '62px', whiteSpace: 'nowrap', color: i === 3 ? C.navy : C.white, fontSize: 22, fontWeight: 800}}>{b.t}</div>
            </div>
          );
        })}
      </AbsoluteFill>
      <SectionLabel n="05" title="Nueve meses" out={1 - exit} />
      <Source text="Esquema ilustrativo, duraciones no a escala · Fuente: Acuerdo 1-2026 SBP, art. 53" out={1 - exit} />
    </AbsoluteFill>
  );
};
