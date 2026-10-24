import React from 'react';
import {AbsoluteFill, interpolateColors, useCurrentFrame} from 'remotion';
import {evolvePath, getLength, getPointAtLength} from '@remotion/paths';
import {C, FONT, IN, INOUT, ease, sp} from '../theme';
import {SectionLabel} from '../ui';

const CELL = 112;
const GAP = 12;
const GX = 210;
const GY = 268;
const ALERT = {row: 4, col: 4};
const ALERT_AT = 72;

const riskColor = (score: number) =>
  interpolateColors(score, [1, 6, 12, 25], [C.teal, '#2B7F95', C.gold, C.coral]);

const fmt = (n: number) => Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');

// Serie de alertas mensuales (datos fijos)
const SERIES = [18, 22, 19, 27, 24, 31, 29, 38, 35, 44, 41, 52];
const CW = 780;
const CH = 300;
const CX = 1000;
const CY = 540;
const pts = SERIES.map((v, i) => [CX + (i * CW) / (SERIES.length - 1), CY + CH - ((v - 10) / 45) * CH]);
const LINE = pts
  .map(([x, y], i) => {
    if (i === 0) return `M ${x} ${y}`;
    const [px, py] = pts[i - 1];
    const mx = (px + x) / 2;
    return `C ${mx} ${py} ${mx} ${y} ${x} ${y}`;
  })
  .join(' ');
const LEN = getLength(LINE);

