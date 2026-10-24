import {build} from 'esbuild';
import {cpSync, mkdirSync, writeFileSync} from 'node:fs';

mkdirSync('dist', {recursive: true});
await build({
  entryPoints: ['src/player.tsx'],
  bundle: true,
  minify: true,
  outfile: 'dist/player.js',
  define: {'process.env.NODE_ENV': '"production"'},
  loader: {'.ttf': 'file'},
});
cpSync('public/fonts', 'dist/fonts', {recursive: true});
writeFileSync(
  'dist/index.html',
  `<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AML KYC Explainer</title>
<style>html,body{margin:0;height:100%;background:#0A1128;display:flex;justify-content:center;align-items:center;overflow:hidden}#root{height:100%;display:flex;justify-content:center}</style>
</head><body><div id="root"></div><script src="player.js"></script></body></html>`,
);
