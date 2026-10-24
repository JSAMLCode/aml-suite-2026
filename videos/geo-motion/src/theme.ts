import {Easing, interpolate, spring} from 'remotion';

export const C = {
  navy: '#0A1128',
  navy2: '#111B3D',
  deep: '#1F306A',
  gold: '#D9B26A',
  goldL: '#F2CF86',
  goldD: '#A87C36',
  cream: '#FFF3CF',
  white: '#F4F6FB',
  mute: '#8E9AB8',
  teal: '#38D9C8',
  coral: '#FF4D6A',
};

export const FONT = "'Nunito Sans', sans-serif";
export const FPS = 30;

export const OUT = Easing.bezier(0.16, 1, 0.3, 1);
export const IN = Easing.bezier(0.7, 0, 0.84, 0);
export const INOUT = Easing.bezier(0.65, 0, 0.35, 1);

export const sp = (
  frame: number,
  delay = 0,
  config: Partial<{damping: number; stiffness: number; mass: number}> = {},
) => spring({frame: frame - delay, fps: FPS, config: {damping: 200, ...config}});

export const ease = (
  frame: number,
  from: number,
  to: number,
  out: [number, number] = [0, 1],
  easing = OUT,
) =>
  interpolate(frame, [from, to], out, {
    easing,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

// Sacudida amortiguada que arranca en `at`
export const shake = (frame: number, at: number, amp = 18, len = 14) => {
  const t = frame - at;
  if (t < 0 || t > len) return {x: 0, y: 0};
  const k = Math.exp(-t / (len / 4));
  return {x: Math.sin(t * 2.7) * amp * k, y: Math.cos(t * 3.3) * amp * 0.6 * k};
};

export const gold = `linear-gradient(135deg, ${C.goldL} 0%, ${C.gold} 45%, ${C.goldD} 100%)`;