export const S4Data: React.FC = () => {
  const f = useCurrentFrame();
  const exit = ease(f, 132, 150, [0, 1], IN);
  const scan = ease(f, 46, 72, [0, 1], INOUT);
  const scanX = GX - 40 + scan * (5 * CELL + 4 * GAP + 80);

  const draw = ease(f, 36, 104, [0, 1], INOUT);
  const head = getPointAtLength(LINE, Math.max(0.01, LEN * draw)) ?? {x: CX, y: CY + CH};
  const evo = evolvePath(draw, LINE);
  const headVal = 10 + ((CY + CH - head.y) / CH) * 45;

  const kpi1 = ease(f, 18, 84, [0, 12480], INOUT);
  const kpi2 = ease(f, 26, 84, [0, 37], INOUT);
  const right = sp(f, 10, {damping: 22, stiffness: 120});

  return (
    <AbsoluteFill style={{background: C.navy2, fontFamily: FONT}}>
      {/* matriz de riesgo 5x5 */}
      {Array.from({length: 25}).map((_, k) => {
        const row = Math.floor(k / 5); // 0 = probabilidad baja (abajo)
        const col = k % 5;
        const score = (row + 1) * (col + 1);
        const x = GX + col * (CELL + GAP);
        const y = GY + (4 - row) * (CELL + GAP);
        const d = (row + col) * 3 + 6;
        const s = sp(f, d, {damping: 11, stiffness: 160});
        const sOut = ease(f, 132 + (8 - row - col), 142 + (8 - row - col), [0, 1], IN);
        const lit = scan > 0 && scanX > x + CELL / 2 ? 1 : 0;
        const isAlert = row === ALERT.row && col === ALERT.col;
        return (
          <div
            key={k}
            style={{
              position: 'absolute',
              left: x,
              top: y,
              width: CELL,
              height: CELL,
              borderRadius: 14,
              background: riskColor(score),
              opacity: 0.35 + 0.65 * Math.max(lit, f > ALERT_AT ? 1 : 0.4),
              transform: `scale(${s * (1 - sOut)})`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: C.navy,
              fontSize: 34,
              fontWeight: 800,
              boxShadow: isAlert && f > ALERT_AT ? `0 0 40px ${C.coral}` : undefined,
            }}
          >
            {score}
          </div>
        );
      })}

      {/* barrido del escáner */}
      {scan > 0 && scan < 1 && (
        <div style={{position: 'absolute', left: scanX, top: GY - 30, width: 4, height: 5 * CELL + 4 * GAP + 60, background: C.goldL, boxShadow: `0 0 30px 8px ${C.gold}`, opacity: 0.9}} />
      )}

      {/* alerta en la celda crítica */}
      {f >= ALERT_AT && (
        <svg width="1920" height="1080" style={{position: 'absolute', opacity: 1 - exit}}>
          {[0, 18, 36].map((o) => {
            const t = ((f - ALERT_AT + o) % 54) / 54;
            const cx = GX + 4 * (CELL + GAP) + CELL / 2;
            const cy = GY + CELL / 2;
            return <rect key={o} x={cx - CELL / 2 - t * 50} y={cy - CELL / 2 - t * 50} width={CELL + t * 100} height={CELL + t * 100} rx={14 + t * 20} fill="none" stroke={C.coral} strokeWidth={4} opacity={1 - t} />;
          })}
        </svg>
      )}
      {(() => {
        const t = sp(f, ALERT_AT + 2, {damping: 14, stiffness: 200});
        return (
          <div
            style={{
              position: 'absolute',
              left: GX + 4 * (CELL + GAP) - 40,
              top: GY - 92,
              padding: '10px 20px',
              borderRadius: 10,
              background: C.coral,
              color: C.white,
              fontSize: 22,
              fontWeight: 800,
              letterSpacing: 3,
              transform: `translateY(${(1 - t) * 30}px) scale(${t})`,
              opacity: (f > ALERT_AT ? 1 : 0) * (1 - exit),
              whiteSpace: 'nowrap',
            }}
          >
            ALERTA · 25 / 25
          </div>
        );
      })()}

      {/* ejes */}
      <div style={{position: 'absolute', left: GX, top: GY + 5 * CELL + 4 * GAP + 22, color: C.mute, fontSize: 20, fontWeight: 700, letterSpacing: 6, opacity: ease(f, 20, 34) * (1 - exit)}}>IMPACTO →</div>
      <div style={{position: 'absolute', left: GX - 60, top: GY + 5 * CELL + 4 * GAP, transform: 'rotate(-90deg)', transformOrigin: '0 0', color: C.mute, fontSize: 20, fontWeight: 700, letterSpacing: 6, opacity: ease(f, 20, 34) * (1 - exit)}}>PROBABILIDAD →</div>

      {/* panel derecho */}
      <div style={{position: 'absolute', inset: 0, transform: `translateX(${(1 - right) * 300 + exit * 400}px)`, opacity: right * (1 - exit)}}>
        <div style={{position: 'absolute', left: CX, top: 262, display: 'flex', gap: 80}}>
          <div>
            <div style={{color: C.mute, fontSize: 20, fontWeight: 700, letterSpacing: 4}}>CLIENTES EVALUADOS</div>
            <div style={{color: C.white, fontSize: 104, fontWeight: 900, fontVariantNumeric: 'tabular-nums', lineHeight: 1.1}}>{fmt(kpi1)}</div>
          </div>
          <div>
            <div style={{color: C.mute, fontSize: 20, fontWeight: 700, letterSpacing: 4}}>ALERTAS</div>
            <div style={{color: C.coral, fontSize: 104, fontWeight: 900, fontVariantNumeric: 'tabular-nums', lineHeight: 1.1}}>{Math.round(kpi2)}</div>
          </div>
        </div>

        <svg width="1920" height="1080" style={{position: 'absolute', left: 0, top: 0}}>
          <defs>
            <linearGradient id="area" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0" stopColor={C.gold} stopOpacity={0.45} />
              <stop offset="1" stopColor={C.gold} stopOpacity={0} />
            </linearGradient>
            <clipPath id="reveal">
              <rect x={CX} y={CY - 40} width={Math.max(0, head.x - CX)} height={CH + 60} />
            </clipPath>
          </defs>
          {[0, 1, 2, 3].map((g) => (
            <line key={g} x1={CX} x2={CX + CW * ease(f, 24 + g * 3, 44 + g * 3)} y1={CY + (g * CH) / 3} y2={CY + (g * CH) / 3} stroke={C.mute} strokeOpacity={0.25} strokeWidth={2} />
          ))}
          <path d={`${LINE} L ${CX + CW} ${CY + CH} L ${CX} ${CY + CH} Z`} fill="url(#area)" clipPath="url(#reveal)" />
          <path d={LINE} fill="none" stroke={C.goldL} strokeWidth={6} strokeLinecap="round" strokeDasharray={evo.strokeDasharray} strokeDashoffset={evo.strokeDashoffset} />
          {draw > 0 && <circle cx={head.x} cy={head.y} r={11} fill={C.navy2} stroke={C.goldL} strokeWidth={5} />}
        </svg>
        {draw > 0 && (
          <div style={{position: 'absolute', left: head.x - 46, top: head.y - 66, width: 92, textAlign: 'center', padding: '6px 0', borderRadius: 8, background: C.white, color: C.navy, fontSize: 24, fontWeight: 900, fontVariantNumeric: 'tabular-nums'}}>
            {Math.round(headVal)}
          </div>
        )}
      </div>

      <div style={{opacity: 1 - exit}}>
        <SectionLabel n="03" title="Datos en movimiento" />
      </div>
    </AbsoluteFill>
  );
};
