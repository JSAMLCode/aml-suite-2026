import React from 'react';
import {Composition} from 'remotion';
import {Geo} from './Showreel';
import {TL} from './tl';
import {FPS} from './theme';

export const Root: React.FC = () => (
  <Composition id="GeoInferencial" component={Geo} durationInFrames={TL.end} fps={FPS} width={1080} height={1080} />
);
