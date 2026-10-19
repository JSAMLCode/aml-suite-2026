import React from 'react';
import {createRoot} from 'react-dom/client';
import {Player} from '@remotion/player';
import {Explainer} from './Explainer';
import {CUTS, FPS, H, W} from './theme';

(window as any).remotion_staticBase = '.';

const App: React.FC = () => (
  <Player
    component={Explainer}
    durationInFrames={CUTS.end}
    fps={FPS}
    compositionWidth={W}
    compositionHeight={H}
    controls
    loop
    autoPlay
    initiallyMuted
    clickToPlay
    style={{height: '100vh', aspectRatio: `${W}/${H}`, maxWidth: '100vw'}}
  />
);

createRoot(document.getElementById('root')!).render(<App />);
