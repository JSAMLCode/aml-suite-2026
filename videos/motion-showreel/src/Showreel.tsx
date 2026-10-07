import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile} from 'remotion';
import {CUTS, C} from './theme';
import {loadFonts} from './fonts';
import {EditorHud, Flash, Grain, Vignette} from './ui';
import {S1ColdOpen} from './scenes/S1ColdOpen';
import {S2Kinetic} from './scenes/S2Kinetic';
import {S3Shapes} from './scenes/S3Shapes';
import {S4Data} from './scenes/S4Data';
import {S5Depth} from './scenes/S5Depth';
import {S6ZoomThrough} from './scenes/S6ZoomThrough';
import {S7Resolve} from './scenes/S7Resolve';

loadFonts();

const SCENES = [
  {from: CUTS.open, to: CUTS.type, C: S1ColdOpen},
  {from: CUTS.type, to: CUTS.shapes, C: S2Kinetic},
  {from: CUTS.shapes, to: CUTS.data, C: S3Shapes},
  {from: CUTS.data, to: CUTS.depth, C: S4Data},
  {from: CUTS.depth, to: CUTS.zoom, C: S5Depth},
  {from: CUTS.zoom, to: CUTS.logo, C: S6ZoomThrough},
  {from: CUTS.logo, to: CUTS.end, C: S7Resolve},
];

export const Showreel: React.FC = () => (
  <AbsoluteFill style={{background: C.navy}}>
    {SCENES.map(({from, to, C: Scene}) => (
      <Sequence key={from} from={from} durationInFrames={to - from}>
        <Scene />
      </Sequence>
    ))}

    <Flash at={CUTS.type} />
    <Flash at={CUTS.depth} color={C.goldL} max={0.5} />
    <Flash at={CUTS.logo + 61} color={C.goldL} max={0.55} />

    <Vignette />
    <Grain />
    <Sequence from={CUTS.type} durationInFrames={CUTS.logo - CUTS.type}>
      <EditorHud />
    </Sequence>

    <Audio src={staticFile('score.wav')} />
  </AbsoluteFill>
);
