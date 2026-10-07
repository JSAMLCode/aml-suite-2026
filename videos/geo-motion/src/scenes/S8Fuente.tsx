import React from 'react';
import {AbsoluteFill, random, useCurrentFrame} from 'remotion';
import {C, FONT, IN, INOUT, OUT, ease, gold, sp} from '../theme';
import {Stamp, Words, useExit} from '../ui';
import {TL, span, wf} from '../tl';

const ID = '08';
const LEN = span(ID).len;

export const S8Fuente: React.FC = () => {
  const f = useCurrentFrame();
  const exit = useExit(LEN, 14);
  const bar = ease(f, 2, 16);
  const cta = ease(f, wf(ID, 'cincuenta') + 14, wf(ID, 'cincuenta') + 28);

  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: FONT}}>
      <AbsoluteFill style={{opacity: 1 - exit, transform: `scale(${1 - exit * 0.08})`, filter: `blur(${exit * 8}px)`}}>
        <div style={{position: 'absolute', left: 64, top: 250, display: 'flex', alignItems: 'center', gap: 16}}>
          <div style={{width: 56 * bar, height: 4, background: C.gold}} />
          <div style={{color: C.gold, fontSize: 24, fontWeight: 800, letterSpacing: 8, opacity: bar}}>FUENTE</div>
        </div>
        <div style={{position: 'absolute', left: 64, top: 300}}>
          <Words
            size={92}
            words={[
              {t: 'Acuerdo', at: wf(ID, 'acuerdo')},
              {t: '1-2026', at: wf(ID, 'uno'), color: C.goldL},
            ]}
          />
          <div style={{marginTop: 10}}>
            <Words size={40} weight={700} words={[{t: 'Superintendencia de Bancos de Panamá', at: wf(ID, 'sbp'), color: C.mute}]} />
          </div>
        </div>
        <Stamp text="ART. 14" at={wf(ID, 'catorce')} color={C.gold} rot={-4} size={44} style={{left: 64, top: 540}} />
        <Stamp text="ART. 53" at={wf(ID, 'cincuenta')} color={C.gold} rot={3} size={44} style={{left: 330, top: 540}} />

        <div style={{position: 'absolute', left: 64, top: 720, opacity: cta, transform: `translateY(${(1 - cta) * 20}px)`}}>
          <div style={{color: C.white, fontSize: 30, fontWeight: 800}}>¿Tecnología o Cumplimiento?</div>
          <div style={{color: C.mute, fontSize: 24, fontWeight: 600, marginTop: 8}}>Cuéntenos en los comentarios.</div>
          <div style={{color: C.teal, fontSize: 22, fontWeight: 800, marginTop: 14, letterSpacing: 1}}>#PBC #Cumplimiento #GeolocalizaciónInferencial</div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// Firma: partículas que convergen en un anillo elíptico y colapsan al punto inicial
const N = 200;
const RY = 300;
const RXK = 1.38;
const BURST = 42;
const P = Array.from({length: N}).map((_, i) => {
  const a = random(`a${i}`) * Math.PI * 2;
  const dist = 700 + random(`d${i}`) * 700;
  return {sx: 540 + Math.cos(a) * dist, sy: 540 + Math.sin(a) * dist, ta: (i / N) * Math.PI * 2, delay: random(`t${i}`) * 20, size: 1.6 + random(`s${i}`) * 3.4, gold: random(`c${i}`) > 0.35};
});
const CRED = ['CP/AML FIBA · ISO 37301 · 37001 · 37000 · 31000', 'AI COMPLIANCE EXPERT · LEGALTECH ARCHITECT', 'LEAN SIX SIGMA GREEN BELT · DOCENTE · SPEAKER'];

