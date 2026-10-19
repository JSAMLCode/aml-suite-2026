import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C, FONT, IN, OUT, ease, sp} from '../theme';
import {SectionLabel, Source} from '../ui';

const STEPS = [
  {n: '1', t: 'IDENTIFICAR', d: 'Cliente, estructura y beneficiario final'},
  {n: '2', t: 'VERIFICAR', d: 'Documentos y fuentes independientes'},
  {n: '3', t: 'PERFILAR', d: 'Producto, geografía, canal y actividad'},
  {n: '4', t: 'MONITOREAR', d: 'Transacciones y cambios de perfil'},
];

export const S3Flow: React.FC = () => {
  const f = useCurrentFrame();
  const exit = ease(f, 104, 120, [0, 1], IN);
  const top = 480;
  const gap = 290;
  const line = ease(f, 10, 90, [0, 1], OUT);
  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: FONT}}>
      <SectionLabel n="02" title="Ciclo de debida diligencia" />
      <AbsoluteFill style={{transform: `scale(${1 + exit * 0.4})`, opacity: 1 - exit, transformOrigin: '50% 70%'}}>
        <div style={{position: 'absolute', left: 176, top: top + 60, width: 4, height: gap * 3 * line, background: `linear-gradient(${C.gold}, ${C.goldD})`}} />
        {STEPS.map((s, i) => {
          const at = 12 + i * 18;
          const p = sp(f, at, {damping: 15, stiffness: 170});
          return (
            <div key={s.n} style={{position: 'absolute', left: 90, right: 90, top: top + i * gap, height: 240, opacity: Math.min(1, p * 1.5), transform: `translateX(${(1 - p) * 420}px)`}}>
              <div style={{position: 'absolute', left: 0, top: 0, width: 180, height: 180, borderRadius: 90, border: `4px solid ${C.gold}`, background: C.navy2, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 100, fontWeight: 900, color: C.goldL, boxShadow: `0 0 ${30 * p}px rgba(217,178,106,.35)`}}>{s.n}</div>
              <div style={{position: 'absolute', left: 230, top: 28, fontSize: 70, fontWeight: 900, letterSpacing: 4, color: C.white}}>{s.t}</div>
              <div style={{position: 'absolute', left: 230, top: 112, width: 700, fontSize: 32, fontWeight: 600, color: C.mute, lineHeight: 1.25}}>{s.d}</div>
            </div>
          );
        })}
      </AbsoluteFill>
      <Source text="ESQUEMA ILUSTRATIVO · APLICAR SEGÚN NORMA DEL SUPERVISOR COMPETENTE" />
    </AbsoluteFill>
  );
};
