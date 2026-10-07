import React from 'react';
import {AbsoluteFill, Sequence} from 'remotion';
import {C} from './theme';
import {loadFonts} from './fonts';
import {TL, span} from './tl';
import {Flash} from './ui';
import {S0Open, S1Fecha} from './scenes/S1Fecha';
import {S2Art53} from './scenes/S2Art53';
import {S3Art14} from './scenes/S3Art14';
import {S4Senales} from './scenes/S4Senales';
import {S5Controles} from './scenes/S5Controles';
import {S6Plazo} from './scenes/S6Plazo';
import {S7Pregunta} from './scenes/S7Pregunta';
import {S8Fuente, S9Firma} from './scenes/S8Fuente';

loadFonts();

// Escenario 1080×1080: todas las escenas. Cada formato lo coloca y le añade su marco.

const SCENES: [string, React.FC][] = [
  ['01', S1Fecha],
  ['02', S2Art53],
  ['03', S3Art14],
  ['04', S4Senales],
  ['05', S5Controles],
  ['06', S6Plazo],
  ['07', S7Pregunta],
  ['08', S8Fuente],
];

export const Stage: React.FC = () => (
  <AbsoluteFill style={{background: C.navy, overflow: 'hidden'}}>
    <Sequence durationInFrames={TL.open}>
      <S0Open />
    </Sequence>
    {SCENES.map(([id, Scene]) => (
      <Sequence key={id} from={span(id).from} durationInFrames={span(id).len}>
        <Scene />
      </Sequence>
    ))}
    <Sequence from={TL.sign} durationInFrames={TL.end - TL.sign}>
      <S9Firma />
    </Sequence>

    {['02', '03', '04', '05', '06', '07'].map((id) => (
      <Flash key={id} at={span(id).from} max={0.35} />
    ))}

  </AbsoluteFill>
);
