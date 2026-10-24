import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {evolvePath, getPointAtLength} from '@remotion/paths';
import {C, FONT, INOUT, ease, sp} from '../theme';
import {SectionLabel, Slam, Source, useExit} from '../ui';
import {span, wf} from '../tl';

const ID = '05';
const LEN = span(ID).len;

const NODE = {x: 330, y: 560};
const OK = {x: 610, y: 330, w: 410, h: 150};
const NO = {x: 610, y: 560, w: 410, h: 330};
const P_IN = `M 200 ${NODE.y} L ${NODE.x - 100} ${NODE.y}`;
const P_OK = `M ${NODE.x + 100} ${NODE.y} C 540 ${NODE.y} 520 ${OK.y + OK.h / 2} ${OK.x} ${OK.y + OK.h / 2}`;
const P_NO = `M ${NODE.x + 100} ${NODE.y} C 540 ${NODE.y} 520 ${NO.y + 60} ${NO.x} ${NO.y + 60}`;

const Path: React.FC<{d: string; p: number; color: string}> = ({d, p, color}) => {
  const ev = evolvePath(p, d);
  return <path d={d} fill="none" stroke={color} strokeWidth={4} strokeLinecap="round" strokeDasharray={ev.strokeDasharray} strokeDashoffset={ev.strokeDashoffset} />;
};

export const S5Controles: React.FC = () => {
  const f = useCurrentFrame();
  const exit = useExit(LEN);
  const dos = wf(ID, 'dos');
  const verif = wf(ID, 'verificar');
  const cliente = wf(ID, 'cliente');
  const frenar = wf(ID, 'frenar');
  const items = [
    {t: 'Jurisdicción de alto riesgo', at: wf(ID, 'alto')},
    {t: 'Jurisdicción sancionada', at: wf(ID, 'sancionadas')},
    {t: 'No cuadra con lo declarado', at: wf(ID, 'cuadran')},
  ];

  const flow = sp(f, dos + 10, {damping: 18, stiffness: 120});
  const pIn = ease(f, dos + 8, dos + 22, [0, 1], INOUT);
  const pOk = ease(f, verif - 4, verif + 10, [0, 1], INOUT);
  const pNo = ease(f, frenar - 4, frenar + 10, [0, 1], INOUT);
  const okCard = sp(f, verif + 4, {damping: 14, stiffness: 170});
  const noCard = sp(f, frenar + 4, {damping: 14, stiffness: 170});
  const check = ease(f, cliente, cliente + 10);
  // paquete que recorre la rama de bloqueo y se detiene en seco
  const pkt = ease(f, frenar + 4, frenar + 22, [0, 1], INOUT);
  const head = getPointAtLength(P_NO, pkt * 330) ?? {x: 0, y: 0};

  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: FONT}}>
      <AbsoluteFill style={{opacity: 1 - exit, filter: `blur(${exit * 10}px)`}}>
        {/* "2 controles" */}
        <div style={{position: 'absolute', inset: 0, transformOrigin: '64px 150px', transform: `scale(${1 - ease(f, dos + 6, dos + 20, [0, 1], INOUT) * 0.62})`}}>
          <Slam text="2" at={dos} size={300} x={190} y={300} />
        </div>
        <div style={{position: 'absolute', left: 150, top: 168, color: C.white, fontSize: 52, fontWeight: 900, opacity: ease(f, dos + 14, dos + 24), transform: `translateX(${(1 - ease(f, dos + 14, dos + 24)) * -30}px)`}}>
          controles
        </div>

        <svg width="1080" height="1080" style={{position: 'absolute'}}>
          <Path d={P_IN} p={pIn} color={C.mute} />
          <Path d={P_OK} p={pOk} color={C.teal} />
          <Path d={P_NO} p={pNo} color={C.coral} />
          {pkt > 0 && pkt < 1 && <circle cx={head.x} cy={head.y} r={9} fill={C.coral} />}
        </svg>

        {/* origen y nodo */}
        <div style={{position: 'absolute', left: 40, top: NODE.y - 50, width: 160, height: 100, borderRadius: 14, border: `2px solid ${C.mute}55`, background: 'rgba(255,255,255,0.04)', color: C.white, fontSize: 19, fontWeight: 800, display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', opacity: flow, transform: `translateX(${(1 - flow) * -80}px)`}}>
          Solicitud de apertura
        </div>
        <div style={{position: 'absolute', left: NODE.x - 100, top: NODE.y - 70, width: 200, height: 140, borderRadius: 18, background: C.gold, color: C.navy, fontSize: 24, fontWeight: 900, display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', lineHeight: 1.15, transform: `scale(${flow})`, boxShadow: `0 0 50px ${C.gold}55`}}>
          Ubicación estimada
        </div>

        {/* control 1: validar */}
        <div style={{position: 'absolute', left: OK.x, top: OK.y, width: OK.w, height: OK.h, borderRadius: 16, border: `2px solid ${C.teal}`, background: C.navy2, padding: 24, boxSizing: 'border-box', transform: `scale(${okCard})`, transformOrigin: 'left center'}}>
          <div style={{display: 'flex', alignItems: 'center', gap: 14, color: C.teal, fontSize: 30, fontWeight: 900, letterSpacing: 2}}>
            <svg width="34" height="34">
              <circle cx="17" cy="17" r="15" fill="none" stroke={C.teal} strokeWidth="3" />
              <path d="M 9 17 L 15 23 L 26 11" fill="none" stroke={C.teal} strokeWidth="4" strokeLinecap="round" strokeDasharray="30" strokeDashoffset={30 * (1 - check)} />
            </svg>
            VALIDAR
          </div>
          <div style={{color: C.white, fontSize: 22, fontWeight: 600, marginTop: 14}}>Domicilio declarado por el cliente</div>
        </div>

        {/* control 2: frenar */}
        <div style={{position: 'absolute', left: NO.x, top: NO.y, width: NO.w, height: NO.h, borderRadius: 16, border: `2px solid ${C.coral}`, background: C.navy2, padding: 24, boxSizing: 'border-box', transform: `scale(${noCard})`, transformOrigin: 'left top'}}>
          <div style={{display: 'flex', alignItems: 'center', gap: 14, color: C.coral, fontSize: 30, fontWeight: 900, letterSpacing: 2}}>
            <svg width="34" height="34">
              <circle cx="17" cy="17" r="15" fill="none" stroke={C.coral} strokeWidth="3" />
              <path d="M 11 11 L 23 23 M 23 11 L 11 23" stroke={C.coral} strokeWidth="4" strokeLinecap="round" />
            </svg>
            FRENAR APERTURA
          </div>
          {items.map((it, i) => {
            const p = sp(f, it.at, {damping: 15, stiffness: 180});
            return (
              <div key={i} style={{display: 'flex', alignItems: 'center', gap: 12, marginTop: i === 0 ? 26 : 18, opacity: Math.min(1, p * 1.5), transform: `translateX(${(1 - p) * 60}px)`}}>
                <div style={{width: 10, height: 10, borderRadius: 5, background: C.coral, flexShrink: 0}} />
                <div style={{color: C.white, fontSize: 22, fontWeight: 700}}>{it.t}</div>
              </div>
            );
          })}
        </div>
      </AbsoluteFill>
      <SectionLabel n="04" title="Para qué sirve" out={1 - exit} />
      <Source text="Fuente: Acuerdo 1-2026 SBP, arts. 14 y 53" out={1 - exit} />
    </AbsoluteFill>
  );
};
