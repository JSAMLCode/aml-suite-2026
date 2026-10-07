import React from 'react';
import {AbsoluteFill, Audio, staticFile, useCurrentFrame} from 'remotion';
import {C, FONT, ease, sp} from './theme';
import {CHAPTERS, TL, span} from './tl';
import {EditorHud, Grain, Vignette} from './ui';
import {Stage} from './Stage';

export type Fmt = '1x1' | '4x5' | '9x16' | '16x9';

// ---------- subtítulos palabra a palabra ----------
type Word = {w: string; f: number};
type Cue = {words: Word[]; from: number; to: number};

// Bloques que terminan en signo de puntuación o a las 7 palabras
const CUES: Cue[] = (() => {
  const out: Cue[] = [];
  TL.lines.forEach((l, li) => {
    const lineEnd = li + 1 < TL.lines.length ? TL.lines[li + 1].start : TL.sign;
    let cur: Word[] = [];
    const flush = () => {
      if (cur.length) out.push({words: cur, from: cur[0].f, to: 0});
      cur = [];
    };
    l.words.forEach((w) => {
      cur.push({w: w.w, f: l.start + w.f});
      if (/[.,:;?]$/.test(w.w) || cur.length >= 7) flush();
    });
    flush();
    // cada bloque dura hasta que empieza el siguiente de su frase (o el fin de la frase)
    const mine = out.filter((c) => c.from >= l.start && c.from < lineEnd);
    mine.forEach((c, i) => (c.to = i + 1 < mine.length ? mine[i + 1].from : Math.min(lineEnd, c.words[c.words.length - 1].f + 40)));
  });
  return out;
})();

const Captions: React.FC<{size: number; align: 'center' | 'left'; width: number}> = ({size, align, width}) => {
  const f = useCurrentFrame();
  const cue = CUES.find((c) => f >= c.from - 3 && f < c.to);
  if (!cue) return null;
  const inP = sp(f, cue.from - 3, {damping: 18, stiffness: 200});
  const out = ease(f, cue.to - 4, cue.to);
  return (
    <div style={{width, display: 'flex', flexWrap: 'wrap', justifyContent: align === 'center' ? 'center' : 'flex-start', columnGap: size * 0.28, rowGap: size * 0.1, fontFamily: FONT, transform: `translateY(${(1 - inP) * 24}px)`, opacity: Math.min(1, inP * 1.4) * (1 - out)}}>
      {cue.words.map((w, i) => {
        const next = cue.words[i + 1]?.f ?? cue.to;
        const said = f >= w.f;
        const now = said && f < next;
        return (
          <span key={i} style={{fontSize: size, fontWeight: 800, lineHeight: 1.2, color: now ? C.goldL : said ? C.white : 'rgba(244,246,251,0.35)', textShadow: '0 2px 12px rgba(0,0,0,0.5)'}}>
            {w.w}
          </span>
        );
      })}
    </div>
  );
};

// ---------- progreso por capítulos ----------
const IDS = TL.lines.map((l) => l.id);
const chapterAt = (f: number) => {
  let cur = -1;
  IDS.forEach((id, i) => {
    if (f >= span(id).from) cur = i;
  });
  return f >= TL.sign ? IDS.length : cur;
};

// Barras tipo historia (vertical y 4:5)
const StoryBar: React.FC<{width: number}> = ({width}) => {
  const f = useCurrentFrame();
  const gap = 8;
  const w = (width - gap * (IDS.length - 1)) / IDS.length;
  return (
    <div style={{display: 'flex', gap, width}}>
      {IDS.map((id) => {
        const {from, len} = span(id);
        const p = ease(f, from, from + len, [0, 1], (t) => t);
        return (
          <div key={id} style={{width: w, height: 5, borderRadius: 3, background: 'rgba(142,154,184,0.3)', overflow: 'hidden'}}>
            <div style={{width: `${p * 100}%`, height: '100%', background: C.gold}} />
          </div>
        );
      })}
    </div>
  );
};

