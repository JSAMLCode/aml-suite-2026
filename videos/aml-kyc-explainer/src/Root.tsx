import React from 'react';
import {Composition} from 'remotion';
import {Explainer} from './Explainer';
import {CUTS, FPS, H, W} from './theme';

export const Root: React.FC = () => (
  <Composition id="Explainer" component={Explainer} durationInFrames={CUTS.end} fps={FPS} width={W} height={H} />
);
