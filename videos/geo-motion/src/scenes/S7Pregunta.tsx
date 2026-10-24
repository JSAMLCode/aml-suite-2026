import React from 'react';
import {AbsoluteFill, Easing, useCurrentFrame} from 'remotion';
import {C, FONT, ease, sp} from '../theme';
import {SectionLabel, Words} from '../ui';
import {span, wf} from '../tl';

const ID = '07';
const LEN = span(ID).len;
const RING = {x: 540, y: 660};

export const S7Pregunta: React.FC = () => {
  const f = useCurrentFrame();
  const tec = wf(ID, 'tecnología');
  const o = wf(ID, 'o');
  const cum = wf(ID, 'cumplimiento');
  // zoom a través de la "o": transición hacia la fuente
  const zIn = LEN - 22;
  const z = ease(f, zIn, LEN, [0, 1], Easing.in(Easing.exp));
  const scale = 1 + z * 70;
  const ring = sp(f, o - 3, {damping: 11, stiffness: 220});
  const speed = ease(f, zIn + 4, LEN);

  const card = (label: string, at: number, x: number, dir: number) => {
    const p = sp(f, at - 2, {damping: 15, stiffness: 150});
    return (
      <div style={{position: 'absolute', left: x, top: RING.y - 110, width: 330, height: 220, perspective: 900, opacity: Math.min(1, p * 1.5)}}>
        <div style={{width: '100%', height: '100%', borderRadius: 22, border: `2px solid ${C.gold}`, background: 'linear-gradient(160deg, rgba(31,48,106,0.95), rgba(17,27,61,0.95))', display: 'flex', alignItems: 'center', justifyContent: 'center', color: C.white, fontSize: 36, fontWeight: 900, letterSpacing: 2, transform: `rotateY(${dir * (14 + (1 - p) * 60)}deg) translateX(${(1 - p) * dir * -260}px)`, boxShadow: '0 30px 60px rgba(0,0,0,0.45)'}}>
          {label}
        </div>
      </div>
    );
  };

  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: FONT, overflow: 'hidden'}}>
      {speed > 0 && (
        <svg width="1080" height="1080" style={{position: 'absolute', opacity: speed * 0.8}}>
          {Array.from({length: 40}).map((_, i) => {
            const a = (i / 40) * Math.PI * 2 + i * 0.37;
            const r0 = 200 + ((i * 97 + f * 40) % 500);
            const len = 80 + speed * 200;
            return <line key={i} x1={540 + Math.cos(a) * r0} y1={540 + Math.sin(a) * r0} x2={540 + Math.cos(a) * (r0 + len)} y2={540 + Math.sin(a) * (r0 + len)} stroke={i % 5 ? C.mute : C.gold} strokeWidth={3} strokeLinecap="round" />;
          })}
        </svg>
      )}
      <AbsoluteFill style={{transformOrigin: `${RING.x}px ${RING.y}px`, transform: `translate(0, ${(540 - RING.y) * z}px) scale(${scale})`}}>
        <div style={{position: 'absolute', left: 64, top: 220, opacity: 1 - ease(f, zIn, zIn + 6)}}>
          <Words
            size={64}
            align="center"
            words={[
              {t: '¿Quién', at: wf(ID, 'quién')},
              {t: 'es', at: wf(ID, 'es')},
              {t: 'el', at: wf(ID, 'el')},
              {t: 'dueño', at: wf(ID, 'dueño'), color: C.gold},
              {t: 'de', at: wf(ID, 'de', 1)},
              {t: 'este', at: wf(ID, 'este')},
              {t: 'proyecto?', at: wf(ID, 'proyecto')},
            ]}
          />
        </div>
        {card('Tecnología', tec, 60, 1)}
        {card('Cumplimiento', cum, 690, -1)}
        {f >= o - 3 && (
          <svg width="1080" height="1080" style={{position: 'absolute'}}>
            <circle cx={RING.x} cy={RING.y} r={44 * ring} fill="none" stroke={C.gold} strokeWidth={20} />
          </svg>
        )}
      </AbsoluteFill>
      <div style={{opacity: 1 - ease(f, zIn, zIn + 6)}}>
        <SectionLabel n="06" title="La pregunta" />
      </div>
    </AbsoluteFill>
  );
};
