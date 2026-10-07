import React from 'react';
import {Composition} from 'remotion';
import {Frame, Fmt} from './Frame';
import {TL} from './tl';
import {FPS} from './theme';

const FORMATS: {id: string; fmt: Fmt; w: number; h: number}[] = [
  {id: 'Geo-1x1', fmt: '1x1', w: 1080, h: 1080},
  {id: 'Geo-4x5', fmt: '4x5', w: 1080, h: 1350},
  {id: 'Geo-9x16', fmt: '9x16', w: 1080, h: 1920},
  {id: 'Geo-16x9', fmt: '16x9', w: 1920, h: 1080},
];

export const Root: React.FC = () => (
  <>
    {FORMATS.map((c) => (
      <Composition key={c.id} id={c.id} component={Frame} defaultProps={{fmt: c.fmt}} durationInFrames={TL.end} fps={FPS} width={c.w} height={c.h} />
    ))}
  </>
);
