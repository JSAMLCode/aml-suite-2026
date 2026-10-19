import React from 'react';
import {AbsoluteFill, Sequence} from 'remotion';
import {CUTS, C} from './theme';
import {loadFonts} from './fonts';
import {EditorHud, Flash, Grain, Vignette} from './ui';
import {S1Open} from './scenes/S1Open';
import {S2Kyc} from './scenes/S2Kyc';
import {S3Flow} from './scenes/S3Flow';
import {S4Matrix} from './scenes/S4Matrix';
import {S5Rba} from './scenes/S5Rba';
import {S6Brand} from './scenes/S6Brand';

const SCENES = [
  {from: CUTS.open, to: CUTS.kyc, C: S1Open},
  {from: CUTS.kyc, to: CUTS.flow, C: S2Kyc},
  {from: CUTS.flow, to: CUTS.matrix, C: S3Flow},
  {from: CUTS.matrix, to: CUTS.rba, C: S4Matrix},
  {from: CUTS.rba, to: CUTS.brand, C: S5Rba},
  {from: CUTS.brand, to: CUTS.end, C: S6Brand},
];

export const Explainer: React.FC = () => {
  loadFonts();
  return (
    <AbsoluteFill style={{background: C.navy}}>
      {SCENES.map(({from, to, C: Scene}) => (
        <Sequence key={from} from={from} durationInFrames={to - from}>
          <Scene />
        </Sequence>
      ))}
      <Flash at={CUTS.kyc} />
      <Flash at={CUTS.matrix} color={C.goldL} max={0.5} />
      <Flash at={CUTS.brand} color={C.goldL} max={0.55} />
      <Vignette />
      <Grain />
      <Sequence from={CUTS.kyc} durationInFrames={CUTS.brand - CUTS.kyc}>
        <EditorHud />
      </Sequence>
    </AbsoluteFill>
  );
};
