import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C, FONT, IN, INOUT, ease, shake, sp} from '../theme';
import {SectionLabel} from '../ui';

const STAMP = 62;

const Card: React.FC<{children: React.ReactNode; accent: string}> = ({children, accent}) => (
  <div
    style={{
      width: 520,
      height: 620,
      borderRadius: 28,
      background: 'linear-gradient(160deg, rgba(31,48,106,0.95), rgba(17,27,61,0.95))',
      border: `2px solid ${accent}`,
      boxShadow: `0 40px 80px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.08)`,
      padding: 44,
      boxSizing: 'border-box',
      fontFamily: FONT,
      color: C.white,
      position: 'relative',
      overflow: 'hidden',
    }}
  >
    {children}
  </div>
);

const Row: React.FC<{w: number; c?: string; h?: number}> = ({w, c = C.mute, h = 16}) => (
  <div style={{width: w, height: h, borderRadius: h / 2, background: c, opacity: 0.5, marginBottom: 18}} />
);

export const S5Depth: React.FC = () => {
  const f = useCurrentFrame();
  const enter = sp(f, 0, {damping: 20, stiffness: 60});
  const orbit = ease(f, 0, 100, [-38, 18], INOUT);
  const dolly = ease(f, 0, 100, [-900, -250], INOUT);
  const sh = shake(f, STAMP, 12, 12);
  const stamp = sp(f, STAMP - 6, {damping: 10, stiffness: 320, mass: 0.7});

  const cards = [
    {
      accent: C.teal,
      body: (
        <>
          <div style={{width: 120, height: 120, borderRadius: 60, background: C.teal, opacity: 0.85, marginBottom: 30}} />
          <div style={{fontSize: 30, fontWeight: 800, marginBottom: 24}}>Perfil KYC</div>
          <Row w={380} />
          <Row w={300} />
          <Row w={340} />
          <Row w={220} c={C.teal} />
        </>
      ),
    },
    {
      accent: C.gold,
      body: (
        <>
          <div style={{fontSize: 30, fontWeight: 800, marginBottom: 30}}>Debida diligencia</div>
          {[0.9, 0.55, 0.75, 0.35, 0.65].map((v, i) => {
            const g = sp(f, 18 + i * 4, {damping: 16});
            return (
              <div key={i} style={{display: 'flex', alignItems: 'center', gap: 16, marginBottom: 22}}>
                <div style={{width: 26, height: 26, borderRadius: 6, border: `3px solid ${C.gold}`, background: g > 0.6 ? C.gold : 'transparent'}} />
                <div style={{height: 16, borderRadius: 8, background: C.mute, opacity: 0.5, width: 340 * v * g}} />
              </div>
            );
          })}
          <div
            style={{
              position: 'absolute',
              left: 70,
              bottom: 90,
              padding: '14px 26px',
              border: `6px solid ${C.coral}`,
              borderRadius: 12,
              color: C.coral,
              fontSize: 54,
              fontWeight: 900,
              letterSpacing: 6,
              transform: `rotate(-12deg) scale(${f < STAMP - 6 ? 0 : 3 - 2 * stamp})`,
              opacity: f < STAMP - 6 ? 0 : Math.min(1, stamp * 2),
            }}
          >
            VERIFICADO
          </div>
        </>
      ),
    },
    {
      accent: C.coral,
      body: (
        <>
          <div style={{fontSize: 30, fontWeight: 800, marginBottom: 30}}>Monitoreo</div>
          <div style={{display: 'flex', alignItems: 'flex-end', gap: 18, height: 300}}>
            {[0.4, 0.7, 0.5, 0.9, 0.6, 1].map((v, i) => {
              const g = sp(f, 24 + i * 3, {damping: 14, stiffness: 140});
              return <div key={i} style={{width: 50, height: 300 * v * g, borderRadius: 8, background: i === 5 ? C.coral : C.mute, opacity: i === 5 ? 1 : 0.55}} />;
            })}
          </div>
        </>
      ),
    },
  ];

  return (
    <AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 40%, ${C.deep} 0%, ${C.navy} 70%)`, perspective: 1800}}>
      {/* suelo en perspectiva */}
      <div
        style={{
          position: 'absolute',
          left: -1000,
          top: 640,
          width: 3920,
          height: 1600,
          transform: 'rotateX(78deg)',
          transformOrigin: 'top',
          backgroundImage: `linear-gradient(${C.mute}33 2px, transparent 2px), linear-gradient(90deg, ${C.mute}33 2px, transparent 2px)`,
          backgroundSize: '120px 120px',
          backgroundPosition: `0 ${f * 4}px`,
          opacity: enter,
        }}
      />
      <AbsoluteFill style={{transformStyle: 'preserve-3d', transform: `translate(${sh.x}px, ${sh.y}px) translateZ(${dolly}px) rotateX(6deg) rotateY(${orbit}deg)`}}>
        {cards.map((c, i) => {
          const a = (i - 1) * 42;
          const fly = ease(f, 98 + (2 - i) * 4, 116 + (2 - i) * 4, [0, 1], IN);
          const pop = sp(f, 4 + i * 6, {damping: 16, stiffness: 110});
          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: 960 - 260,
                top: 540 - 310,
                transformStyle: 'preserve-3d',
                transform: `rotateY(${a}deg) translateZ(${520 + fly * 2400}px) translateY(${(1 - pop) * 500}px)`,
                filter: `blur(${fly * 12}px)`,
                opacity: pop,
              }}
            >
              <Card accent={c.accent}>{c.body}</Card>
            </div>
          );
        })}
      </AbsoluteFill>
      <SectionLabel n="04" title="Profundidad 3D" />
    </AbsoluteFill>
  );
};
