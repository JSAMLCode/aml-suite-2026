import React from 'react';
import {AbsoluteFill, Easing, useCurrentFrame} from 'remotion';
import {C, FONT, ease, sp} from '../theme';
import {SectionLabel} from '../ui';

// Cajas de ancho fijo: la "O" queda en una posición conocida para el zoom
const LETTERS = ['M', 'O', 'T', 'I', 'O', 'N'];
const BOXW = 250;
const LEFT0 = 960 - (LETTERS.length * BOXW) / 2;
const RING_X = LEFT0 + BOXW * 1 + BOXW / 2;
const RING_Y = 540;
const ZOOM_IN = 42;
const ZOOM_OUT = 84;

export const S6ZoomThrough: React.FC = () => {
  const f = useCurrentFrame();
  const z = ease(f, ZOOM_IN, ZOOM_OUT, [0, 1], Easing.in(Easing.exp));
  const scale = 1 + z * 90;
  const speed = ease(f, ZOOM_IN + 10, ZOOM_OUT - 4);

  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: FONT, overflow: 'hidden'}}>
      {/* líneas de velocidad durante el zoom */}
      {speed > 0 && (
        <svg width="1920" height="1080" style={{position: 'absolute', opacity: speed * 0.8}}>
          {Array.from({length: 48}).map((_, i) => {
            const a = (i / 48) * Math.PI * 2 + i * 0.37;
            const r0 = 300 + ((i * 97 + f * 40) % 700);
            const len = 120 + speed * 260;
            return (
              <line
                key={i}
                x1={960 + Math.cos(a) * r0}
                y1={540 + Math.sin(a) * r0}
                x2={960 + Math.cos(a) * (r0 + len)}
                y2={540 + Math.sin(a) * (r0 + len)}
                stroke={i % 5 === 0 ? C.gold : C.mute}
                strokeWidth={3}
                strokeLinecap="round"
              />
            );
          })}
        </svg>
      )}

      {/* desplazamos la O al centro mientras escalamos sobre ella */}
      <AbsoluteFill
        style={{
          transformOrigin: `${RING_X}px ${RING_Y}px`,
          transform: `translate(${(960 - RING_X) * z}px, 0) scale(${scale})`,
        }}
      >
        {LETTERS.map((ch, i) => {
          const p = sp(f, 2 + i * 3, {damping: 15, stiffness: 150});
          const style: React.CSSProperties = {
            position: 'absolute',
            left: LEFT0 + i * BOXW,
            top: RING_Y - 170,
            width: BOXW,
            height: 340,
            overflow: 'hidden',
          };
          if (i === 1) {
            return (
              <div key={i} style={style}>
                <svg width={BOXW} height={340} style={{transform: `translateY(${(1 - p) * 340}px)`}}>
                  <circle cx={BOXW / 2} cy={170} r={98} fill="none" stroke={C.gold} strokeWidth={46} />
                </svg>
              </div>
            );
          }
          return (
            <div key={i} style={style}>
              <div style={{transform: `translateY(${(1 - p) * 340}px)`, textAlign: 'center', fontSize: 300, fontWeight: 900, lineHeight: '340px', color: C.white}}>{ch}</div>
            </div>
          );
        })}
      </AbsoluteFill>

      <div style={{position: 'absolute', top: 760, width: '100%', textAlign: 'center', color: C.mute, fontSize: 26, fontWeight: 700, letterSpacing: 10, opacity: ease(f, 14, 26) * (1 - ease(f, ZOOM_IN, ZOOM_IN + 8))}}>
        ZOOM-THROUGH · MATCH CUT · WHIP PAN
      </div>
      <div style={{opacity: 1 - ease(f, ZOOM_IN, ZOOM_IN + 8)}}>
        <SectionLabel n="05" title="Transiciones" />
      </div>
    </AbsoluteFill>
  );
};
