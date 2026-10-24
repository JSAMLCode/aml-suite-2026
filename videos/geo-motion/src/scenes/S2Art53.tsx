import React from 'react';
import {AbsoluteFill, interpolateColors, useCurrentFrame} from 'remotion';
import {C, FONT, IN, INOUT, ease, shake, sp} from '../theme';
import {SectionLabel, Slam, Source, useExit} from '../ui';
import {span, wf} from '../tl';

const ID = '02';
const LEN = span(ID).len;

// Rejilla de palabras apiladas en máscara, como en tipografía cinética
const Line: React.FC<{t: string; at: number; out: number; dir: number; color?: string; size?: number}> = ({t, at, out, dir, color = C.white, size = 112}) => {
  const f = useCurrentFrame();
  const p = sp(f, at, {damping: 18, stiffness: 140});
  const o = ease(f, out, out + 12, [0, 1], IN);
  return (
    <div style={{position: 'relative', height: size * 1.08, overflow: 'hidden', width: 1080}}>
      <div style={{position: 'absolute', inset: 0, textAlign: 'center', fontSize: size, fontWeight: 900, lineHeight: `${size * 1.08}px`, color, transform: `translateX(${(1 - p) * dir * 1100}px) translateY(${-o * size * 1.1}px) skewX(${(1 - p) * dir * -14}deg)`}}>
        {t}
      </div>
    </div>
  );
};

export const S2Art53: React.FC = () => {
  const f = useCurrentFrame();
  const exit = useExit(LEN);
  const art = wf(ID, 'artículo');
  const n53 = wf(ID, 'cincuenta');
  const bancos = wf(ID, 'bancos');
  const digital = wf(ID, 'digitales');
  const remotos = wf(ID, 'remotos');
  const geo = wf(ID, 'geolocalización');
  const ya = wf(ID, 'ya');
  const opc = wf(ID, 'opcional');

  // El 53 se retira a la esquina cuando entra el sujeto obligado
  const park = ease(f, bancos - 10, bancos + 8, [0, 1], INOUT);
  const flip = sp(f, ya, {damping: 13, stiffness: 220});
  const sh = shake(f, opc, 12, 12);
  const inverted = f >= opc && f < opc + 14;
  const toggleIn = sp(f, geo + 10, {damping: 18, stiffness: 120});

  return (
    <AbsoluteFill style={{background: inverted ? C.gold : C.navy, fontFamily: FONT}}>
      <AbsoluteFill style={{transform: `translate(${sh.x}px, ${sh.y}px)`, opacity: 1 - exit, filter: `blur(${exit * 10}px)`}}>
        {/* ART. 53: golpe y luego se aparca arriba a la derecha */}
        <div style={{position: 'absolute', inset: 0, transformOrigin: '1068px 68px', transform: `scale(${1 - park * 0.72})`}}>
          <div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', color: C.mute, fontSize: 34, fontWeight: 800, letterSpacing: 14, opacity: ease(f, art, art + 10) * (1 - park)}}>ARTÍCULO</div>
          <Slam text="53" at={n53} size={330} y={540} outline />
        </div>

        {/* sujeto y supuesto */}
        <div style={{position: 'absolute', top: 250, left: 0}}>
          <Line t="BANCOS CON" at={bancos} out={geo - 14} dir={-1} size={96} />
          <Line t="APERTURA" at={digital - 8} out={geo - 11} dir={1} color={C.gold} />
          <Line t="DIGITAL" at={digital} out={geo - 8} dir={-1} />
          <Line t="O REMOTA" at={remotos} out={geo - 5} dir={1} />
        </div>

        {/* obligación */}
        <div style={{position: 'absolute', top: 300, left: 0}}>
          <Line t="GEOLOCALIZACIÓN" at={geo} out={LEN} dir={-1} size={98} color={inverted ? C.navy : C.white} />
          <Line t="INFERENCIAL" at={geo + 8} out={LEN} dir={1} size={98} color={inverted ? C.navy : C.gold} />
        </div>

        {/* interruptor opcional → obligatorio */}
        <div style={{position: 'absolute', left: 140, top: 640, width: 800, height: 150, borderRadius: 24, border: `2px solid ${inverted ? C.navy : C.mute}55`, background: inverted ? 'transparent' : 'rgba(255,255,255,0.04)', transform: `translateY(${(1 - toggleIn) * 300}px)`, opacity: toggleIn, display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 48px', boxSizing: 'border-box'}}>
          <div style={{position: 'relative', fontSize: 40, fontWeight: 800, color: inverted ? C.navy : interpolateColors(flip, [0, 1], [C.white, C.mute])}}>
            Opcional
            <div style={{position: 'absolute', left: -6, top: 26, height: 5, width: 196 * ease(f, opc, opc + 8), background: C.coral}} />
          </div>
          <div style={{width: 150, height: 74, borderRadius: 37, background: interpolateColors(flip, [0, 1], ['#2A3558', inverted ? C.navy : C.gold]), position: 'relative'}}>
            <div style={{position: 'absolute', top: 7, left: 7 + flip * 76, width: 60, height: 60, borderRadius: 30, background: C.white, boxShadow: '0 4px 12px rgba(0,0,0,0.35)'}} />
          </div>
          <div style={{fontSize: 40, fontWeight: 900, color: inverted ? C.navy : interpolateColors(flip, [0, 1], [C.mute, C.goldL])}}>Obligatorio</div>
        </div>
      </AbsoluteFill>
      <SectionLabel n="01" title="Artículo 53" out={1 - exit} />
      <Source text="Fuente: Acuerdo 1-2026 SBP, art. 53" out={1 - exit} />
    </AbsoluteFill>
  );
};
