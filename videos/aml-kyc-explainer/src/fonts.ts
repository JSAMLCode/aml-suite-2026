import {continueRender, delayRender, staticFile} from 'remotion';

const weights: [number, string][] = [
  [300, 'n1.ttf'],
  [400, 'n2.ttf'],
  [600, 'n600.ttf'],
  [700, 'n3.ttf'],
  [800, 'n800.ttf'],
  [900, 'n4.ttf'],
];

let loaded = false;

export const loadFonts = () => {
  if (loaded || typeof document === 'undefined') return;
  loaded = true;
  const handle = delayRender('Cargando Nunito Sans');
  Promise.all(
    weights.map(([w, file]) => {
      const face = new FontFace('Nunito Sans', `url(${staticFile(`fonts/${file}`)})`, {
        weight: String(w),
      });
      document.fonts.add(face);
      return face.load();
    }),
  ).then(() => continueRender(handle));
};
