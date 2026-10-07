import React from 'react';
import {Composition} from 'remotion';
import {Showreel} from './Showreel';
import {CUTS, FPS} from './theme';

export const Root: React.FC = () => (
  <Composition id="Showreel" component={Showreel} durationInFrames={CUTS.end} fps={FPS} width={1920} height={1080} />
);
