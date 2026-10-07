import React from 'react';
import {AbsoluteFill, interpolateColors, useCurrentFrame} from 'remotion';
import {interpolatePath, translatePath} from '@remotion/paths';
import {makeCircle, makePolygon, makeRect, makeStar, makeTriangle} from '@remotion/shapes';
import {noise3D} from '@remotion/noise';
import {C, FONT, IN, INOUT, ease, sp} from '../theme';
import {SectionLabel} from '../ui';

const BOX = 460;
const centered = (s: {path: string; width: number; height: number}) =>
  translatePath(s.path, (BOX - s.width) / 2, (BOX - s.height) / 2);

const SHAPES = [
  centered(makeCircle({radius: 190})),
  centered(makeRect({width: 340, height: 340, cornerRadius: 36})),
  centered(makeTriangle({length: 430, direction: 'up', cornerRadius: 24})),
  centered(makePolygon({points: 6, radius: 205, cornerRadius: 20})),
  centered(makeStar({points: 5, innerRadius: 95, outerRadius: 220, cornerRadius: 14})),
  centered(makeCircle({radius: 190})),
];
const MORPHS = [14, 34, 54, 74, 92]; // inicio de cada transformación
const MORPH_LEN = 12;

const shapeAt = (f: number) => {
  for (let i = MORPHS.length - 1; i >= 0; i--) {
    if (f >= MORPHS[i]) {
      const p = ease(f, MORPHS[i], MORPHS[i] + MORPH_LEN, [0, 1], INOUT);
      return interpolatePath(p, SHAPES[i], SHAPES[i + 1]);
    }
  }
  return SHAPES[0];
};

const COLS = 32;
const ROWS = 18;
const GAP = 60;

export const S3Shapes: React.FC = () => {
  const f = useCurrentFrame();
  const enter = sp(f, 0, {damping: 12, stiffness: 120});
  // pequeño rebote al final de cada transformación
  const pop = MORPHS.reduce((acc, t) => acc + (sp(f, t + MORPH_LEN - 4, {damping: 8, stiffness: 300}) - sp(f, t + MORPH_LEN + 2, {damping: 8, stiffness: 300})) * 0.12, 0);
  const rot = ease(f, 0, 104, [-20, 70], INOUT);

  const exit = ease(f, 104, 120, [0, 1], IN);
  const fill = interpolateColors(exit, [0, 0.5], [C.gold, C.navy2]);
  const scale = (0.2 + 0.8 * enter + pop) * (1 + exit * 13);

  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: FONT}}>
      {/* rejilla de puntos: ruido + ondas en cada transformación */}
      <svg width="1920" height="1080" style={{position: 'absolute', opacity: 1 - exit}}>
        {Array.from({length: COLS * ROWS}).map((_, k) => {
          const c = k % COLS;
          const r = Math.floor(k / COLS);
          const x = 960 + (c - (COLS - 1) / 2) * GAP;
          const y = 540 + (r - (ROWS - 1) / 2) * GAP;
          const d = Math.hypot(x - 960, y - 540);
          const n = (noise3D('grid', c * 0.13, r * 0.13, f * 0.025) + 1) / 2;
          let bump = 0;
          for (const t of MORPHS) {
            const age = f - t;
            if (age < 0 || age > 40) continue;
            bump += Math.exp(-(((d - age * 30) / 70) ** 2)) * (1 - age / 40);
          }
          const appear = ease(f, d / 40, d / 40 + 10);
          return (
            <circle
              key={k}
              cx={x}
              cy={y}
              r={(1.5 + n * 2.5 + bump * 5) * appear}
              fill={bump > 0.15 ? C.goldL : C.mute}
              opacity={0.25 + n * 0.3 + bump * 0.5}
            />
          );
        })}
      </svg>

      {/* órbita con satélites */}
      <svg width="1920" height="1080" style={{position: 'absolute', opacity: enter * (1 - exit)}}>
        <circle cx="960" cy="540" r="340" fill="none" stroke={C.mute} strokeOpacity={0.35} strokeWidth={2} strokeDasharray="4 14" transform={`rotate(${f * 0.8} 960 540)`} />
        {[0, 1, 2].map((i) => {
          const a = ((f * 2.4 + i * 120) * Math.PI) / 180;
          return <circle key={i} cx={960 + Math.cos(a) * 340} cy={540 + Math.sin(a) * 340} r={i === 0 ? 10 : 6} fill={i === 0 ? C.teal : C.gold} />;
        })}
      </svg>

      {/* forma principal */}
      <div style={{position: 'absolute', left: 960 - BOX / 2, top: 540 - BOX / 2, width: BOX, height: BOX, transform: `scale(${scale}) rotate(${rot}deg)`}}>
        <svg width={BOX} height={BOX} style={{overflow: 'visible'}}>
          <defs>
            <linearGradient id="gg" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0" stopColor={exit > 0 ? fill : C.goldL} />
              <stop offset="1" stopColor={exit > 0 ? fill : C.goldD} />
            </linearGradient>
          </defs>
          <path d={shapeAt(f)} fill="url(#gg)" />
          <path d={shapeAt(f)} fill="none" stroke={C.cream} strokeOpacity={0.5 * (1 - exit)} strokeWidth={3} transform={`translate(${BOX / 2} ${BOX / 2}) scale(1.12) translate(${-BOX / 2} ${-BOX / 2})`} />
        </svg>
      </div>

      <div style={{opacity: 1 - exit}}>
        <SectionLabel n="02" title="Morphing y geometría" />
      </div>
    </AbsoluteFill>
  );
};
