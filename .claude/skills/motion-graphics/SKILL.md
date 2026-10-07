---
name: motion-graphics
description: Crea piezas de motion graphics en Remotion con el sistema visual de Serrano Lawyers / SELENE (navy, oro, Nunito Sans, HUD de sala de edición, cortes a 120 BPM y partitura sintetizada sincronizada). Úsala cada vez que pidan un motion graphics, showreel, explainer animado, intro, cierre de marca o animación de datos.
---

# motion-graphics

Plantilla de referencia: `videos/motion-showreel/`. Es el diseño aprobado por el
cliente. Toda pieza nueva parte de ahí y respeta este sistema; solo cambia el
contenido de las escenas.

## Arranque

1. Copia la plantilla sin dependencias ni renders:
   `rsync -a --exclude node_modules --exclude out videos/motion-showreel/ videos/<slug>/`
   y luego `cd videos/<slug> && npm install`.
2. Navegador: `remotion.config.ts` ya apunta a
   `/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`
   con `swangle`. No descargues Chrome.
3. Antes de escribir escenas, fija con el usuario: guion o mensaje, duración,
   formato (16:9 o 9:16), marca del cierre (SELENE, Serrano Lawyers &
   Consultants o Procompliance) y la escena de datos (qué cifras son reales).
   No inventes cifras regulatorias: si no hay datos, márcalos como ilustrativos.

## Sistema visual (no negociable)

- Paleta (`src/theme.ts`): navy `#0A1128`, navy2 `#111B3D`, deep `#1F306A`,
  oro `#D9B26A` / `#F2CF86` / `#A87C36`, crema `#FFF3CF`, blanco `#F4F6FB`,
  mute `#8E9AB8`, teal `#38D9C8` (bajo/positivo), coral `#FF4D6A` (alerta).
  Gradiente oro a 135° para titulares clave.
- Tipografía: Nunito Sans local (`public/fonts`, cargada con `delayRender` en
  `src/fonts.ts`). Titulares 900, rótulos 700 en mayúsculas con tracking 4–10.
- Capas globales: `Vignette`, `Grain` (feTurbulence con semilla por fotograma),
  `EditorHud` (esquinas de zona segura, timecode, punto REC) y `SectionLabel`
  ("NN — Título", barra dorada que se estira y texto que sube por máscara).
- Fondo siempre navy; el oro es acento, nunca fondo salvo en un golpe de
  inversión de color de menos de 1 s.

## Ritmo y estructura

- 30 fps, 120 BPM: 1 pulso = 15 fotogramas. Todo corte cae en múltiplo de 15.
  Los cortes viven en `CUTS` de `theme.ts`; las escenas usan tiempo local.
- Estructura base de 30 s (900 f), adaptable:
  apertura (90) → tipografía cinética (120) → geometría/morph (120) →
  datos (150) → 3D (120) → transición zoom-through (90) → resolución de marca (210).
- Bookend: la pieza abre con una línea que colapsa en un punto dorado y cierra
  con el anillo colapsando en el mismo punto.
- Cada escena termina en una salida motivada que enlaza con la siguiente
  (match cut, forma que crece hasta ser el fondo, tarjetas que pasan la cámara,
  zoom a través de una letra). Destellos `Flash` de 2+6 fotogramas en cortes duros.

## Reglas de animación

- Nada aparece: todo llega. `spring` (`sp()`) para entradas, `ease()` con
  `OUT`/`IN`/`INOUT` (béziers de `theme.ts`) para movimientos. Sin fundidos planos.
- Golpes: escala 3→1 con muelle rígido + `shake()` amortiguada + onda expansiva.
- Todo depende solo del fotograma. Aleatoriedad solo con `random('semilla')`
  de Remotion; jamás `Math.random` ni estado entre fotogramas.
- La imagen enseña, no repite: rotula datos (cifras, sellos, escalas), no frases
  que ya dice la voz o el titular.
- Profundidad: eco en contorno (`WebkitTextStroke`) con retardo, parallax,
  `perspective` + `preserve-3d`.

## Recetas probadas (y sus trampas)

- Morph entre formas distintas: NO uses `interpolatePath` de `@remotion/paths`
  (retuerce triángulo↔hexágono↔estrella). Muestrea cada forma con
  `getPointAtLength` (144 puntos), alinea el punto de arranque con la forma
  anterior por mínima distancia e interpola punto a punto (ver `S3Shapes.tsx`).
- Zoom-through en una letra: cajas de ancho conocido por letra (`WIDTHS`),
  la "O" como anillo SVG; `transform-origin` en su centro, escala exponencial
  hasta ×90 y traslación al centro de pantalla. Ajusta `WIDTHS` midiendo el
  fotograma, nunca a ojo.
- Tarjetas 3D: en fila (x = ±600, z distinto, rotateY ±22°), no en carrusel
  cerrado: en carrusel se atraviesan.
- Matriz de riesgo 5×5: puntuación = probabilidad × impacto, color
  teal→oro→coral con `interpolateColors`, entrada en diagonal, barrido de
  escáner y alerta pulsante en la celda crítica. Es la escena de marca para
  piezas AML/KYC.
- Curvas: `evolvePath` para el trazo, `clipPath` para el área, marcador con
  valor que sigue la cabeza (`getPointAtLength` puede devolver null: usa `??`).
- Logotipo final: partículas que convergen en un anillo elíptico (rx = 1,55·ry)
  para que quepa el texto; tracking 56→20, brillo que barre el gradiente oro.

## Sonido

- `score.py` (numpy + scipy) genera `public/score.wav`: 120 BPM, La menor
  (Am–F–C–G), apertura con dron e impacto, groove con sidechain, silencio antes
  de la resolución, impacto + campanas en el logotipo.
- Cada acento se ancla con `fr(fotograma)` a un evento visible. Si mueves un
  evento en el vídeo, mueve su acento en `score.py`. Sin evento, sin sonido.
- No puedes oír el resultado: entrégalo diciendo que el balance lo valida el
  usuario. No afines a oído; evita lo dudoso.

## Verificación antes de entregar

1. `npx tsc -p .` sin errores.
2. Fotogramas sueltos con un solo bundle:
   `OUTDIR=out/rN node review.mjs 30 60 90 ...` (usa una carpeta nueva por
   ronda; no borres con globs relativos).
3. Hoja de contactos: `./sheet.sh video.mp4 out/sheet.png f1 f2 ...` o
   `ffmpeg ... tile=4xN` sobre los PNG. Revisa cada transición en su
   fotograma central y cada golpe en su fotograma de impacto.
4. Busca: texto que invade formas, elementos fuera del 14–88 % vertical,
   formas que se retuercen, solapes en 3D, cifras mal formateadas.
5. Render final en segundo plano con timeout largo (≥ 60 min):
   `npx remotion render src/index.ts Showreel out/<Nombre>_16x9.mp4 --concurrency=<núcleos> --crf=18`
   (`--concurrency` no puede superar los núcleos; ~1 s por fotograma con 4).
6. Hoja de contactos del MP4 final, commit + push del código y del MP4, y
   envía el vídeo al usuario.

## Vertical 9:16

Las escenas están compuestas en coordenadas de 1920×1080. Para 9:16 crea una
composición 1080×1920 y reencuadra cada escena (apilar en vez de alinear en
fila, tipografía ~0,75×, matriz arriba y KPIs abajo). No escales el 16:9.