export const S9Firma: React.FC = () => {
  const f = useCurrentFrame();
  const len = TL.end - TL.sign;
  const spin = f * 0.5 + ease(f, BURST - 6, BURST + 30, [0, 110], OUT);
  const ry = RY + ease(f, BURST - 4, BURST + 20, [0, 24], OUT);
  const close = ease(f, len - 30, len - 8, [0, 1], IN);
  const tracking = ease(f, BURST, BURST + 46, [30, 6], OUT);
  const shine = ease(f, BURST + 18, BURST + 64, [-40, 140], INOUT);
  const logo = sp(f, BURST, {damping: 14, stiffness: 120});
  const sub = ease(f, BURST + 22, BURST + 38);
  const cred = ease(f, BURST + 38, BURST + 56);
  const fadeText = 1 - ease(f, len - 40, len - 28);
  const burst = ease(f, BURST - 2, BURST + 24);

  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: FONT}}>
      <AbsoluteFill style={{background: `radial-gradient(circle at 50% 50%, ${C.deep} 0%, transparent 60%)`, opacity: ease(f, BURST - 10, BURST + 20) * fadeText}} />
      <svg width="1080" height="1080" style={{position: 'absolute'}}>
        {P.map((p, i) => {
          const t = ease(f, p.delay, p.delay + 30, [0, 1], INOUT);
          const tp = ease(f - 2, p.delay, p.delay + 30, [0, 1], INOUT);
          const a = p.ta + (spin * Math.PI) / 180;
          const r = ry * (1 - close);
          const tx = 540 + Math.cos(a) * r * RXK;
          const ty = 540 + Math.sin(a) * r;
          const x = p.sx + (tx - p.sx) * t;
          const y = p.sy + (ty - p.sy) * t;
          return (
            <g key={i} opacity={1 - ease(f, len - 10, len - 4)}>
              <line x1={p.sx + (tx - p.sx) * tp} y1={p.sy + (ty - p.sy) * tp} x2={x} y2={y} stroke={p.gold ? C.gold : C.mute} strokeWidth={p.size} strokeLinecap="round" opacity={0.6} />
              <circle cx={x} cy={y} r={p.size} fill={p.gold ? C.goldL : C.white} />
            </g>
          );
        })}
        {burst > 0 && burst < 1 && <ellipse cx="540" cy="540" rx={(RY + burst * 500) * RXK} ry={RY + burst * 500} fill="none" stroke={C.goldL} strokeWidth={12 * (1 - burst)} opacity={1 - burst} />}
        <circle cx="540" cy="540" r={9 * ease(f, len - 10, len - 5) * (1 - ease(f, len - 3, len))} fill={C.goldL} />
      </svg>

      <div style={{position: 'absolute', top: 360, width: '100%', textAlign: 'center', opacity: fadeText}}>
        <div style={{display: 'inline-block', fontSize: 74, fontWeight: 900, lineHeight: 1.05, letterSpacing: tracking, paddingLeft: tracking, backgroundImage: `linear-gradient(110deg, transparent ${shine - 12}%, rgba(255,255,255,0.95) ${shine}%, transparent ${shine + 12}%), ${gold}`, WebkitBackgroundClip: 'text', color: 'transparent', opacity: f < BURST ? 0 : 1, transform: `scale(${0.6 + 0.4 * logo})`, filter: `blur(${(1 - Math.min(1, logo)) * 14}px)`}}>
          JOSÉ ANTONIO
          <br />
          SERRANO
        </div>
        <div style={{width: 220 * sub, height: 2, background: C.gold, margin: '22px auto 18px'}} />
        <div style={{color: C.white, fontSize: 24, fontWeight: 700, letterSpacing: 8, opacity: sub, transform: `translateY(${(1 - sub) * 18}px)`}}>AML · CUMPLIMIENTO · GRC</div>
        <div style={{marginTop: 24, opacity: cred, transform: `translateY(${(1 - cred) * 14}px)`}}>
          {CRED.map((c) => (
            <div key={c} style={{color: C.mute, fontSize: 15, fontWeight: 700, letterSpacing: 2.5, lineHeight: 1.75}}>
              {c}
            </div>
          ))}
        </div>
      </div>
    </AbsoluteFill>
  );
};