// Índice lateral (horizontal)
const ChapterRail: React.FC = () => {
  const f = useCurrentFrame();
  const cur = chapterAt(f);
  const on = ease(f, 8, 30);
  return (
    <div style={{fontFamily: FONT, opacity: on}}>
      {IDS.map((id, i) => {
        const active = i === cur;
        const done = i < cur;
        const a = active ? sp(f, span(id).from, {damping: 18, stiffness: 160}) : 0;
        return (
          <div key={id} style={{display: 'flex', alignItems: 'center', gap: 16, height: 54}}>
            <div style={{width: 6 + a * 34, height: 3, background: active ? C.gold : done ? C.mute : 'rgba(142,154,184,0.3)'}} />
            <div style={{fontSize: 18, fontWeight: 800, letterSpacing: 2, color: active ? C.gold : 'rgba(142,154,184,0.6)', width: 30}}>{id}</div>
            <div style={{fontSize: active ? 24 : 20, fontWeight: active ? 900 : 600, color: active ? C.white : done ? C.mute : 'rgba(142,154,184,0.45)'}}>{CHAPTERS[id]}</div>
          </div>
        );
      })}
    </div>
  );
};

const Brand: React.FC<{size?: number}> = ({size = 22}) => {
  const f = useCurrentFrame();
  const o = ease(f, 10, 28);
  return (
    <div style={{fontFamily: FONT, opacity: o}}>
      <div style={{color: C.gold, fontSize: size * 0.8, fontWeight: 800, letterSpacing: 6}}>ACUERDO 1-2026 · SBP</div>
      <div style={{color: C.white, fontSize: size * 1.6, fontWeight: 900, marginTop: 6, lineHeight: 1.1}}>Geolocalización inferencial</div>
    </div>
  );
};

// La firma ocupa todo el lienzo: el marco se retira al llegar a ella
const useChrome = () => {
  const f = useCurrentFrame();
  return 1 - ease(f, TL.sign - 12, TL.sign);
};

export const Frame: React.FC<{fmt: Fmt}> = ({fmt}) => {
  const chrome = useChrome();
  const f = useCurrentFrame();
  const stage = (left: number, top: number) => (
    <div style={{position: 'absolute', left, top, width: 1080, height: 1080, overflow: 'hidden'}}>
      <Stage />
    </div>
  );
  return (
    <AbsoluteFill style={{background: C.navy}}>
      {fmt === '1x1' && stage(0, 0)}

      {fmt === '4x5' && (
        <>
          {stage(0, 0)}
          <div style={{position: 'absolute', left: 64, top: 1110, width: 952, height: 200, display: 'flex', alignItems: 'center', justifyContent: 'center', opacity: chrome}}>
            <Captions size={40} align="center" width={952} />
          </div>
        </>
      )}

      {fmt === '9x16' && (
        <>
          <div style={{position: 'absolute', left: 64, top: 170, opacity: chrome}}>
            <StoryBar width={952} />
            <div style={{marginTop: 26}}>
              <Brand size={22} />
            </div>
          </div>
          {stage(0, 360)}
          <div style={{position: 'absolute', left: 64, top: 1450, width: 952, height: 190, display: 'flex', alignItems: 'flex-start', justifyContent: 'center', opacity: chrome}}>
            <Captions size={46} align="center" width={952} />
          </div>
        </>
      )}

      {fmt === '16x9' && (
        <>
          {stage(420, 0)}
          <div style={{position: 'absolute', left: 64, top: 110, opacity: chrome}}>
            <Brand size={20} />
          </div>
          <div style={{position: 'absolute', left: 64, top: 330, opacity: chrome}}>
            <ChapterRail />
          </div>
          <div style={{position: 'absolute', left: 1540, top: 0, width: 330, height: 1080, display: 'flex', alignItems: 'center', opacity: chrome}}>
            <Captions size={34} align="left" width={330} />
          </div>
          <div style={{position: 'absolute', left: 419, top: 80, width: 1, height: 920, background: 'rgba(142,154,184,0.18)', opacity: chrome}} />
          <div style={{position: 'absolute', left: 1500, top: 80, width: 1, height: 920, background: 'rgba(142,154,184,0.18)', opacity: chrome}} />
        </>
      )}

      <Vignette />
      <Grain />
      {(fmt === '1x1' || fmt === '16x9') && (
        <div style={{position: 'absolute', inset: 0, opacity: chrome * ease(f, span('02').from, span('02').from + 15)}}>
          <EditorHud />
        </div>
      )}
      <Audio src={staticFile('mix.wav')} />
    </AbsoluteFill>
  );
};
