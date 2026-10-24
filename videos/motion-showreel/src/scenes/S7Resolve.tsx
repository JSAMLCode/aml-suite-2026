import React from 'react';
import {AbsoluteFill, random, useCurrentFrame} from 'remotion';
import {C, FONT, IN, INOUT, OUT, ease, gold, sp} from '../theme';

const N = 220;
const RING = 300;
const RX = 1.55; // anillo elíptico: deja aire al logotipo
const BURST = 62; // los puntos cierran el anillo y estalla el logotipo
const WORD = 'SELENE';

const P = Array.from({length: N}).map((_, i) => {
  const a = random(`a${i}`) * Math.PI * 2;
  const dist = 900 + random(`d${i}`) * 900;
  return {
    sx: 960 + Math.cos(a) * dist,
    sy: 540 + Math.sin(a) * dist * 0.7,
    ta: (i / N) * Math.PI * 2,
    delay: random(`t${i}`) * 26,
    size: 2 + random(`s${i}`) * 4,
    gold: random(`c${i}`) > 0.35,
  };
});

export const S7Resolve: React.FC = () => {
  const f = useCurrentFrame();
  const spin = f * 0.6 + ease(f, BURST - 6, BURST + 30, [0, 120], OUT);
  const ringR = RING + ease(f, BURST - 4, BURST + 20, [0, 40], OUT);
  const close = ease(f, 176, 204, [0, 1], IN); // el anillo colapsa al punto inicial
  const tracking = ease(f, BURST, BURST + 50, [56, 20], OUT);
  const shine = ease(f, BURST + 20, BURST + 70, [-40, 140], INOUT);
  const logo = sp(f, BURST, {damping: 14, stiffness: 120});
  const sub = ease(f, BURST + 26, BURST + 44);
  const tag = ease(f, BURST + 44, BURST + 62);
  const fadeText = 1 - ease(f, 170, 184);

  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: FONT}}>
      <AbsoluteFill style={{background: `radial-gradient(circle at 50% 50%, ${C.deep} 0%, transparent 55%)`, opacity: ease(f, BURST - 10, BURST + 20) * fadeText}} />

      <svg width="1920" height="1080" style={{position: 'absolute'}}>
        {P.map((p, i) => {
          const t = ease(f, p.delay, p.delay + 36, [0, 1], INOUT);
          const a = p.ta + (spin * Math.PI) / 180;
          const r = ringR * (1 - close) + (i % 3) * 6 * (1 - close);
          const tx = 960 + Math.cos(a) * r * RX;
          const ty = 540 + Math.sin(a) * r;
          const x = p.sx + (tx - p.sx) * t;
          const y = p.sy + (ty - p.sy) * t;
          // estela: segmento hacia atrás proporcional a la velocidad
          const tPrev = ease(f - 2, p.delay, p.delay + 36, [0, 1], INOUT);
          const px = p.sx + (tx - p.sx) * tPrev;
          const py = p.sy + (ty - p.sy) * tPrev;
          return (
            <g key={i} opacity={1 - ease(f, 196, 206)}>
              <line x1={px} y1={py} x2={x} y2={y} stroke={p.gold ? C.gold : C.mute} strokeWidth={p.size} strokeLinecap="round" opacity={0.6} />
              <circle cx={x} cy={y} r={p.size * (1 - close * 0.5)} fill={p.gold ? C.goldL : C.white} />
            </g>
          );
        })}
        {/* destello del cierre del anillo */}
        {f >= BURST - 2 && (
          <ellipse cx="960" cy="540" rx={(RING + ease(f, BURST - 2, BURST + 24) * 700) * RX} ry={RING + ease(f, BURST - 2, BURST + 24) * 700} fill="none" stroke={C.goldL} strokeWidth={14 * (1 - ease(f, BURST - 2, BURST + 24))} opacity={1 - ease(f, BURST - 2, BURST + 24)} />
        )}
        {/* punto final: rima con la apertura */}
        <circle cx="960" cy="540" r={9 * ease(f, 198, 204) * (1 - ease(f, 206, 210))} fill={C.goldL} />
      </svg>

      {/* logotipo */}
      <div style={{position: 'absolute', top: 430, width: '100%', textAlign: 'center', opacity: fadeText}}>
        <div
          style={{
            display: 'inline-block',
            fontSize: 130,
            fontWeight: 900,
            letterSpacing: tracking,
            paddingLeft: tracking,
            backgroundImage: `linear-gradient(110deg, transparent ${shine - 12}%, rgba(255,255,255,0.95) ${shine}%, transparent ${shine + 12}%), ${gold}`,
            WebkitBackgroundClip: 'text',
            color: 'transparent',
            opacity: f < BURST ? 0 : 1,
            transform: `scale(${0.6 + 0.4 * logo})`,
            filter: `blur(${(1 - Math.min(1, logo)) * 16}px)`,
          }}
        >
          {WORD}
        </div>
        <div style={{marginTop: 4, color: C.white, fontSize: 26, fontWeight: 600, letterSpacing: 7, opacity: sub, transform: `translateY(${(1 - sub) * 24}px)`}}>
          SERRANO LAWYERS &amp; CONSULTANTS
        </div>
        <div style={{marginTop: 40, color: C.mute, fontSize: 19, fontWeight: 700, letterSpacing: 4, opacity: tag, transform: `translateY(${(1 - tag) * 20}px)`}}>
          MOTION GRAPHICS ESCRITOS EN CÓDIGO · REMOTION + REACT
        </div>
      </div>
    </AbsoluteFill>
  );
};
