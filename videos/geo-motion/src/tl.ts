import tl from './timeline.json';

export const TL = tl;
export const W = 1080;
export const H = 1080;

const norm = (s: string) =>
  s
    .toLowerCase()
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/[^a-z0-9]/g, '');

export const line = (id: string) => {
  const l = TL.lines.find((x) => x.id === id);
  if (!l) throw new Error(`Frase ${id} no existe`);
  return l;
};

// Fotograma local (desde el inicio de la frase) de la palabra n-ésima que empieza por `word`
export const wf = (id: string, word: string, nth = 0) => {
  const hits = line(id).words.filter((w) => norm(w.w).startsWith(norm(word)));
  if (!hits[nth]) throw new Error(`"${word}" no está en la frase ${id}`);
  return hits[nth].f;
};

// Tramo de cada escena: desde su frase hasta la siguiente (o la firma)
export const span = (id: string) => {
  const i = TL.lines.findIndex((x) => x.id === id);
  const from = TL.lines[i].start;
  const to = i + 1 < TL.lines.length ? TL.lines[i + 1].start : TL.sign;
  return {from, len: to - from};
};
