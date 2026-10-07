// Renderiza fotogramas sueltos con un solo bundle: node review.mjs 30 60 90 ...
import {bundle} from '@remotion/bundler';
import {selectComposition, renderStill} from '@remotion/renderer';
import path from 'node:path';

const frames = process.argv.slice(2).map(Number);
const browserExecutable = '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell';
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts')});
const composition = await selectComposition({serveUrl, id: process.env.COMP ?? 'GeoInferencial', browserExecutable});
for (const frame of frames) {
  await renderStill({serveUrl, composition, frame, output: `${process.env.OUTDIR ?? "out/frames"}/f${String(frame).padStart(3, '0')}.png`, browserExecutable, chromiumOptions: {gl: 'swangle'}});
  console.log('ok', frame);
}
