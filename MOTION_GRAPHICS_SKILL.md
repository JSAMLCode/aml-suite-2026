# Skill de vídeo y Motion Graphics · Serrano Lawyers / SELENE

Paquete instalable con dos skills de Claude Code:

- **motion-graphics**: explainers, showreels e intros en Remotion con el
  sistema visual navy/oro, voz sincronizada palabra a palabra, banda sonora
  cinematográfica y exportación a 9:16, 16:9, 4:5 y 1:1. Incluye la plantilla
  completa (el explainer "Geolocalización inferencial" funcionando) y las
  recetas del showreel.
- **editar-video**: vídeos grabados a cámara en formato partido para Reels y TikTok.

## Instalación en otra sesión

1. Sube este archivo al repositorio (por ejemplo a la raíz) o adjúntalo en el chat.
2. Pídele a Claude: *"Instala las skills de MOTION_GRAPHICS_SKILL.md"*. Claude
   copia el instalador de abajo a un archivo y lo ejecuta:

```bash
python3 install_skills.py MOTION_GRAPHICS_SKILL.md .claude/skills     # por proyecto
python3 install_skills.py MOTION_GRAPHICS_SKILL.md ~/.claude/skills   # para todos tus proyectos
```

3. Commit y push de `.claude/skills/` para que la skill viaje con el repositorio.
   En sesiones en la nube, `~/.claude` se pierde al cerrar el contenedor: la
   instalación por proyecto es la que persiste.
4. Para el primer vídeo: *"Usa la skill motion-graphics para…"*. La skill
   arranca copiando `template/`, instala dependencias y fuentes, y pregunta guion,
   formatos, cierre, voz y datos antes de construir.

Requisitos que la skill instala o verifica: Node 18+, `npm install` (Remotion
4.0.533, @fontsource/nunito-sans), Python 3 con numpy y scipy, ffmpeg.

### Instalador (`install_skills.py`)

```python
import pathlib, re, sys
src = sys.argv[1]
dest = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else '.claude/skills')
txt = open(src, encoding='utf-8').read()
n = 0
for m in re.finditer(r'<!-- file: (.+?) -->\n````[^\n]*\n(.*?)\n````\n', txt, re.S):
    p = dest / m.group(1)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(m.group(2) + '\n', encoding='utf-8')
    n += 1
for sh in dest.glob('motion-graphics/template/*.sh'):
    sh.chmod(0o755)
print(f'{n} archivos instalados en {dest}')
```

## Contenido (44 archivos)

- `motion-graphics/SKILL.md`
- `editar-video/SKILL.md`
- `motion-graphics/template/package.json`
- `motion-graphics/template/remotion.config.ts`
- `motion-graphics/template/tsconfig.json`
- `motion-graphics/template/.gitignore`
- `motion-graphics/template/setup-fonts.sh`
- `motion-graphics/template/src/fonts.ts`
- `motion-graphics/template/src/index.ts`
- `motion-graphics/template/src/Root.tsx`
- `motion-graphics/template/src/Stage.tsx`
- `motion-graphics/template/src/Frame.tsx`
- `motion-graphics/template/src/theme.ts`
- `motion-graphics/template/src/tl.ts`
- `motion-graphics/template/src/ui.tsx`
- `motion-graphics/template/src/timeline.json`
- `motion-graphics/template/src/scenes/S1Fecha.tsx`
- `motion-graphics/template/src/scenes/S2Art53.tsx`
- `motion-graphics/template/src/scenes/S3Art14.tsx`
- `motion-graphics/template/src/scenes/S4Senales.tsx`
- `motion-graphics/template/src/scenes/S5Controles.tsx`
- `motion-graphics/template/src/scenes/S6Plazo.tsx`
- `motion-graphics/template/src/scenes/S7Pregunta.tsx`
- `motion-graphics/template/src/scenes/S8Fuente.tsx`
- `motion-graphics/template/script.json`
- `motion-graphics/template/LOCUCION.md`
- `motion-graphics/template/voice/README.md`
- `motion-graphics/template/align.py`
- `motion-graphics/template/timeline.py`
- `motion-graphics/template/score.py`
- `motion-graphics/template/review.mjs`
- `motion-graphics/template/sheet.sh`
- `motion-graphics/recipes/showreel/README.md`
- `motion-graphics/recipes/showreel/theme.ts`
- `motion-graphics/recipes/showreel/ui.tsx`
- `motion-graphics/recipes/showreel/Showreel.tsx`
- `motion-graphics/recipes/showreel/scenes/S1ColdOpen.tsx`
- `motion-graphics/recipes/showreel/scenes/S2Kinetic.tsx`
- `motion-graphics/recipes/showreel/scenes/S3Shapes.tsx`
- `motion-graphics/recipes/showreel/scenes/S4Data.tsx`
- `motion-graphics/recipes/showreel/scenes/S5Depth.tsx`
- `motion-graphics/recipes/showreel/scenes/S6ZoomThrough.tsx`
- `motion-graphics/recipes/showreel/scenes/S7Resolve.tsx`
- `motion-graphics/recipes/showreel/score.py`

---

<!-- file: motion-graphics/SKILL.md -->
````markdown
---
name: motion-graphics
description: Crea piezas de motion graphics y explainers animados en Remotion con el sistema visual de Serrano Lawyers / SELENE / Procompliance (navy y oro, Nunito Sans, HUD de sala de edición, cortes a 120 BPM, golpes sincronizados con la voz, banda sonora cinematográfica sintetizada y exportación a 9:16, 16:9, 4:5 y 1:1). Úsala cada vez que pidan un motion graphics, showreel, explainer, intro, cierre de marca, animación de datos o un vídeo para Reels, TikTok o LinkedIn.
---

# motion-graphics

Sistema probado y aprobado por el cliente en dos piezas: un showreel de 30 s y el
explainer "Geolocalización inferencial" (Acuerdo 1-2026 SBP). La plantilla
completa está en `template/` (junto a este archivo) y las recetas de escenas
sueltas en `recipes/`. Toda pieza nueva parte de ahí: solo cambia el contenido.

## 0. Arranque de un proyecto

```bash
SKILL=.claude/skills/motion-graphics          # o ~/.claude/skills/motion-graphics
mkdir -p videos/<slug> && cp -r $SKILL/template/. videos/<slug>/
cd videos/<slug> && npm install
bash setup-fonts.sh                           # copia Nunito Sans desde @fontsource a public/fonts
pip install numpy scipy                       # para align.py y score.py
python3 score.py && npx tsc -p . && OUTDIR=out/r1 node review.mjs 60 600 1200
```

- Navegador: `remotion.config.ts` y `review.mjs` usan el Chromium preinstalado
  (`/opt/pw-browsers/...headless_shell`) si existe; si no, Remotion descarga el suyo.
- No hay `rsync` en el contenedor de la nube: usa `cp -r` o `tar`.
- La plantilla trae el explainer de geolocalización como ejemplo funcionando
  (8 escenas + firma). Sustituye `src/scenes/*`, `script.json` y la voz.

## 1. Antes de construir: preguntar

No construyas con dudas abiertas. Fija con el usuario:
1. Guion o mensaje, y duración aproximada.
2. Formatos: 9:16 (Reels/TikTok), 16:9 (LinkedIn/YouTube), 4:5 (feed), 1:1.
3. Marca del cierre: SELENE, Serrano Lawyers & Consultants, Procompliance o la
   firma personal de José Antonio Serrano (con credenciales).
4. Voz: grabada por el usuario (lo más humano), o TTS (ver §6).
5. Datos: qué cifras son reales. Nunca inventes cifras regulatorias; si son
   ilustrativas, rotula "Esquema ilustrativo".

## 2. Sistema visual (no negociable)

- Paleta (`src/theme.ts`): navy `#0A1128`, navy2 `#111B3D`, deep `#1F306A`,
  oro `#D9B26A` / `#F2CF86` / `#A87C36`, crema `#FFF3CF`, blanco `#F4F6FB`,
  mute `#8E9AB8`, teal `#38D9C8` (bajo / positivo / validar), coral `#FF4D6A`
  (alerta / bloqueo / ocultación). Gradiente oro a 135° para titulares clave.
- Tipografía: Nunito Sans local, cargada con `delayRender` (`src/fonts.ts`).
  Titulares 900; rótulos 700 en mayúsculas con tracking 4–10.
- Capas: `Vignette`, `Grain` (feTurbulence con semilla por fotograma),
  `EditorHud` (esquinas, timecode, punto REC, firma), `SectionLabel`
  ("NN — Título": barra dorada que se estira y texto que sube por máscara),
  `Source` (nota de fuente al pie: obligatoria en toda escena normativa).
- Fondo siempre navy. El oro es acento; solo puede ser fondo en un golpe de
  inversión de color de menos de 1 s.
- Zona segura: nada importante por encima del 14 % ni por debajo del 88 % de
  la altura del escenario.

## 3. Ritmo y estructura

- 30 fps y 120 BPM: 1 pulso = 15 fotogramas. Todo corte cae en un múltiplo de 15.
- Showreel (sin voz), 30 s: apertura (90 f) → tipografía cinética (120) →
  geometría/morph (120) → datos (150) → 3D (120) → zoom-through (90) →
  resolución de marca (210). Recetas en `recipes/showreel/`.
- Explainer (con voz): una escena por frase; el tramo de cada escena va desde
  su frase hasta la siguiente (`span(id)`).
- Bookend: abre con una línea dorada que colapsa en un punto y cierra con el
  anillo de partículas colapsando en el mismo punto.
- Cada escena sale de forma motivada hacia la siguiente: match cut, forma que
  crece hasta ser el fondo, tarjetas que pasan la cámara, zoom a través de una
  letra. Destellos `Flash` (2 + 6 fotogramas) en cortes duros.

## 4. Reglas de animación

- Nada aparece: todo llega. `sp()` (spring) para entradas; `ease()` con
  `OUT` / `IN` / `INOUT` (béziers de `theme.ts`) para movimientos. Sin fundidos planos.
- Golpe (`Slam`): escala 3→1 con muelle rígido + `shake()` amortiguada + onda
  expansiva + eco en contorno.
- Sello (`Stamp`): cae girado con muelle rígido; para "PLAZO LÍMITE",
  "VERIFICADO", "FUENTE PRIMARIA…".
- Cada golpe cae en la palabra que lo nombra: `wf('03', 'catorce')`.
- La imagen enseña, no repite: rotula datos (cifras, sellos, escalas), no la
  frase que dice la voz.
- Todo depende solo del fotograma. Aleatoriedad solo con `random('semilla')`
  de Remotion; nunca `Math.random` ni estado entre fotogramas.
- Pantallas quietas: solo se mueve lo que entra.
- Hooks de React siempre al principio del componente, nunca dentro de JSX condicional.

## 5. Recetas probadas y sus trampas

| Receta | Archivo | Trampa evitada |
|---|---|---|
| Morph entre formas | `recipes/showreel/S3Shapes.tsx` | `interpolatePath` retuerce triángulo↔hexágono↔estrella: muestrea 144 puntos con `getPointAtLength`, alinea el arranque por mínima distancia e interpola punto a punto |
| Zoom-through en una letra | `recipes/showreel/S6ZoomThrough.tsx`, `template/src/scenes/S7Pregunta.tsx` | La "O" es un anillo SVG en una caja de ancho conocido; escala exponencial ×70–90 sobre su centro y traslación al centro de pantalla. Mide los anchos en el fotograma, nunca a ojo |
| Tarjetas 3D | `recipes/showreel/S5Depth.tsx` | En fila (x = ±600, z distinto, rotateY ±22°), no en carrusel cerrado: en carrusel se atraviesan |
| Matriz de riesgo 5×5 | `recipes/showreel/S4Data.tsx` | Probabilidad × impacto, color teal→oro→coral (`interpolateColors`), entrada en diagonal, escáner y alerta pulsante. Escena de marca para AML/KYC |
| Curvas y KPIs | `recipes/showreel/S4Data.tsx` | `evolvePath` para el trazo y `clipPath` para el área. `getPointAtLength` puede devolver null: usa `??` |
| Número de artículo | `template/src/scenes/S2Art53.tsx` | `Slam` gigante que luego se aparca arriba a la derecha escalando sobre un `transform-origin` calculado (o = (destino − s·centro)/(1 − s)), sin traslaciones |
| Nodos alrededor de un globo | `template/src/scenes/S4Senales.tsx` | Elipse rx 330 / ry 290; cada nodo sale del centro con su palabra; contador n/8; paquetes que vuelven al centro al resolver |
| Flujo con ramas | `template/src/scenes/S5Controles.tsx` | Conectores bezier con `evolvePath`; rama teal (validar) y coral (frenar) |
| Cronograma | `template/src/scenes/S6Plazo.tsx` | Cursor HOY que avanza; barras con muelle; etiqueta "Esquema ilustrativo, duraciones no a escala" |
| Firma con partículas | `template/src/scenes/S8Fuente.tsx` (`S9Firma`) | Anillo elíptico (rx = 1,38–1,55·ry) para que quepa el nombre; tracking que se cierra; brillo que barre el oro |

## 6. Voz y sincronía

- Lo más humano es la voz del propio usuario. Entrégale el guion con pausas
  marcadas (`/` corta 0,3 s, `//` respiración 0,7 s, **negrita** para énfasis),
  como en `template/LOCUCION.md`. Archivos `voice/01.wav` … `NN.wav`.
- TTS: ElevenLabs (requiere clave y permitir `api.elevenlabs.io` en la red del
  entorno) o Higgsfield `generate_audio` (`text2speech_v2`, variante
  `elevenlabs`; consume créditos). Huggingface suele estar bloqueado: no hay
  Kokoro ni Whisper locales.
- Siglas: que la voz diga el nombre completo ("Superintendencia de Bancos de
  Panamá") y la pantalla muestre nombre y sigla. Números: "uno dos mil
  veintiséis", sin "guion".
- `align.py` saca tiempos por palabra sin Whisper: RMS de 10 ms, anclas en
  pausas (oraciones → comas → palabras por sílabas). Fronteras de oración
  ±30 ms; palabras ±150 ms. Si Whisper está disponible, úsalo.
- `timeline.py` coloca cada frase en el siguiente pulso con ≥ 0,3 s de respiro
  y escribe `src/timeline.json`, que leen vídeo, subtítulos y música.
- `wf(id, 'palabra', nth)` da el fotograma local; acepta alternativas
  `'superintendencia|sbp'` para sobrevivir a cambios de guion. `cue()` en
  `score.py` hace el mismo cálculo.
- Tú no oyes el audio: lo que dependa del oído (balance, ritmo, empalmes) se
  entrega diciendo que lo valida el usuario.

## 7. Formatos de salida

`src/Stage.tsx` es el escenario de 1080×1080 con todas las escenas.
`src/Frame.tsx` lo coloca y añade marco por formato (`src/Root.tsx` registra
`Geo-1x1`, `Geo-4x5`, `Geo-9x16`, `Geo-16x9`):

| Formato | Composición |
|---|---|
| 9:16 1080×1920 (Reels) | Barras de progreso por capítulo + título arriba (y 170), escenario en y 360, subtítulos en y 1450 (fuera de los botones de Instagram). Sin HUD |
| 16:9 1920×1080 (LinkedIn) | Índice de capítulos a la izquierda, escenario centrado (x 420), subtítulos a la derecha, HUD completo |
| 4:5 1080×1350 (feed) | Escenario arriba, subtítulos debajo |
| 1:1 1080×1080 | Escenario solo, HUD |

Subtítulos palabra a palabra: la palabra que suena en oro, las dichas en
blanco y las que faltan al 35 %. El marco se retira al llegar a la firma.

## 8. Sonido

`score.py` (numpy + scipy) compone y mezcla en `public/mix.wav`:
- Cinematográfica, épica e inspiracional: 120 BPM, La menor con vi–IV–I–V
  (Am–F–C–G). Cuerdas en ensemble, spiccato en ostinato, metales, coro,
  piano, campanas, timbales, taikos, braams, sub drops, risers y platillo invertido.
- Arco anclado a la línea de tiempo: apertura íntima → ostinato → crescendo →
  tramo pleno con melodía de metales → tensión (reloj + redoble) → vacío en la
  pregunta → clímax en Do mayor en la firma.
- Cada acento se ancla con `cue(id, palabra)` a un evento visible. Sin evento,
  sin sonido.
- La música baja ~10 dB bajo la voz (envolvente de 150 ms). Sin saturación.
  Master con `loudnorm` a −14 LUFS / −1,5 dBTP.
- Sin voz (`voice/` vacío), genera solo música.
- Es síntesis, no orquesta grabada: si el usuario tiene una pista con licencia
  (Artlist, Epidemic), móntala y sincroniza los golpes con ella.

## 9. Verificación antes de entregar

1. `npx tsc -p .` sin errores.
2. Fotogramas sueltos con un solo bundle:
   `COMP=Geo-9x16 OUTDIR=out/rN node review.mjs 60 600 1200` (carpeta nueva
   por ronda; no borres con globs relativos: el guardián de `rm` lo bloquea).
3. Hojas de contactos (`sheet.sh` o `ffmpeg … tile=4xN`): cada transición en
   su fotograma central y cada golpe en su fotograma de impacto.
4. Busca: texto que invade formas, elementos fuera de la zona segura, formas
   que se retuercen, solapes en 3D, cifras mal formateadas, subtítulos desfasados.
5. Cuando algo se vea descentrado, mide los píxeles del fotograma; no ajustes a ojo.
6. Render en segundo plano con timeout largo (≥ 60 min por formato; ~1 s por
   fotograma con 4 núcleos; `--concurrency` ≤ núcleos):
   `npx remotion render src/index.ts Geo-9x16 out/<Nombre>_9x16.mp4 --concurrency=4 --crf=18`
7. Hoja de contactos y sonoridad del MP4 final (`ffmpeg -af ebur128`), commit +
   push y envío del vídeo al usuario.

## 10. Vídeos grabados (cara + animación)

Para vídeos con la persona a cámara, usa también la skill `editar-video`
(formato partido: animación arriba 806 px, cara abajo, 1080×1920).
````

<!-- file: editar-video/SKILL.md -->
````markdown
---
name: editar-video
description: Edita vídeos verticales para TikTok e Instagram montados en Remotion, con formato partido (animación arriba, cara abajo). Úsala cuando te pasen un vídeo grabado y pidan transcribir, cortar, subtitular, animar o exportar.
---

# editar-video

Un vídeo se monta como una lista de tramos. Cada tramo es un clip recortado,
sus palabras con tiempos y una escena de Remotion que pinta la animación.

## Flujo

1. **Audio.** Extrae siempre la primera pista:
   `ffmpeg -nostdin -y -i INPUT.MOV -map 0:a:0 -ac 1 -ar 16000 audio.wav`
   (los MOV de iPhone traen una segunda pista espacial que no sirve).
2. **Transcribe por palabras** con faster-whisper large-v3 y marcas por palabra.
   Corrige nombres de producto antes de cortar.
3. **Agrupa por pausas de más de 0,6 s.** Así se ven las tomas repetidas.
   Quédate con la última toma buena y retranscribe solo esas ventanas.
4. **Mide los bordes con RMS (ventanas de 10 ms), no con Whisper.**
   - Entrada: primer cruce sostenido de −47 dB, menos 0,12 s. En el primer
     tramo del vídeo, menos 0,02 s: la voz debe empezar en el segundo 0.
   - Salida: donde el RMS baja de −50 dB, más 0,14–0,35 s de cola.
   - Revisa también la última sílaba: puede llegar 0,2 s más allá de lo
     que marca la transcripción.
5. **Corta cada tramo** a 1080x1920 y 30 fps y guarda un JSON con las palabras
   relativas al inicio del tramo (`id`, `dur`, `mode`, `words`).
6. **Pregunta antes de construir** si hay algo por decidir: el gancho, el
   cierre, qué va a pantalla completa. No construyas con dudas abiertas.
7. **Escribe una escena por tramo** y regístrala en la composición.
8. **Renderiza y revisa fotogramas** (hoja de contactos y recortes a tamaño
   real) antes de enseñar nada.

## Formatos de tramo

- `split`: lienzo blanco arriba (806 px) con la animación; la cara abajo.
- `full`: blanco entero. Una sola idea clave por vídeo.
- `face`: solo la cara, para el cierre.

## Reglas de animación

- **Nada aparece: todo llega.** Entradas con muelle (`spring`), movimientos con
  curvas de easing, reacciones con onda y sacudida. Sin fundidos planos.
- **La imagen enseña, no repite.** No pongas chips que digan lo mismo que la
  voz. Rotula solo datos: horas, cantidades, sellos.
- **Cada golpe cae en la palabra que lo nombra.** Lee los tiempos del JSON.
- **Todo depende solo del tiempo.** Sin `Math.random`, sin estado entre
  fotogramas.
- **Personajes y decorado con continuidad.** El problema y el resultado pasan
  en el mismo escenario.
- **Pantallas completas quietas.** Solo se mueven los elementos que entran.

## Subtítulos y zona segura

- Blancos y planos sobre el vídeo, en negro sobre fondos claros. Sin placa.
- Nada importante por encima del 14 % ni por debajo del 88 % de la altura.

## Sonido

Efectos cortos (pop, tick, ping) solo cuando confirman algo visible, muy por
debajo de la voz. Si un sonido no tiene evento en pantalla, quítalo.

## Cuando algo se ve descentrado

Mide los píxeles del fotograma renderizado. No ajustes la constante a ojo.

## Lo que no se puede verificar

Tú no oyes el audio. Lo que dependa del oído (empalmes, ritmo, tono) no se da
por bueno: se evita, no se afina. No empalmes dos tomas dentro de un sintagma.
````

<!-- file: motion-graphics/template/package.json -->
````json
{
  "name": "motion-template",
  "private": true,
  "scripts": {
    "studio": "remotion studio",
    "music": "python3 score.py",
    "r:9x16": "remotion render src/index.ts Geo-9x16 out/video_9x16.mp4 --crf=18",
    "r:16x9": "remotion render src/index.ts Geo-16x9 out/video_16x9.mp4 --crf=18",
    "r:4x5": "remotion render src/index.ts Geo-4x5 out/video_4x5.mp4 --crf=18",
    "r:1x1": "remotion render src/index.ts Geo-1x1 out/video_1x1.mp4 --crf=18"
  },
  "dependencies": {
    "@remotion/bundler": "4.0.533",
    "@remotion/cli": "4.0.533",
    "@remotion/noise": "4.0.533",
    "@remotion/paths": "4.0.533",
    "@remotion/renderer": "4.0.533",
    "@remotion/shapes": "4.0.533",
    "react": "18.3.1",
    "react-dom": "18.3.1",
    "remotion": "4.0.533",
    "@fontsource/nunito-sans": "5.3.0"
  },
  "devDependencies": {
    "@types/react": "18.3.12",
    "typescript": "5.6.3"
  }
}
````

<!-- file: motion-graphics/template/remotion.config.ts -->
````ts
import fs from 'node:fs';
import {Config} from '@remotion/cli/config';

Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(92);
Config.setOverwriteOutput(true);
// Chromium preinstalado en los contenedores de Claude Code; si no existe, Remotion descarga el suyo
const CHROME = '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell';
if (fs.existsSync(CHROME)) Config.setBrowserExecutable(CHROME);
Config.setChromiumOpenGlRenderer('swangle');
````

<!-- file: motion-graphics/template/tsconfig.json -->
````json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "strict": true,
    "skipLibCheck": true,
    "noEmit": true,
    "resolveJsonModule": true
  },
  "include": ["src"]
}
````

<!-- file: motion-graphics/template/.gitignore -->
````
node_modules
out/*
!out/*.mp4
.cache
public/fonts/*.woff2
````

<!-- file: motion-graphics/template/setup-fonts.sh -->
````bash
#!/bin/bash
# Copia Nunito Sans (paquete npm @fontsource/nunito-sans) a public/fonts
set -e
cd "$(dirname "$0")"
mkdir -p public/fonts
for w in 300 400 600 700 800 900; do
  cp node_modules/@fontsource/nunito-sans/files/nunito-sans-latin-$w-normal.woff2 public/fonts/
done
echo "fuentes listas en public/fonts"
````

<!-- file: motion-graphics/template/src/fonts.ts -->
````ts
import {continueRender, delayRender, staticFile} from 'remotion';

const weights: [number, string][] = [300, 400, 600, 700, 800, 900].map((w) => [w, `nunito-sans-latin-${w}-normal.woff2`]);

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
````

<!-- file: motion-graphics/template/src/index.ts -->
````tsx
import {registerRoot} from 'remotion';
import {Root} from './Root';

registerRoot(Root);
````

<!-- file: motion-graphics/template/src/Root.tsx -->
````tsx
import React from 'react';
import {Composition} from 'remotion';
import {Frame, Fmt} from './Frame';
import {TL} from './tl';
import {FPS} from './theme';

const FORMATS: {id: string; fmt: Fmt; w: number; h: number}[] = [
  {id: 'Geo-1x1', fmt: '1x1', w: 1080, h: 1080},
  {id: 'Geo-4x5', fmt: '4x5', w: 1080, h: 1350},
  {id: 'Geo-9x16', fmt: '9x16', w: 1080, h: 1920},
  {id: 'Geo-16x9', fmt: '16x9', w: 1920, h: 1080},
];

export const Root: React.FC = () => (
  <>
    {FORMATS.map((c) => (
      <Composition key={c.id} id={c.id} component={Frame} defaultProps={{fmt: c.fmt}} durationInFrames={TL.end} fps={FPS} width={c.w} height={c.h} />
    ))}
  </>
);
````

<!-- file: motion-graphics/template/src/Stage.tsx -->
````tsx
import React from 'react';
import {AbsoluteFill, Sequence} from 'remotion';
import {C} from './theme';
import {loadFonts} from './fonts';
import {TL, span} from './tl';
import {Flash} from './ui';
import {S0Open, S1Fecha} from './scenes/S1Fecha';
import {S2Art53} from './scenes/S2Art53';
import {S3Art14} from './scenes/S3Art14';
import {S4Senales} from './scenes/S4Senales';
import {S5Controles} from './scenes/S5Controles';
import {S6Plazo} from './scenes/S6Plazo';
import {S7Pregunta} from './scenes/S7Pregunta';
import {S8Fuente, S9Firma} from './scenes/S8Fuente';

loadFonts();

// Escenario 1080×1080: todas las escenas. Cada formato lo coloca y le añade su marco.

const SCENES: [string, React.FC][] = [
  ['01', S1Fecha],
  ['02', S2Art53],
  ['03', S3Art14],
  ['04', S4Senales],
  ['05', S5Controles],
  ['06', S6Plazo],
  ['07', S7Pregunta],
  ['08', S8Fuente],
];

export const Stage: React.FC = () => (
  <AbsoluteFill style={{background: C.navy, overflow: 'hidden'}}>
    <Sequence durationInFrames={TL.open}>
      <S0Open />
    </Sequence>
    {SCENES.map(([id, Scene]) => (
      <Sequence key={id} from={span(id).from} durationInFrames={span(id).len}>
        <Scene />
      </Sequence>
    ))}
    <Sequence from={TL.sign} durationInFrames={TL.end - TL.sign}>
      <S9Firma />
    </Sequence>

    {['02', '03', '04', '05', '06', '07'].map((id) => (
      <Flash key={id} at={span(id).from} max={0.35} />
    ))}

  </AbsoluteFill>
);
````

<!-- file: motion-graphics/template/src/Frame.tsx -->
````tsx
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
````

<!-- file: motion-graphics/template/src/theme.ts -->
````tsx
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
````

<!-- file: motion-graphics/template/src/tl.ts -->
````tsx
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
// Acepta alternativas ('sbp|superintendencia') para que la escena sobreviva a un cambio de guion
export const wf = (id: string, word: string, nth = 0) => {
  for (const alt of word.split('|')) {
    const hits = line(id).words.filter((w) => norm(w.w).startsWith(norm(alt)));
    if (hits[nth]) return hits[nth].f;
  }
  throw new Error(`"${word}" no está en la frase ${id}`);
};

export const CHAPTERS: Record<string, string> = {
  '01': 'El plazo',
  '02': 'Artículo 53',
  '03': 'Artículo 14',
  '04': 'Las señales',
  '05': 'Para qué sirve',
  '06': 'Nueve meses',
  '07': 'La pregunta',
  '08': 'Fuente',
};

// Tramo de cada escena: desde su frase hasta la siguiente (o la firma)
export const span = (id: string) => {
  const i = TL.lines.findIndex((x) => x.id === id);
  const from = TL.lines[i].start;
  const to = i + 1 < TL.lines.length ? TL.lines[i + 1].start : TL.sign;
  return {from, len: to - from};
};
````

<!-- file: motion-graphics/template/src/ui.tsx -->
````tsx
import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, FONT, FPS, IN, ease, gold, shake, sp} from './theme';
import {H, W} from './tl';

// Rótulo de sección: barra dorada que se estira y texto que sube por máscara
export const SectionLabel: React.FC<{n: string; title: string; at?: number; out?: number}> = ({n, title, at = 4, out = 1}) => {
  const f = useCurrentFrame();
  const bar = ease(f, at, at + 14);
  const txt = ease(f, at + 4, at + 20);
  return (
    <div style={{position: 'absolute', left: 64, top: 92, fontFamily: FONT, display: 'flex', alignItems: 'center', gap: 16, opacity: out}}>
      <div style={{width: 48 * bar, height: 3, background: C.gold}} />
      <div style={{overflow: 'hidden', height: 28}}>
        <div style={{transform: `translateY(${(1 - txt) * 28}px)`, color: C.white, fontSize: 19, fontWeight: 700, letterSpacing: 5, textTransform: 'uppercase'}}>
          <span style={{color: C.gold}}>{n}</span>
          <span style={{opacity: 0.85}}> — {title}</span>
        </div>
      </div>
    </div>
  );
};

// Nota de fuente al pie: obligatoria en cada escena con contenido normativo
export const Source: React.FC<{text: string; at?: number; out?: number}> = ({text, at = 10, out = 1}) => {
  const f = useCurrentFrame();
  const o = ease(f, at, at + 14);
  return (
    <div style={{position: 'absolute', left: 64, top: 958, fontFamily: FONT, color: C.mute, fontSize: 15, fontWeight: 600, letterSpacing: 1, opacity: o * out * 0.9}}>
      {text}
    </div>
  );
};

// Palabras que llegan una a una por máscara, cada una en su fotograma
export const Words: React.FC<{
  words: {t: string; at: number; color?: string}[];
  size: number;
  weight?: number;
  align?: 'left' | 'center';
  width?: number;
  lh?: number;
}> = ({words, size, weight = 900, align = 'left', width = 952, lh = 1.12}) => {
  const f = useCurrentFrame();
  return (
    <div style={{width, display: 'flex', flexWrap: 'wrap', justifyContent: align === 'center' ? 'center' : 'flex-start', columnGap: size * 0.26, fontFamily: FONT}}>
      {words.map((w, i) => {
        const p = sp(f, w.at, {damping: 16, stiffness: 170});
        return (
          <div key={i} style={{overflow: 'hidden', height: size * lh, lineHeight: `${size * lh}px`}}>
            <div style={{transform: `translateY(${(1 - p) * size * 1.1}px)`, fontSize: size, fontWeight: weight, color: w.color ?? C.white, whiteSpace: 'nowrap'}}>{w.t}</div>
          </div>
        );
      })}
    </div>
  );
};

// Número gigante que cae con golpe: escala 3→1, sacudida y onda expansiva
export const Slam: React.FC<{text: string; at: number; size: number; x?: number; y: number; outline?: boolean}> = ({text, at, size, x = W / 2, y, outline}) => {
  const f = useCurrentFrame();
  const p = sp(f, at - 5, {damping: 12, stiffness: 260, mass: 0.6});
  const lag = sp(f, at, {damping: 20, stiffness: 90});
  const sh = shake(f, at, 16, 14);
  if (f < at - 5) return null;
  return (
    <>
      <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0, pointerEvents: 'none'}}>
        {[0, 7].map((d) => {
          const k = ease(f, at + d, at + d + 28);
          return k > 0 && k < 1 ? <circle key={d} cx={x} cy={y} r={size * 0.45 + k * 700} fill="none" stroke={C.gold} strokeWidth={8 * (1 - k)} opacity={1 - k} /> : null;
        })}
      </svg>
      {outline && (
        <div style={{position: 'absolute', left: x - 600, top: y - size * 0.6, width: 1200, textAlign: 'center', fontFamily: FONT, fontSize: size, fontWeight: 900, lineHeight: `${size * 1.2}px`, color: 'transparent', WebkitTextStroke: `2px ${C.gold}`, opacity: 0.5, transform: `translate(${18 + sh.x}px, ${14 + sh.y}px) scale(${1.15 - 0.15 * lag})`}}>
          {text}
        </div>
      )}
      <div
        style={{
          position: 'absolute',
          left: x - 600,
          top: y - size * 0.6,
          width: 1200,
          textAlign: 'center',
          fontFamily: FONT,
          fontSize: size,
          fontWeight: 900,
          lineHeight: `${size * 1.2}px`,
          backgroundImage: gold,
          WebkitBackgroundClip: 'text',
          color: 'transparent',
          transform: `translate(${sh.x}px, ${sh.y}px) scale(${3 - 2 * p})`,
          opacity: Math.min(1, p * 2),
        }}
      >
        {text}
      </div>
    </>
  );
};

// Sello que cae girado con muelle rígido
export const Stamp: React.FC<{text: string; at: number; color?: string; rot?: number; size?: number; style?: React.CSSProperties}> = ({text, at, color = C.coral, rot = -8, size = 30, style}) => {
  const f = useCurrentFrame();
  const p = sp(f, at - 5, {damping: 10, stiffness: 320, mass: 0.7});
  if (f < at - 5) return null;
  return (
    <div style={{position: 'absolute', padding: `${size * 0.3}px ${size * 0.6}px`, border: `${Math.max(3, size / 8)}px solid ${color}`, borderRadius: 10, color, fontFamily: FONT, fontSize: size, fontWeight: 900, letterSpacing: size * 0.12, whiteSpace: 'nowrap', transform: `rotate(${rot}deg) scale(${3 - 2 * p})`, opacity: Math.min(1, p * 2), ...style}}>
      {text}
    </div>
  );
};

const pad = (n: number) => String(n).padStart(2, '0');

// Capa de sala de edición: esquinas, timecode, punto REC y firma
export const EditorHud: React.FC<{offset?: number}> = ({offset = 0}) => {
  const {width: W, height: H} = useVideoConfig();
  const f = useCurrentFrame() + offset;
  const s = Math.floor(f / FPS);
  const tc = `00:${pad(Math.floor(s / 60))}:${pad(s % 60)}:${pad(f % FPS)}`;
  const on = ease(f - offset, 6, 24);
  const corner = (r: number, x: number, y: number) => (
    <div key={r} style={{position: 'absolute', left: x, top: y, width: 36, height: 36, borderTop: `2px solid ${C.mute}`, borderLeft: `2px solid ${C.mute}`, transform: `rotate(${r}deg)`, opacity: 0.45 * on}} />
  );
  const chrome: React.CSSProperties = {position: 'absolute', bottom: 46, color: C.mute, fontSize: 15, fontWeight: 600, letterSpacing: 3, opacity: 0.8 * on, fontFamily: FONT};
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {corner(0, 36, 36)}
      {corner(90, W - 72, 36)}
      {corner(180, W - 72, H - 72)}
      {corner(270, 36, H - 72)}
      <div style={{...chrome, left: 64, fontVariantNumeric: 'tabular-nums'}}>TC {tc}</div>
      <div style={{...chrome, right: 64, display: 'flex', alignItems: 'center', gap: 10}}>
        <div style={{width: 10, height: 10, borderRadius: 5, background: C.coral, opacity: Math.floor(f / 15) % 2 ? 0.35 : 1}} />
        J. A. SERRANO · AML · GRC
      </div>
    </AbsoluteFill>
  );
};

export const Grain: React.FC = () => {
  const {width: W, height: H} = useVideoConfig();
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{pointerEvents: 'none', mixBlendMode: 'overlay', opacity: 0.16}}>
      <svg width={W} height={H}>
        <filter id="g">
          <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed={f % 12} />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width={W} height={H} filter="url(#g)" />
      </svg>
    </AbsoluteFill>
  );
};

export const Vignette: React.FC = () => (
  <AbsoluteFill style={{pointerEvents: 'none', background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,0.55) 100%)'}} />
);

export const Flash: React.FC<{at: number; color?: string; max?: number}> = ({at, color = C.white, max = 0.6}) => {
  const f = useCurrentFrame();
  const o = f < at ? ease(f, at - 2, at, [0, max]) : ease(f, at, at + 6, [max, 0]);
  if (o <= 0) return null;
  return <AbsoluteFill style={{background: color, opacity: o, pointerEvents: 'none'}} />;
};

// Salida estándar de escena: empuje y desenfoque en los últimos fotogramas
export const useExit = (len: number, n = 12) => {
  const f = useCurrentFrame();
  return ease(f, len - n, len, [0, 1], IN);
};
````

<!-- file: motion-graphics/template/src/timeline.json -->
````json
{
 "fps": 30,
 "open": 45,
 "lines": [
  {
   "id": "01",
   "start": 45,
   "dur": 3.349,
   "words": [
    {
     "w": "Treinta",
     "f": 1
    },
    {
     "w": "de",
     "f": 13
    },
    {
     "w": "junio",
     "f": 18
    },
    {
     "w": "de",
     "f": 30
    },
    {
     "w": "dos",
     "f": 35
    },
    {
     "w": "mil",
     "f": 41
    },
    {
     "w": "veintisiete.",
     "f": 47
    },
    {
     "w": "Ese",
     "f": 70
    },
    {
     "w": "es",
     "f": 81
    },
    {
     "w": "el",
     "f": 87
    },
    {
     "w": "plazo.",
     "f": 91
    }
   ]
  },
  {
   "id": "02",
   "start": 165,
   "dur": 9.728,
   "words": [
    {
     "w": "El",
     "f": 1
    },
    {
     "w": "artículo",
     "f": 9
    },
    {
     "w": "cincuenta",
     "f": 32
    },
    {
     "w": "y",
     "f": 49
    },
    {
     "w": "tres",
     "f": 55
    },
    {
     "w": "obliga",
     "f": 61
    },
    {
     "w": "a",
     "f": 78
    },
    {
     "w": "los",
     "f": 84
    },
    {
     "w": "bancos",
     "f": 89
    },
    {
     "w": "que",
     "f": 101
    },
    {
     "w": "abren",
     "f": 106
    },
    {
     "w": "cuentas",
     "f": 116
    },
    {
     "w": "por",
     "f": 127
    },
    {
     "w": "medios",
     "f": 132
    },
    {
     "w": "digitales",
     "f": 143
    },
    {
     "w": "o",
     "f": 163
    },
    {
     "w": "remotos",
     "f": 169
    },
    {
     "w": "a",
     "f": 186
    },
    {
     "w": "incorporar",
     "f": 191
    },
    {
     "w": "la",
     "f": 210
    },
    {
     "w": "geolocalización",
     "f": 215
    },
    {
     "w": "inferencial.",
     "f": 243
    },
    {
     "w": "Ya",
     "f": 262
    },
    {
     "w": "no",
     "f": 267
    },
    {
     "w": "es",
     "f": 271
    },
    {
     "w": "opcional.",
     "f": 276
    }
   ]
  },
  {
   "id": "03",
   "start": 465,
   "dur": 11.392,
   "words": [
    {
     "w": "El",
     "f": 1
    },
    {
     "w": "artículo",
     "f": 9
    },
    {
     "w": "catorce",
     "f": 28
    },
    {
     "w": "la",
     "f": 43
    },
    {
     "w": "exige",
     "f": 47
    },
    {
     "w": "como",
     "f": 61
    },
    {
     "w": "fuente",
     "f": 71
    },
    {
     "w": "primaria",
     "f": 80
    },
    {
     "w": "de",
     "f": 95
    },
    {
     "w": "evaluación",
     "f": 99
    },
    {
     "w": "de",
     "f": 118
    },
    {
     "w": "riesgo.",
     "f": 123
    },
    {
     "w": "Y",
     "f": 133
    },
    {
     "w": "la",
     "f": 138
    },
    {
     "w": "define",
     "f": 144
    },
    {
     "w": "así:",
     "f": 161
    },
    {
     "w": "estimar",
     "f": 172
    },
    {
     "w": "la",
     "f": 186
    },
    {
     "w": "ubicación",
     "f": 191
    },
    {
     "w": "del",
     "f": 210
    },
    {
     "w": "solicitante",
     "f": 214
    },
    {
     "w": "y",
     "f": 238
    },
    {
     "w": "del",
     "f": 243
    },
    {
     "w": "dispositivo,",
     "f": 250
    },
    {
     "w": "sin",
     "f": 268
    },
    {
     "w": "necesidad",
     "f": 272
    },
    {
     "w": "de",
     "f": 291
    },
    {
     "w": "coordenadas",
     "f": 295
    },
    {
     "w": "físicas",
     "f": 314
    },
    {
     "w": "directas.",
     "f": 327
    }
   ]
  },
  {
   "id": "04",
   "start": 825,
   "dur": 9.579,
   "words": [
    {
     "w": "Las",
     "f": 1
    },
    {
     "w": "señales:",
     "f": 8
    },
    {
     "w": "dirección",
     "f": 29
    },
    {
     "w": "IP,",
     "f": 44
    },
    {
     "w": "tipo",
     "f": 59
    },
    {
     "w": "de",
     "f": 69
    },
    {
     "w": "red,",
     "f": 74
    },
    {
     "w": "proveedor",
     "f": 79
    },
    {
     "w": "de",
     "f": 96
    },
    {
     "w": "internet,",
     "f": 102
    },
    {
     "w": "VPN,",
     "f": 118
    },
    {
     "w": "proxies,",
     "f": 134
    },
    {
     "w": "redes",
     "f": 139
    },
    {
     "w": "de",
     "f": 151
    },
    {
     "w": "anonimización,",
     "f": 157
    },
    {
     "w": "zona",
     "f": 192
    },
    {
     "w": "horaria,",
     "f": 204
    },
    {
     "w": "y",
     "f": 221
    },
    {
     "w": "configuración",
     "f": 225
    },
    {
     "w": "regional",
     "f": 247
    },
    {
     "w": "del",
     "f": 260
    },
    {
     "w": "dispositivo.",
     "f": 264
    }
   ]
  },
  {
   "id": "05",
   "start": 1125,
   "dur": 9.941,
   "words": [
    {
     "w": "Sirve",
     "f": 1
    },
    {
     "w": "para",
     "f": 15
    },
    {
     "w": "dos",
     "f": 28
    },
    {
     "w": "cosas.",
     "f": 35
    },
    {
     "w": "Verificar",
     "f": 49
    },
    {
     "w": "el",
     "f": 69
    },
    {
     "w": "domicilio",
     "f": 74
    },
    {
     "w": "que",
     "f": 94
    },
    {
     "w": "declara",
     "f": 99
    },
    {
     "w": "el",
     "f": 114
    },
    {
     "w": "cliente.",
     "f": 120
    },
    {
     "w": "Y",
     "f": 132
    },
    {
     "w": "frenar",
     "f": 137
    },
    {
     "w": "aperturas",
     "f": 148
    },
    {
     "w": "desde",
     "f": 167
    },
    {
     "w": "jurisdicciones",
     "f": 177
    },
    {
     "w": "de",
     "f": 201
    },
    {
     "w": "alto",
     "f": 206
    },
    {
     "w": "riesgo,",
     "f": 216
    },
    {
     "w": "sancionadas,",
     "f": 227
    },
    {
     "w": "o",
     "f": 247
    },
    {
     "w": "que",
     "f": 252
    },
    {
     "w": "no",
     "f": 257
    },
    {
     "w": "cuadran",
     "f": 262
    },
    {
     "w": "con",
     "f": 270
    },
    {
     "w": "lo",
     "f": 275
    },
    {
     "w": "declarado.",
     "f": 279
    }
   ]
  },
  {
   "id": "06",
   "start": 1440,
   "dur": 8.853,
   "words": [
    {
     "w": "Nueve",
     "f": 1
    },
    {
     "w": "meses",
     "f": 13
    },
    {
     "w": "parecen",
     "f": 25
    },
    {
     "w": "muchos.",
     "f": 43
    },
    {
     "w": "Pero",
     "f": 56
    },
    {
     "w": "hay",
     "f": 66
    },
    {
     "w": "que",
     "f": 72
    },
    {
     "w": "decidir",
     "f": 77
    },
    {
     "w": "si",
     "f": 93
    },
    {
     "w": "se",
     "f": 98
    },
    {
     "w": "construye",
     "f": 103
    },
    {
     "w": "o",
     "f": 119
    },
    {
     "w": "se",
     "f": 125
    },
    {
     "w": "compra.",
     "f": 130
    },
    {
     "w": "Integrar",
     "f": 142
    },
    {
     "w": "con",
     "f": 157
    },
    {
     "w": "la",
     "f": 164
    },
    {
     "w": "plataforma",
     "f": 169
    },
    {
     "w": "de",
     "f": 186
    },
    {
     "w": "apertura.",
     "f": 191
    },
    {
     "w": "Calibrar.",
     "f": 206
    },
    {
     "w": "Y",
     "f": 226
    },
    {
     "w": "documentar",
     "f": 230
    },
    {
     "w": "en",
     "f": 247
    },
    {
     "w": "el",
     "f": 251
    },
    {
     "w": "manual.",
     "f": 255
    }
   ]
  },
  {
   "id": "07",
   "start": 1725,
   "dur": 4.672,
   "words": [
    {
     "w": "¿Su",
     "f": 1
    },
    {
     "w": "banco",
     "f": 6
    },
    {
     "w": "ya",
     "f": 16
    },
    {
     "w": "definió",
     "f": 21
    },
    {
     "w": "quién",
     "f": 37
    },
    {
     "w": "es",
     "f": 42
    },
    {
     "w": "el",
     "f": 47
    },
    {
     "w": "dueño",
     "f": 52
    },
    {
     "w": "de",
     "f": 62
    },
    {
     "w": "este",
     "f": 67
    },
    {
     "w": "proyecto?",
     "f": 79
    },
    {
     "w": "¿Tecnología,",
     "f": 93
    },
    {
     "w": "o",
     "f": 118
    },
    {
     "w": "Cumplimiento?",
     "f": 122
    }
   ]
  },
  {
   "id": "08",
   "start": 1875,
   "dur": 5.547,
   "words": [
    {
     "w": "Fuente:",
     "f": 1
    },
    {
     "w": "Acuerdo",
     "f": 17
    },
    {
     "w": "uno",
     "f": 35
    },
    {
     "w": "guion",
     "f": 46
    },
    {
     "w": "dos",
     "f": 52
    },
    {
     "w": "mil",
     "f": 58
    },
    {
     "w": "veintiséis",
     "f": 64
    },
    {
     "w": "de",
     "f": 81
    },
    {
     "w": "la",
     "f": 87
    },
    {
     "w": "SBP,",
     "f": 94
    },
    {
     "w": "artículos",
     "f": 100
    },
    {
     "w": "catorce",
     "f": 123
    },
    {
     "w": "y",
     "f": 137
    },
    {
     "w": "cincuenta",
     "f": 142
    },
    {
     "w": "y",
     "f": 156
    },
    {
     "w": "tres.",
     "f": 160
    }
   ]
  }
 ],
 "sign": 2055,
 "end": 2250
}
````

<!-- file: motion-graphics/template/src/scenes/S1Fecha.tsx -->
````tsx
import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C, FONT, IN, ease, sp} from '../theme';
import {SectionLabel, Slam, Stamp, useExit} from '../ui';
import {TL, span, wf} from '../tl';

// Apertura: línea dorada que colapsa en un punto (antes de la voz)
export const S0Open: React.FC = () => {
  const f = useCurrentFrame();
  const grow = ease(f, 0, 16);
  const collapse = ease(f, 18, 30, [0, 1], IN);
  const w = 820 * grow * (1 - collapse);
  const dot = ease(f, 26, 34);
  return (
    <AbsoluteFill style={{background: C.navy}}>
      <div style={{position: 'absolute', left: 540 - w / 2, top: 539, width: w, height: 3, background: C.gold, boxShadow: `0 0 20px ${C.gold}`}} />
      <div style={{position: 'absolute', left: 531, top: 531, width: 18, height: 18, borderRadius: 9, background: C.goldL, transform: `scale(${dot * 1.3})`, boxShadow: `0 0 36px ${C.goldL}`}} />
    </AbsoluteFill>
  );
};

const ID = '01';
const LEN = span(ID).len;

export const S1Fecha: React.FC = () => {
  const f = useCurrentFrame();
  const exit = useExit(LEN);
  // el punto de la apertura se abre en la órbita
  const orbit = sp(f, 0, {damping: 18, stiffness: 70});
  const ddmm = wf(ID, 'treinta');
  const year = wf(ID, 'veintisiete');
  const plazo = wf(ID, 'plazo');

  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: FONT}}>
      <AbsoluteFill style={{transform: `scale(${1 + exit * 0.15})`, filter: `blur(${exit * 12}px)`, opacity: 1 - exit * 0.5}}>
        <svg width="1080" height="1080" style={{position: 'absolute'}}>
          <circle cx="540" cy="540" r={9 + orbit * 351} fill="none" stroke={C.mute} strokeOpacity={0.4} strokeWidth={2} strokeDasharray="4 14" transform={`rotate(${f * 0.8} 540 540)`} />
          {[0, 1, 2].map((i) => {
            const a = ((f * 2.2 + i * 120) * Math.PI) / 180;
            const r = 9 + orbit * 351;
            return <circle key={i} cx={540 + Math.cos(a) * r} cy={540 + Math.sin(a) * r} r={i === 0 ? 9 : 6} fill={i === 0 ? C.teal : C.gold} opacity={orbit} />;
          })}
        </svg>

        {/* 30 · 06: dígito a dígito */}
        <div style={{position: 'absolute', top: 300, width: '100%', display: 'flex', justifyContent: 'center'}}>
          {'30 · 06'.split('').map((ch, i) => {
            const p = sp(f, ddmm + i * 2, {damping: 14, stiffness: 180});
            return (
              <span key={i} style={{display: 'inline-block', minWidth: ch === ' ' ? 30 : undefined, fontSize: 150, fontWeight: 900, color: C.white, opacity: Math.min(1, p * 1.4), transform: `translateY(${(1 - p) * 70}px)`, filter: `blur(${(1 - Math.min(1, p)) * 8}px)`}}>
                {ch}
              </span>
            );
          })}
        </div>

        <Slam text="2027" at={year} size={230} y={590} outline />

        <Stamp text="PLAZO LÍMITE" at={plazo} style={{left: 360, top: 790}} size={34} />
      </AbsoluteFill>
      <SectionLabel n="SBP" title="Acuerdo 1-2026" out={1 - exit} />
    </AbsoluteFill>
  );
};

export const OPEN = TL.open;
````

<!-- file: motion-graphics/template/src/scenes/S2Art53.tsx -->
````tsx
import React from 'react';
import {AbsoluteFill, interpolateColors, useCurrentFrame} from 'remotion';
import {C, FONT, IN, INOUT, ease, shake, sp} from '../theme';
import {SectionLabel, Slam, Source, useExit} from '../ui';
import {span, wf} from '../tl';

const ID = '02';
const LEN = span(ID).len;

// Rejilla de palabras apiladas en máscara, como en tipografía cinética
const Line: React.FC<{t: string; at: number; out: number; dir: number; color?: string; size?: number}> = ({t, at, out, dir, color = C.white, size = 112}) => {
  const f = useCurrentFrame();
  const p = sp(f, at, {damping: 18, stiffness: 140});
  const o = ease(f, out, out + 12, [0, 1], IN);
  return (
    <div style={{position: 'relative', height: size * 1.08, overflow: 'hidden', width: 1080}}>
      <div style={{position: 'absolute', inset: 0, textAlign: 'center', fontSize: size, fontWeight: 900, lineHeight: `${size * 1.08}px`, color, transform: `translateX(${(1 - p) * dir * 1100}px) translateY(${-o * size * 1.1}px) skewX(${(1 - p) * dir * -14}deg)`}}>
        {t}
      </div>
    </div>
  );
};

export const S2Art53: React.FC = () => {
  const f = useCurrentFrame();
  const exit = useExit(LEN);
  const art = wf(ID, 'artículo');
  const n53 = wf(ID, 'cincuenta');
  const bancos = wf(ID, 'bancos');
  const digital = wf(ID, 'digitales');
  const remotos = wf(ID, 'remotos');
  const geo = wf(ID, 'geolocalización');
  const ya = wf(ID, 'ya');
  const opc = wf(ID, 'opcional');

  // El 53 se retira a la esquina cuando entra el sujeto obligado
  const park = ease(f, bancos - 10, bancos + 8, [0, 1], INOUT);
  const flip = sp(f, ya, {damping: 13, stiffness: 220});
  const sh = shake(f, opc, 12, 12);
  const inverted = f >= opc && f < opc + 14;
  const toggleIn = sp(f, geo + 10, {damping: 18, stiffness: 120});

  return (
    <AbsoluteFill style={{background: inverted ? C.gold : C.navy, fontFamily: FONT}}>
      <AbsoluteFill style={{transform: `translate(${sh.x}px, ${sh.y}px)`, opacity: 1 - exit, filter: `blur(${exit * 10}px)`}}>
        {/* ART. 53: golpe y luego se aparca arriba a la derecha */}
        <div style={{position: 'absolute', inset: 0, transformOrigin: '1068px 68px', transform: `scale(${1 - park * 0.72})`}}>
          <div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', color: C.mute, fontSize: 34, fontWeight: 800, letterSpacing: 14, opacity: ease(f, art, art + 10) * (1 - park)}}>ARTÍCULO</div>
          <Slam text="53" at={n53} size={330} y={540} outline />
        </div>

        {/* sujeto y supuesto */}
        <div style={{position: 'absolute', top: 250, left: 0}}>
          <Line t="BANCOS CON" at={bancos} out={geo - 14} dir={-1} size={96} />
          <Line t="APERTURA" at={digital - 8} out={geo - 11} dir={1} color={C.gold} />
          <Line t="DIGITAL" at={digital} out={geo - 8} dir={-1} />
          <Line t="O REMOTA" at={remotos} out={geo - 5} dir={1} />
        </div>

        {/* obligación */}
        <div style={{position: 'absolute', top: 300, left: 0}}>
          <Line t="GEOLOCALIZACIÓN" at={geo} out={LEN} dir={-1} size={98} color={inverted ? C.navy : C.white} />
          <Line t="INFERENCIAL" at={geo + 8} out={LEN} dir={1} size={98} color={inverted ? C.navy : C.gold} />
        </div>

        {/* interruptor opcional → obligatorio */}
        <div style={{position: 'absolute', left: 140, top: 640, width: 800, height: 150, borderRadius: 24, border: `2px solid ${inverted ? C.navy : C.mute}55`, background: inverted ? 'transparent' : 'rgba(255,255,255,0.04)', transform: `translateY(${(1 - toggleIn) * 300}px)`, opacity: toggleIn, display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 48px', boxSizing: 'border-box'}}>
          <div style={{position: 'relative', fontSize: 40, fontWeight: 800, color: inverted ? C.navy : interpolateColors(flip, [0, 1], [C.white, C.mute])}}>
            Opcional
            <div style={{position: 'absolute', left: -6, top: 26, height: 5, width: 196 * ease(f, opc, opc + 8), background: C.coral}} />
          </div>
          <div style={{width: 150, height: 74, borderRadius: 37, background: interpolateColors(flip, [0, 1], ['#2A3558', inverted ? C.navy : C.gold]), position: 'relative'}}>
            <div style={{position: 'absolute', top: 7, left: 7 + flip * 76, width: 60, height: 60, borderRadius: 30, background: C.white, boxShadow: '0 4px 12px rgba(0,0,0,0.35)'}} />
          </div>
          <div style={{fontSize: 40, fontWeight: 900, color: inverted ? C.navy : interpolateColors(flip, [0, 1], [C.mute, C.goldL])}}>Obligatorio</div>
        </div>
      </AbsoluteFill>
      <SectionLabel n="01" title="Artículo 53" out={1 - exit} />
      <Source text="Fuente: Acuerdo 1-2026 SBP, art. 53" out={1 - exit} />
    </AbsoluteFill>
  );
};
````

<!-- file: motion-graphics/template/src/scenes/S3Art14.tsx -->
````tsx
import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {noise3D} from '@remotion/noise';
import {C, FONT, INOUT, ease, sp} from '../theme';
import {SectionLabel, Slam, Source, Stamp, Words, useExit} from '../ui';
import {span, wf} from '../tl';

const ID = '03';
const LEN = span(ID).len;

const PANEL = {x: 64, y: 330, w: 952, h: 560};
const COLS = 19;
const ROWS = 11;
const PINS = [
  {label: 'SOLICITANTE', x: 360, y: 600, word: 'solicitante', r: 120},
  {label: 'DISPOSITIVO', x: 720, y: 650, word: 'dispositivo', r: 95},
];

export const S3Art14: React.FC = () => {
  const f = useCurrentFrame();
  const exit = useExit(LEN);
  const n14 = wf(ID, 'catorce');
  const primaria = wf(ID, 'primaria');
  const estimar = wf(ID, 'estimar');
  const sin = wf(ID, 'sin');
  const coord = wf(ID, 'coordenadas');

  const park = ease(f, estimar - 16, estimar + 2, [0, 1], INOUT);
  const panel = sp(f, estimar - 6, {damping: 20, stiffness: 110});
  const pinT = PINS.map((p) => wf(ID, p.word));

  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: FONT}}>
      <AbsoluteFill style={{opacity: 1 - exit, filter: `blur(${exit * 10}px)`}}>
        {/* ART. 14 con golpe; se aparca arriba a la derecha */}
        <div style={{position: 'absolute', inset: 0, transformOrigin: '1068px 68px', transform: `scale(${1 - park * 0.72})`}}>
          <div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', color: C.mute, fontSize: 34, fontWeight: 800, letterSpacing: 14, opacity: ease(f, 6, 16) * (1 - park)}}>ARTÍCULO</div>
          <Slam text="14" at={n14} size={330} y={540} outline />
        </div>
        <div style={{opacity: 1 - park}}>
          <Stamp text="FUENTE PRIMARIA DE RIESGO" at={primaria} color={C.gold} rot={-6} size={30} style={{left: 250, top: 790}} />
        </div>

        {/* titular de la definición */}
        <div style={{position: 'absolute', left: 64, top: 190}}>
          <Words
            size={58}
            words={[
              {t: 'Estimar', at: estimar, color: C.gold},
              {t: 'la', at: estimar + 3},
              {t: 'ubicación', at: wf(ID, 'ubicación')},
              {t: 'sin', at: sin},
              {t: 'coordenadas', at: coord},
              {t: 'directas', at: coord + 4},
            ]}
          />
        </div>

        {/* mapa de puntos con dos estimaciones */}
        <div style={{position: 'absolute', left: PANEL.x, top: PANEL.y, width: PANEL.w, height: PANEL.h, borderRadius: 18, border: `2px solid ${C.mute}33`, background: 'rgba(255,255,255,0.03)', opacity: panel, transform: `translateY(${(1 - panel) * 80}px)`}} />
        <svg width="1080" height="1080" style={{position: 'absolute', opacity: panel}}>
          {Array.from({length: COLS * ROWS}).map((_, k) => {
            const c = k % COLS;
            const r = Math.floor(k / COLS);
            const x = PANEL.x + 46 + c * ((PANEL.w - 92) / (COLS - 1));
            const y = PANEL.y + 46 + r * ((PANEL.h - 92) / (ROWS - 1));
            const n = (noise3D('m', c * 0.15, r * 0.15, f * 0.02) + 1) / 2;
            let bump = 0;
            PINS.forEach((p, i) => {
              const age = f - pinT[i];
              if (age < 0 || age > 45) return;
              const d = Math.hypot(x - p.x, y - p.y);
              bump += Math.exp(-(((d - age * 14) / 40) ** 2)) * (1 - age / 45);
            });
            return <circle key={k} cx={x} cy={y} r={1.6 + n * 1.8 + bump * 4} fill={bump > 0.15 ? C.goldL : C.mute} opacity={0.25 + n * 0.25 + bump * 0.5} />;
          })}
          {PINS.map((p, i) => {
            const s = sp(f, pinT[i] - 4, {damping: 11, stiffness: 200});
            if (f < pinT[i] - 4) return null;
            const breathe = 1 + 0.05 * Math.sin((f - pinT[i]) / 9);
            return (
              <g key={i}>
                {/* círculo de incertidumbre: es una estimación, no un punto */}
                <circle cx={p.x} cy={p.y} r={p.r * s * breathe} fill={C.gold} fillOpacity={0.08} stroke={C.gold} strokeOpacity={0.7} strokeWidth={2} strokeDasharray="6 8" transform={`rotate(${f * 0.6} ${p.x} ${p.y})`} />
                <circle cx={p.x} cy={p.y} r={11 * s} fill={C.goldL} />
                <circle cx={p.x} cy={p.y} r={22 * s} fill="none" stroke={C.goldL} strokeWidth={3} opacity={0.6} />
              </g>
            );
          })}
        </svg>
        {PINS.map((p, i) => {
          const t = ease(f, pinT[i] + 4, pinT[i] + 16);
          return (
            <div key={i} style={{position: 'absolute', left: p.x - 120, top: p.y + p.r + 12, width: 240, textAlign: 'center', color: C.white, fontSize: 20, fontWeight: 800, letterSpacing: 4, opacity: t, transform: `translateY(${(1 - t) * 14}px)`}}>
              {p.label}
            </div>
          );
        })}

        {/* GPS tachado: sin coordenadas físicas directas */}
        {(() => {
          const a = sp(f, sin, {damping: 16, stiffness: 160});
          const strike = ease(f, coord, coord + 10);
          return (
            <div style={{position: 'absolute', right: 96, top: PANEL.y + 30, display: 'flex', alignItems: 'center', gap: 12, padding: '10px 18px', borderRadius: 12, border: `2px solid ${C.coral}`, color: C.coral, fontSize: 20, fontWeight: 900, letterSpacing: 3, opacity: a, transform: `scale(${0.6 + 0.4 * a})`}}>
              <svg width="28" height="28">
                <circle cx="14" cy="14" r="9" fill="none" stroke={C.coral} strokeWidth="3" />
                <line x1="14" y1="0" x2="14" y2="28" stroke={C.coral} strokeWidth="3" />
                <line x1="0" y1="14" x2="28" y2="14" stroke={C.coral} strokeWidth="3" />
                <line x1="2" y1="26" x2={2 + 24 * strike} y2={26 - 24 * strike} stroke={C.white} strokeWidth="4" />
              </svg>
              <span style={{position: 'relative'}}>
                COORDENADAS GPS
                <span style={{position: 'absolute', left: -4, top: 12, height: 4, width: 214 * strike, background: C.white}} />
              </span>
            </div>
          );
        })()}
      </AbsoluteFill>
      <SectionLabel n="02" title="Artículo 14" out={1 - exit} />
      <Source text="Fuente: Acuerdo 1-2026 SBP, art. 14" out={1 - exit} />
    </AbsoluteFill>
  );
};
````

<!-- file: motion-graphics/template/src/scenes/S4Senales.tsx -->
````tsx
import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {evolvePath} from '@remotion/paths';
import {C, FONT, INOUT, ease, sp} from '../theme';
import {SectionLabel, Source, useExit} from '../ui';
import {span, wf} from '../tl';

const ID = '04';
const LEN = span(ID).len;
const CX = 540;
const CY = 590;
const RX = 330;
const RY = 290;
const R = 132;

// Las ocho señales del art. 14, en el orden en que se nombran.
// Coral: señales de ocultación (VPN, proxies, anonimización).
const SIG = [
  {t: 'Dirección IP', word: 'dirección', a: -150},
  {t: 'Tipo de red', word: 'tipo', a: 180},
  {t: 'Proveedor de internet', word: 'proveedor', a: 145},
  {t: 'VPN', word: 'vpn', a: -30, hide: true},
  {t: 'Proxies', word: 'proxies', a: 0, hide: true},
  {t: 'Redes de anonimización', word: 'redes', a: 35, hide: true},
  {t: 'Zona horaria', word: 'zona', a: 90},
  {t: 'Configuración regional', word: 'configuración', a: -90},
];

const Globe: React.FC<{f: number; s: number; pulse: number}> = ({f, s, pulse}) => {
  const rot = f * 0.03;
  return (
    <svg width="1080" height="1080" style={{position: 'absolute'}}>
      <defs>
        <radialGradient id="gl" cx="0.38" cy="0.32" r="0.8">
          <stop offset="0" stopColor={C.deep} />
          <stop offset="1" stopColor={C.navy2} />
        </radialGradient>
        <clipPath id="gc">
          <circle cx={CX} cy={CY} r={R * s} />
        </clipPath>
      </defs>
      <circle cx={CX} cy={CY} r={R * s + 30 * pulse} fill="none" stroke={C.gold} strokeWidth={6 * (1 - pulse)} opacity={pulse > 0 ? 1 - pulse : 0} />
      <circle cx={CX} cy={CY} r={R * s} fill="url(#gl)" stroke={C.gold} strokeWidth={3} />
      <g clipPath="url(#gc)" stroke={C.mute} strokeOpacity={0.45} fill="none" strokeWidth={1.5}>
        {Array.from({length: 6}).map((_, i) => {
          const ph = rot + (i * Math.PI) / 6;
          return <ellipse key={i} cx={CX} cy={CY} rx={Math.abs(Math.cos(ph)) * R * s} ry={R * s} />;
        })}
        {[-0.66, -0.33, 0, 0.33, 0.66].map((k) => (
          <ellipse key={k} cx={CX} cy={CY + k * R * s} rx={Math.sqrt(1 - k * k) * R * s} ry={6 * s} />
        ))}
      </g>
    </svg>
  );
};

export const S4Senales: React.FC = () => {
  const f = useCurrentFrame();
  const exit = useExit(LEN);
  const globe = sp(f, 0, {damping: 14, stiffness: 120});
  const times = SIG.map((s) => wf(ID, s.word));
  const count = times.filter((t) => f >= t).length;
  const resolve = wf(ID, 'dispositivo') + 6;
  const pulse = f >= resolve ? ease(f, resolve, resolve + 24) : 0;
  const chip = sp(f, resolve, {damping: 14, stiffness: 180});

  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: FONT}}>
      <AbsoluteFill style={{opacity: 1 - exit, transform: `scale(${1 + exit * 0.12})`, filter: `blur(${exit * 10}px)`}}>
        {/* conectores */}
        <svg width="1080" height="1080" style={{position: 'absolute'}}>
          {SIG.map((s, i) => {
            const a = (s.a * Math.PI) / 180;
            const x = CX + Math.cos(a) * RX;
            const y = CY + Math.sin(a) * RY;
            const d = `M ${CX + Math.cos(a) * R} ${CY + Math.sin(a) * R} L ${x} ${y}`;
            const p = ease(f, times[i], times[i] + 10, [0, 1], INOUT);
            const ev = evolvePath(p, d);
            // paquete que viaja hacia el globo al resolver
            const q = ease(f, resolve - 14 + i, resolve - 2 + i, [0, 1], INOUT);
            return (
              <g key={i}>
                <path d={d} stroke={s.hide ? C.coral : C.gold} strokeOpacity={0.7} strokeWidth={2.5} strokeDasharray={ev.strokeDasharray} strokeDashoffset={ev.strokeDashoffset} fill="none" />
                {q > 0 && q < 1 && <circle cx={x + (CX + Math.cos(a) * R - x) * q} cy={y + (CY + Math.sin(a) * R - y) * q} r={7} fill={C.goldL} />}
              </g>
            );
          })}
        </svg>

        <Globe f={f} s={globe} pulse={pulse} />

        {SIG.map((s, i) => {
          const a = (s.a * Math.PI) / 180;
          const x = CX + Math.cos(a) * RX;
          const y = CY + Math.sin(a) * RY;
          const p = sp(f, times[i] + 4, {damping: 13, stiffness: 190});
          if (f < times[i] + 4) return null;
          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: x - 115,
                top: y - 36,
                width: 230,
                minHeight: 72,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                textAlign: 'center',
                padding: '8px 14px',
                boxSizing: 'border-box',
                borderRadius: 14,
                background: C.navy2,
                border: `2px solid ${s.hide ? C.coral : C.gold}`,
                color: C.white,
                fontSize: 22,
                fontWeight: 800,
                lineHeight: 1.15,
                transform: `translate(${(CX - x) * (1 - p)}px, ${(CY - y) * (1 - p)}px) scale(${p})`,
                boxShadow: '0 12px 30px rgba(0,0,0,0.35)',
              }}
            >
              {s.t}
            </div>
          );
        })}

        {/* contador de señales */}
        <div style={{position: 'absolute', right: 64, top: 160, textAlign: 'right'}}>
          <div style={{color: C.goldL, fontSize: 84, fontWeight: 900, lineHeight: 1, fontVariantNumeric: 'tabular-nums'}}>
            {count}
            <span style={{color: C.mute, fontSize: 40}}> / 8</span>
          </div>
          <div style={{color: C.mute, fontSize: 16, fontWeight: 700, letterSpacing: 4, marginTop: 6}}>SEÑALES</div>
        </div>

        <div style={{position: 'absolute', left: CX - 150, top: CY - 22, width: 300, display: 'flex', justifyContent: 'center', opacity: chip, transform: `scale(${chip})`}}>
          <div style={{padding: '10px 18px', borderRadius: 10, background: C.gold, color: C.navy, fontSize: 18, fontWeight: 900, letterSpacing: 2, whiteSpace: 'nowrap'}}>UBICACIÓN ESTIMADA</div>
        </div>
      </AbsoluteFill>
      <SectionLabel n="03" title="Las señales" out={1 - exit} />
      <Source text="Fuente: Acuerdo 1-2026 SBP, art. 14" out={1 - exit} />
    </AbsoluteFill>
  );
};
````

<!-- file: motion-graphics/template/src/scenes/S5Controles.tsx -->
````tsx
import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {evolvePath, getPointAtLength} from '@remotion/paths';
import {C, FONT, INOUT, ease, sp} from '../theme';
import {SectionLabel, Slam, Source, useExit} from '../ui';
import {span, wf} from '../tl';

const ID = '05';
const LEN = span(ID).len;

const NODE = {x: 330, y: 560};
const OK = {x: 610, y: 330, w: 410, h: 150};
const NO = {x: 610, y: 560, w: 410, h: 330};
const P_IN = `M 200 ${NODE.y} L ${NODE.x - 100} ${NODE.y}`;
const P_OK = `M ${NODE.x + 100} ${NODE.y} C 540 ${NODE.y} 520 ${OK.y + OK.h / 2} ${OK.x} ${OK.y + OK.h / 2}`;
const P_NO = `M ${NODE.x + 100} ${NODE.y} C 540 ${NODE.y} 520 ${NO.y + 60} ${NO.x} ${NO.y + 60}`;

const Path: React.FC<{d: string; p: number; color: string}> = ({d, p, color}) => {
  const ev = evolvePath(p, d);
  return <path d={d} fill="none" stroke={color} strokeWidth={4} strokeLinecap="round" strokeDasharray={ev.strokeDasharray} strokeDashoffset={ev.strokeDashoffset} />;
};

export const S5Controles: React.FC = () => {
  const f = useCurrentFrame();
  const exit = useExit(LEN);
  const dos = wf(ID, 'dos');
  const verif = wf(ID, 'verificar');
  const cliente = wf(ID, 'cliente');
  const frenar = wf(ID, 'frenar');
  const items = [
    {t: 'Jurisdicción de alto riesgo', at: wf(ID, 'alto')},
    {t: 'Jurisdicción sancionada', at: wf(ID, 'sancionadas')},
    {t: 'No cuadra con lo declarado', at: wf(ID, 'cuadran')},
  ];

  const flow = sp(f, dos + 10, {damping: 18, stiffness: 120});
  const pIn = ease(f, dos + 8, dos + 22, [0, 1], INOUT);
  const pOk = ease(f, verif - 4, verif + 10, [0, 1], INOUT);
  const pNo = ease(f, frenar - 4, frenar + 10, [0, 1], INOUT);
  const okCard = sp(f, verif + 4, {damping: 14, stiffness: 170});
  const noCard = sp(f, frenar + 4, {damping: 14, stiffness: 170});
  const check = ease(f, cliente, cliente + 10);
  // paquete que recorre la rama de bloqueo y se detiene en seco
  const pkt = ease(f, frenar + 4, frenar + 22, [0, 1], INOUT);
  const head = getPointAtLength(P_NO, pkt * 330) ?? {x: 0, y: 0};

  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: FONT}}>
      <AbsoluteFill style={{opacity: 1 - exit, filter: `blur(${exit * 10}px)`}}>
        {/* "2 controles" */}
        <div style={{position: 'absolute', inset: 0, transformOrigin: '64px 150px', transform: `scale(${1 - ease(f, dos + 6, dos + 20, [0, 1], INOUT) * 0.62})`}}>
          <Slam text="2" at={dos} size={300} x={190} y={300} />
        </div>
        <div style={{position: 'absolute', left: 150, top: 168, color: C.white, fontSize: 52, fontWeight: 900, opacity: ease(f, dos + 14, dos + 24), transform: `translateX(${(1 - ease(f, dos + 14, dos + 24)) * -30}px)`}}>
          controles
        </div>

        <svg width="1080" height="1080" style={{position: 'absolute'}}>
          <Path d={P_IN} p={pIn} color={C.mute} />
          <Path d={P_OK} p={pOk} color={C.teal} />
          <Path d={P_NO} p={pNo} color={C.coral} />
          {pkt > 0 && pkt < 1 && <circle cx={head.x} cy={head.y} r={9} fill={C.coral} />}
        </svg>

        {/* origen y nodo */}
        <div style={{position: 'absolute', left: 40, top: NODE.y - 50, width: 160, height: 100, borderRadius: 14, border: `2px solid ${C.mute}55`, background: 'rgba(255,255,255,0.04)', color: C.white, fontSize: 19, fontWeight: 800, display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', opacity: flow, transform: `translateX(${(1 - flow) * -80}px)`}}>
          Solicitud de apertura
        </div>
        <div style={{position: 'absolute', left: NODE.x - 100, top: NODE.y - 70, width: 200, height: 140, borderRadius: 18, background: C.gold, color: C.navy, fontSize: 24, fontWeight: 900, display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', lineHeight: 1.15, transform: `scale(${flow})`, boxShadow: `0 0 50px ${C.gold}55`}}>
          Ubicación estimada
        </div>

        {/* control 1: validar */}
        <div style={{position: 'absolute', left: OK.x, top: OK.y, width: OK.w, height: OK.h, borderRadius: 16, border: `2px solid ${C.teal}`, background: C.navy2, padding: 24, boxSizing: 'border-box', transform: `scale(${okCard})`, transformOrigin: 'left center'}}>
          <div style={{display: 'flex', alignItems: 'center', gap: 14, color: C.teal, fontSize: 30, fontWeight: 900, letterSpacing: 2}}>
            <svg width="34" height="34">
              <circle cx="17" cy="17" r="15" fill="none" stroke={C.teal} strokeWidth="3" />
              <path d="M 9 17 L 15 23 L 26 11" fill="none" stroke={C.teal} strokeWidth="4" strokeLinecap="round" strokeDasharray="30" strokeDashoffset={30 * (1 - check)} />
            </svg>
            VALIDAR
          </div>
          <div style={{color: C.white, fontSize: 22, fontWeight: 600, marginTop: 14}}>Domicilio declarado por el cliente</div>
        </div>

        {/* control 2: frenar */}
        <div style={{position: 'absolute', left: NO.x, top: NO.y, width: NO.w, height: NO.h, borderRadius: 16, border: `2px solid ${C.coral}`, background: C.navy2, padding: 24, boxSizing: 'border-box', transform: `scale(${noCard})`, transformOrigin: 'left top'}}>
          <div style={{display: 'flex', alignItems: 'center', gap: 14, color: C.coral, fontSize: 30, fontWeight: 900, letterSpacing: 2}}>
            <svg width="34" height="34">
              <circle cx="17" cy="17" r="15" fill="none" stroke={C.coral} strokeWidth="3" />
              <path d="M 11 11 L 23 23 M 23 11 L 11 23" stroke={C.coral} strokeWidth="4" strokeLinecap="round" />
            </svg>
            FRENAR APERTURA
          </div>
          {items.map((it, i) => {
            const p = sp(f, it.at, {damping: 15, stiffness: 180});
            return (
              <div key={i} style={{display: 'flex', alignItems: 'center', gap: 12, marginTop: i === 0 ? 26 : 18, opacity: Math.min(1, p * 1.5), transform: `translateX(${(1 - p) * 60}px)`}}>
                <div style={{width: 10, height: 10, borderRadius: 5, background: C.coral, flexShrink: 0}} />
                <div style={{color: C.white, fontSize: 22, fontWeight: 700}}>{it.t}</div>
              </div>
            );
          })}
        </div>
      </AbsoluteFill>
      <SectionLabel n="04" title="Para qué sirve" out={1 - exit} />
      <Source text="Fuente: Acuerdo 1-2026 SBP, arts. 14 y 53" out={1 - exit} />
    </AbsoluteFill>
  );
};
````

<!-- file: motion-graphics/template/src/scenes/S6Plazo.tsx -->
````tsx
import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C, FONT, INOUT, ease, sp} from '../theme';
import {SectionLabel, Slam, Source, useExit} from '../ui';
import {span, wf} from '../tl';

const ID = '06';
const LEN = span(ID).len;

const X0 = 90;
const X1 = 990;
const AXIS = 400;
const MONTHS = ['OCT', 'NOV', 'DIC', 'ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN'];
// Frentes de trabajo: posiciones ilustrativas, no a escala
const BARS = [
  {t: 'Construir o comprar', word: 'decidir', a: 0, b: 0.34},
  {t: 'Integrar con la plataforma', word: 'integrar', a: 0.24, b: 0.66},
  {t: 'Calibrar', word: 'calibrar', a: 0.56, b: 0.84},
  {t: 'Documentar en el manual', word: 'documentar', a: 0.62, b: 1},
];

export const S6Plazo: React.FC = () => {
  const f = useCurrentFrame();
  const exit = useExit(LEN);
  const nueve = wf(ID, 'nueve');
  const pero = wf(ID, 'pero');
  const park = ease(f, pero - 10, pero + 6, [0, 1], INOUT);
  const axis = ease(f, pero - 4, pero + 18, [0, 1], INOUT);
  // cursor "hoy" que avanza: el tiempo corre mientras se enumeran los frentes
  const today = ease(f, pero, LEN, [0, 0.18]);
  const xOf = (k: number) => X0 + k * (X1 - X0);

  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: FONT}}>
      <AbsoluteFill style={{opacity: 1 - exit, filter: `blur(${exit * 10}px)`}}>
        {/* 9 meses: golpe y se aparca como titular */}
        <div style={{position: 'absolute', inset: 0, transformOrigin: '64px 150px', transform: `scale(${1 - park * 0.66})`}}>
          <Slam text="9" at={nueve} size={360} x={330} y={520} outline />
          <div style={{position: 'absolute', left: 480, top: 430, color: C.white, fontSize: 110, fontWeight: 900, lineHeight: 1, opacity: ease(f, wf(ID, 'meses'), wf(ID, 'meses') + 8)}}>
            MESES
          </div>
        </div>
        <div style={{position: 'absolute', left: 352, top: 250, color: C.mute, fontSize: 30, fontWeight: 700, opacity: ease(f, pero + 4, pero + 16)}}>
          cuatro frentes de trabajo
        </div>

        {/* eje temporal */}
        <svg width="1080" height="1080" style={{position: 'absolute'}}>
          <line x1={X0} x2={X0 + (X1 - X0) * axis} y1={AXIS} y2={AXIS} stroke={C.mute} strokeOpacity={0.5} strokeWidth={2} />
          {MONTHS.map((m, i) => {
            const x = xOf(i / (MONTHS.length - 1));
            const o = ease(f, pero + i * 2, pero + 8 + i * 2);
            return (
              <g key={m} opacity={o}>
                <line x1={x} x2={x} y1={AXIS - 8} y2={AXIS + 8} stroke={C.mute} strokeWidth={2} />
                <text x={x} y={AXIS - 22} fill={C.mute} fontSize={16} fontWeight={700} textAnchor="middle" fontFamily="Nunito Sans" letterSpacing={2}>
                  {m}
                </text>
              </g>
            );
          })}
          {/* fecha límite */}
          <line x1={X1} x2={X1} y1={AXIS - 60} y2={AXIS - 60 + 520 * axis} stroke={C.coral} strokeWidth={4} />
          {/* hoy */}
          <line x1={xOf(today)} x2={xOf(today)} y1={AXIS - 14} y2={AXIS + 460 * axis} stroke={C.goldL} strokeWidth={2} strokeDasharray="6 8" opacity={axis} />
        </svg>
        <div style={{position: 'absolute', left: X1 - 160, top: AXIS - 100, width: 160, textAlign: 'right', color: C.coral, fontSize: 20, fontWeight: 900, letterSpacing: 2, opacity: axis}}>30·06·2027</div>
        <div style={{position: 'absolute', left: xOf(today) - 40, top: AXIS + 462 * axis, width: 80, textAlign: 'center', color: C.goldL, fontSize: 15, fontWeight: 800, letterSpacing: 3, opacity: axis}}>HOY</div>

        {BARS.map((b, i) => {
          const at = wf(ID, b.word);
          const p = sp(f, at, {damping: 18, stiffness: 150});
          const y = AXIS + 46 + i * 100;
          return (
            <div key={i} style={{position: 'absolute', left: xOf(b.a), top: y, width: (xOf(b.b) - xOf(b.a)) * p, height: 66, borderRadius: 10, background: i === 3 ? C.gold : C.deep, border: `2px solid ${C.gold}`, overflow: 'hidden', opacity: f >= at ? 1 : 0}}>
              <div style={{padding: '0 18px', lineHeight: '62px', whiteSpace: 'nowrap', color: i === 3 ? C.navy : C.white, fontSize: 22, fontWeight: 800}}>{b.t}</div>
            </div>
          );
        })}
      </AbsoluteFill>
      <SectionLabel n="05" title="Nueve meses" out={1 - exit} />
      <Source text="Esquema ilustrativo, duraciones no a escala · Fuente: Acuerdo 1-2026 SBP, art. 53" out={1 - exit} />
    </AbsoluteFill>
  );
};
````

<!-- file: motion-graphics/template/src/scenes/S7Pregunta.tsx -->
````tsx
import React from 'react';
import {AbsoluteFill, Easing, useCurrentFrame} from 'remotion';
import {C, FONT, ease, sp} from '../theme';
import {SectionLabel, Words} from '../ui';
import {span, wf} from '../tl';

const ID = '07';
const LEN = span(ID).len;
const RING = {x: 540, y: 660};

export const S7Pregunta: React.FC = () => {
  const f = useCurrentFrame();
  const tec = wf(ID, 'tecnología');
  const o = wf(ID, 'o');
  const cum = wf(ID, 'cumplimiento');
  // zoom a través de la "o": transición hacia la fuente
  const zIn = LEN - 22;
  const z = ease(f, zIn, LEN, [0, 1], Easing.in(Easing.exp));
  const scale = 1 + z * 70;
  const ring = sp(f, o - 3, {damping: 11, stiffness: 220});
  const speed = ease(f, zIn + 4, LEN);

  const card = (label: string, at: number, x: number, dir: number) => {
    const p = sp(f, at - 2, {damping: 15, stiffness: 150});
    return (
      <div style={{position: 'absolute', left: x, top: RING.y - 110, width: 330, height: 220, perspective: 900, opacity: Math.min(1, p * 1.5)}}>
        <div style={{width: '100%', height: '100%', borderRadius: 22, border: `2px solid ${C.gold}`, background: 'linear-gradient(160deg, rgba(31,48,106,0.95), rgba(17,27,61,0.95))', display: 'flex', alignItems: 'center', justifyContent: 'center', color: C.white, fontSize: 36, fontWeight: 900, letterSpacing: 2, transform: `rotateY(${dir * (14 + (1 - p) * 60)}deg) translateX(${(1 - p) * dir * -260}px)`, boxShadow: '0 30px 60px rgba(0,0,0,0.45)'}}>
          {label}
        </div>
      </div>
    );
  };

  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: FONT, overflow: 'hidden'}}>
      {speed > 0 && (
        <svg width="1080" height="1080" style={{position: 'absolute', opacity: speed * 0.8}}>
          {Array.from({length: 40}).map((_, i) => {
            const a = (i / 40) * Math.PI * 2 + i * 0.37;
            const r0 = 200 + ((i * 97 + f * 40) % 500);
            const len = 80 + speed * 200;
            return <line key={i} x1={540 + Math.cos(a) * r0} y1={540 + Math.sin(a) * r0} x2={540 + Math.cos(a) * (r0 + len)} y2={540 + Math.sin(a) * (r0 + len)} stroke={i % 5 ? C.mute : C.gold} strokeWidth={3} strokeLinecap="round" />;
          })}
        </svg>
      )}
      <AbsoluteFill style={{transformOrigin: `${RING.x}px ${RING.y}px`, transform: `translate(0, ${(540 - RING.y) * z}px) scale(${scale})`}}>
        <div style={{position: 'absolute', left: 64, top: 220, opacity: 1 - ease(f, zIn, zIn + 6)}}>
          <Words
            size={64}
            align="center"
            words={[
              {t: '¿Quién', at: wf(ID, 'quién')},
              {t: 'es', at: wf(ID, 'es')},
              {t: 'el', at: wf(ID, 'el')},
              {t: 'dueño', at: wf(ID, 'dueño'), color: C.gold},
              {t: 'de', at: wf(ID, 'de', 1)},
              {t: 'este', at: wf(ID, 'este')},
              {t: 'proyecto?', at: wf(ID, 'proyecto')},
            ]}
          />
        </div>
        {card('Tecnología', tec, 60, 1)}
        {card('Cumplimiento', cum, 690, -1)}
        {f >= o - 3 && (
          <svg width="1080" height="1080" style={{position: 'absolute'}}>
            <circle cx={RING.x} cy={RING.y} r={44 * ring} fill="none" stroke={C.gold} strokeWidth={20} />
          </svg>
        )}
      </AbsoluteFill>
      <div style={{opacity: 1 - ease(f, zIn, zIn + 6)}}>
        <SectionLabel n="06" title="La pregunta" />
      </div>
    </AbsoluteFill>
  );
};
````

<!-- file: motion-graphics/template/src/scenes/S8Fuente.tsx -->
````tsx
import React from 'react';
import {AbsoluteFill, random, useCurrentFrame} from 'remotion';
import {C, FONT, IN, INOUT, OUT, ease, gold, sp} from '../theme';
import {Stamp, Words, useExit} from '../ui';
import {TL, span, wf} from '../tl';

const ID = '08';
const LEN = span(ID).len;

export const S8Fuente: React.FC = () => {
  const f = useCurrentFrame();
  const exit = useExit(LEN, 14);
  const bar = ease(f, 2, 16);
  const cta = ease(f, wf(ID, 'cincuenta') + 14, wf(ID, 'cincuenta') + 28);

  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: FONT}}>
      <AbsoluteFill style={{opacity: 1 - exit, transform: `scale(${1 - exit * 0.08})`, filter: `blur(${exit * 8}px)`}}>
        <div style={{position: 'absolute', left: 64, top: 250, display: 'flex', alignItems: 'center', gap: 16}}>
          <div style={{width: 56 * bar, height: 4, background: C.gold}} />
          <div style={{color: C.gold, fontSize: 24, fontWeight: 800, letterSpacing: 8, opacity: bar}}>FUENTE</div>
        </div>
        <div style={{position: 'absolute', left: 64, top: 300}}>
          <Words
            size={92}
            words={[
              {t: 'Acuerdo', at: wf(ID, 'acuerdo')},
              {t: '1-2026', at: wf(ID, 'uno'), color: C.goldL},
            ]}
          />
          <div style={{marginTop: 10}}>
            <Words
              size={38}
              weight={700}
              words={[
                {t: 'Superintendencia de Bancos de Panamá', at: wf(ID, 'superintendencia|sbp'), color: C.mute},
                {t: '· SBP', at: wf(ID, 'superintendencia|sbp') + 8, color: C.goldL},
              ]}
            />
          </div>
        </div>
        <Stamp text="ART. 14" at={wf(ID, 'catorce')} color={C.gold} rot={-4} size={44} style={{left: 64, top: 540}} />
        <Stamp text="ART. 53" at={wf(ID, 'cincuenta')} color={C.gold} rot={3} size={44} style={{left: 330, top: 540}} />

        <div style={{position: 'absolute', left: 64, top: 720, opacity: cta, transform: `translateY(${(1 - cta) * 20}px)`}}>
          <div style={{color: C.white, fontSize: 30, fontWeight: 800}}>¿Tecnología o Cumplimiento?</div>
          <div style={{color: C.mute, fontSize: 24, fontWeight: 600, marginTop: 8}}>Cuéntenos en los comentarios.</div>
          <div style={{color: C.teal, fontSize: 22, fontWeight: 800, marginTop: 14, letterSpacing: 1}}>#PBC #Cumplimiento #GeolocalizaciónInferencial</div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// Firma: partículas que convergen en un anillo elíptico y colapsan al punto inicial
const N = 200;
const RY = 300;
const RXK = 1.38;
const BURST = 42;
const P = Array.from({length: N}).map((_, i) => {
  const a = random(`a${i}`) * Math.PI * 2;
  const dist = 700 + random(`d${i}`) * 700;
  return {sx: 540 + Math.cos(a) * dist, sy: 540 + Math.sin(a) * dist, ta: (i / N) * Math.PI * 2, delay: random(`t${i}`) * 20, size: 1.6 + random(`s${i}`) * 3.4, gold: random(`c${i}`) > 0.35};
});
const CRED = ['CP/AML FIBA · ISO 37301 · 37001 · 37000 · 31000', 'AI COMPLIANCE EXPERT · LEGALTECH ARCHITECT', 'LEAN SIX SIGMA GREEN BELT · DOCENTE · SPEAKER'];

export const S9Firma: React.FC = () => {
  const f = useCurrentFrame();
  const len = TL.end - TL.sign;
  const spin = f * 0.5 + ease(f, BURST - 6, BURST + 30, [0, 110], OUT);
  const ry = RY + ease(f, BURST - 4, BURST + 20, [0, 24], OUT);
  const close = ease(f, len - 30, len - 8, [0, 1], IN);
  const tracking = ease(f, BURST, BURST + 46, [30, 6], OUT);
  const shine = ease(f, BURST + 18, BURST + 64, [-40, 140], INOUT);
  const logo = sp(f, BURST, {damping: 14, stiffness: 120});
  const sub = ease(f, BURST + 22, BURST + 38);
  const cred = ease(f, BURST + 38, BURST + 56);
  const fadeText = 1 - ease(f, len - 40, len - 28);
  const burst = ease(f, BURST - 2, BURST + 24);

  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: FONT}}>
      <AbsoluteFill style={{background: `radial-gradient(circle at 50% 50%, ${C.deep} 0%, transparent 60%)`, opacity: ease(f, BURST - 10, BURST + 20) * fadeText}} />
      <svg width="1080" height="1080" style={{position: 'absolute'}}>
        {P.map((p, i) => {
          const t = ease(f, p.delay, p.delay + 30, [0, 1], INOUT);
          const tp = ease(f - 2, p.delay, p.delay + 30, [0, 1], INOUT);
          const a = p.ta + (spin * Math.PI) / 180;
          const r = ry * (1 - close);
          const tx = 540 + Math.cos(a) * r * RXK;
          const ty = 540 + Math.sin(a) * r;
          const x = p.sx + (tx - p.sx) * t;
          const y = p.sy + (ty - p.sy) * t;
          return (
            <g key={i} opacity={1 - ease(f, len - 10, len - 4)}>
              <line x1={p.sx + (tx - p.sx) * tp} y1={p.sy + (ty - p.sy) * tp} x2={x} y2={y} stroke={p.gold ? C.gold : C.mute} strokeWidth={p.size} strokeLinecap="round" opacity={0.6} />
              <circle cx={x} cy={y} r={p.size} fill={p.gold ? C.goldL : C.white} />
            </g>
          );
        })}
        {burst > 0 && burst < 1 && <ellipse cx="540" cy="540" rx={(RY + burst * 500) * RXK} ry={RY + burst * 500} fill="none" stroke={C.goldL} strokeWidth={12 * (1 - burst)} opacity={1 - burst} />}
        <circle cx="540" cy="540" r={9 * ease(f, len - 10, len - 5) * (1 - ease(f, len - 3, len))} fill={C.goldL} />
      </svg>

      <div style={{position: 'absolute', top: 360, width: '100%', textAlign: 'center', opacity: fadeText}}>
        <div style={{display: 'inline-block', fontSize: 74, fontWeight: 900, lineHeight: 1.05, letterSpacing: tracking, paddingLeft: tracking, backgroundImage: `linear-gradient(110deg, transparent ${shine - 12}%, rgba(255,255,255,0.95) ${shine}%, transparent ${shine + 12}%), ${gold}`, WebkitBackgroundClip: 'text', color: 'transparent', opacity: f < BURST ? 0 : 1, transform: `scale(${0.6 + 0.4 * logo})`, filter: `blur(${(1 - Math.min(1, logo)) * 14}px)`}}>
          JOSÉ ANTONIO
          <br />
          SERRANO
        </div>
        <div style={{width: 220 * sub, height: 2, background: C.gold, margin: '22px auto 18px'}} />
        <div style={{color: C.white, fontSize: 24, fontWeight: 700, letterSpacing: 8, opacity: sub, transform: `translateY(${(1 - sub) * 18}px)`}}>AML · CUMPLIMIENTO · GRC</div>
        <div style={{marginTop: 24, opacity: cred, transform: `translateY(${(1 - cred) * 14}px)`}}>
          {CRED.map((c) => (
            <div key={c} style={{color: C.mute, fontSize: 15, fontWeight: 700, letterSpacing: 2.5, lineHeight: 1.75}}>
              {c}
            </div>
          ))}
        </div>
      </div>
    </AbsoluteFill>
  );
};
````

<!-- file: motion-graphics/template/script.json -->
````json
{
 "lines": [
  {
   "id": "01",
   "text": "Treinta de junio de dos mil veintisiete. Ese es el plazo."
  },
  {
   "id": "02",
   "text": "El artículo cincuenta y tres obliga a los bancos que abren cuentas por medios digitales o remotos a incorporar la geolocalización inferencial. Ya no es opcional."
  },
  {
   "id": "03",
   "text": "El artículo catorce la exige como fuente primaria de evaluación de riesgo. Y la define así: estimar la ubicación del solicitante y del dispositivo, sin necesidad de coordenadas físicas directas."
  },
  {
   "id": "04",
   "text": "Las señales: dirección IP, tipo de red, proveedor de internet, VPN, proxies, redes de anonimización, zona horaria, y configuración regional del dispositivo."
  },
  {
   "id": "05",
   "text": "Sirve para dos cosas. Verificar el domicilio que declara el cliente. Y frenar aperturas desde jurisdicciones de alto riesgo, sancionadas, o que no cuadran con lo declarado."
  },
  {
   "id": "06",
   "text": "Nueve meses parecen muchos. Pero hay que decidir si se construye o se compra. Integrar con la plataforma de apertura. Calibrar. Y documentar en el manual."
  },
  {
   "id": "07",
   "text": "¿Su banco ya definió quién es el dueño de este proyecto? ¿Tecnología, o Cumplimiento?"
  },
  {
   "id": "08",
   "text": "Fuente: Acuerdo uno dos mil veintiséis de la Superintendencia de Bancos de Panamá, artículos catorce y cincuenta y tres."
  }
 ]
}
````

<!-- file: motion-graphics/template/LOCUCION.md -->
````markdown
# Locución · Geolocalización inferencial

Tono: ejecutivo, cercano, seguro. Como explicándole el tema a un gerente de cumplimiento en una reunión, no leyendo.
Ritmo: unas 150 palabras por minuto. Baja la intensidad al final de cada idea y sube en las cifras.

Marcas de pausa:
- `/` pausa corta, como una coma al hablar (unos 0,3 s)
- `//` pausa de respiración (unos 0,7 s)
- **negrita**: palabra con énfasis

Formato de entrega: un archivo por frase (`01.wav` … `08.wav`, o `.m4a` del móvil), o uno solo continuo dejando 2 segundos de silencio entre frases. Graba en una habitación con muebles o cortinas, a un palmo del micrófono, sin música de fondo.

---

**01 · La fecha**
**Treinta de junio** de dos mil **veintisiete**. // Ese es el **plazo**.

**02 · Artículo 53**
El artículo **cincuenta y tres** / obliga a los bancos que abren cuentas por medios **digitales** o **remotos** / a incorporar la **geolocalización inferencial**. // Ya **no** es opcional.

**03 · Artículo 14**
El artículo **catorce** la exige / como **fuente primaria** de evaluación de riesgo. // Y la define así: / **estimar** la ubicación del solicitante / y del dispositivo, / **sin** necesidad de coordenadas físicas directas.

**04 · Las señales**
Las señales: // dirección **IP**, / tipo de red, / proveedor de internet, / **VPN**, / proxies, / redes de anonimización, / zona horaria, / y configuración regional del dispositivo.

**05 · Para qué sirve**
Sirve para **dos** cosas. // **Verificar** el domicilio que declara el cliente. // Y **frenar** aperturas desde jurisdicciones de alto riesgo, / sancionadas, / o que no cuadran con lo declarado.

**06 · Nueve meses**
**Nueve meses** parecen muchos. // Pero hay que decidir / si se **construye** o se **compra**. / Integrar con la plataforma de apertura. / **Calibrar**. / Y documentar en el manual.

**07 · La pregunta**
¿Su banco ya definió / quién es el **dueño** de este proyecto? // ¿**Tecnología**, / o **Cumplimiento**?

**08 · Fuente**
Fuente: / Acuerdo **uno dos mil veintiséis** de la **Superintendencia de Bancos de Panamá**, / artículos **catorce** y **cincuenta y tres**.
````

<!-- file: motion-graphics/template/voice/README.md -->
````markdown
# voice/

Una pista por frase del guion: `01.wav`, `02.wav`, … (mono o estéreo, cualquier
frecuencia). Los ids coinciden con `script.json`.

Flujo al recibir la voz:
1. `python3 align.py`     → words.json (tiempos por palabra)
2. `python3 timeline.py`  → src/timeline.json (frases en el pulso)
3. `python3 score.py`     → public/mix.wav (música + voz, −14 LUFS)
4. revisar fotogramas y renderizar los formatos.

Sin voz, `score.py` genera solo la música sobre la línea de tiempo existente.
````

<!-- file: motion-graphics/template/align.py -->
````python
"""Tiempos por palabra sin Whisper (descarga de modelos bloqueada).
Se mide la voz con RMS (ventanas de 10 ms) y se buscan las pausas. Luego se
anclan las fronteras en cascada: fin de oración (. : ?) a la pausa más larga
cercana, comas a la pausa más cercana, y el resto de palabras se reparte por
sílabas entre anclas. Fronteras de oración: ±30 ms. Palabras sueltas: ±150 ms."""
import json, re, wave
import numpy as np

import os
# Guion: script.json. Audio: voice/NN.wav (o VOICE_DIR)
req = json.load(open(os.environ.get('SCRIPT', 'script.json')))
VOICE_DIR = os.environ.get('VOICE_DIR', 'voice')


def load(p):
    w = wave.open(p)
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)
    if w.getnchannels() == 2:
        x = x.reshape(-1, 2).mean(1)
    return x / 32768, w.getframerate()


def syl(w):
    return max(1, len(re.findall(r'[aeiouáéíóúü]+', w.lower())) + (2 if w.upper().strip(',.?:') in ('IP', 'VPN') else 0))


out = []
for line in req['lines']:
    x, sr = load(f"{VOICE_DIR}/{line['id']}.wav")
    hop = sr // 100
    db = np.array([20 * np.log10(np.sqrt(np.mean(x[i:i + hop] ** 2)) + 1e-9) for i in range(0, len(x) - hop, hop)])
    v = db > -45
    first = int(np.argmax(v)) / 100
    last = (len(v) - int(np.argmax(v[::-1]))) / 100
    # pausas: (inicio, fin) de tramos sin voz >= 50 ms dentro del habla
    gaps, s = [], None
    for i, b in enumerate(v):
        t = i / 100
        if not b and s is None and first < t < last:
            s = t
        elif b and s is not None:
            if t - s >= 0.05:
                gaps.append((s, t))
            s = None
    words = line['text'].split()
    sy = np.array([syl(w) for w in words], float)
    cum = np.concatenate([[0], np.cumsum(sy)])
    # anclas: índice de palabra -> tiempo de inicio
    anchors = {0: first, len(words): last}

    def expected(k):
        ks = sorted(anchors)
        lo = max(a for a in ks if a <= k); hi = min(a for a in ks if a >= k)
        if lo == hi:
            return anchors[lo]
        return anchors[lo] + (cum[k] - cum[lo]) / (cum[hi] - cum[lo]) * (anchors[hi] - anchors[lo])

    def snap(ks, tol, prefer_long):
        for k in ks:
            e = expected(k)
            cand = [g for g in gaps if abs((g[0] + g[1]) / 2 - e) < tol]
            if cand:
                g = max(cand, key=lambda g: g[1] - g[0]) if prefer_long else min(cand, key=lambda g: abs((g[0] + g[1]) / 2 - e))
                anchors[k] = g[1]
                gaps.remove(g)

    sent = [i + 1 for i, w in enumerate(words[:-1]) if w[-1] in '.:?']
    comma = [i + 1 for i, w in enumerate(words[:-1]) if w[-1] == ',']
    snap(sent, 1.2, True)
    snap(comma, 0.45, False)
    snap([k for k in range(1, len(words)) if k not in anchors], 0.12, False)
    res = []
    for k, w in enumerate(words):
        res.append({'w': w, 's': round(float(expected(k)), 3), 'e': round(float(expected(k + 1)), 3)})
    out.append({'id': line['id'], 'dur': round(len(x) / sr, 3), 'speech_end': round(last, 3), 'words': res})

json.dump(out, open('words.json', 'w'), ensure_ascii=False, indent=1)
for o in out:
    print(o['id'], ' '.join(f"{w['w']}@{w['s']:.2f}" for w in o['words']))
````

<!-- file: motion-graphics/template/timeline.py -->
````python
"""Línea de tiempo común a vídeo y sonido. Cada frase arranca en el pulso
(múltiplo de 15 fotogramas) con al menos 0,3 s de respiro tras la anterior."""
import json, math

FPS, BEAT, OPEN, SIGN = 30, 15, 45, 195
words = json.load(open('words.json'))
t, lines = OPEN, []
for l in words:
    start = t
    lines.append({'id': l['id'], 'start': start, 'dur': l['dur'],
                  'words': [{'w': w['w'], 'f': round(w['s'] * FPS)} for w in l['words']]})
    t = math.ceil((start + (l['speech_end'] + 0.3) * FPS) / BEAT) * BEAT
tl = {'fps': FPS, 'open': OPEN, 'lines': lines, 'sign': t, 'end': t + SIGN}
json.dump(tl, open('src/timeline.json', 'w'), ensure_ascii=False, indent=1)
print('cortes', [l['start'] for l in lines], 'firma', t, 'fin', t + SIGN, f'= {(t + SIGN) / FPS:.1f} s')
````

<!-- file: motion-graphics/template/score.py -->
````python
"""Banda sonora cinematográfica + locución para "Geolocalización inferencial".

Épica e inspiracional, 120 BPM, La menor con progresión vi–IV–I–V (Am–F–C–G).
Arco dramático anclado a la línea de tiempo (src/timeline.json):
  apertura   dron grave y platillo invertido hacia el golpe del 2027
  01 fecha   cuerdas suaves + piano; braam y timbal en "veintisiete"
  02-03      entra el ostinato de cuerdas; metales graves en cada compás
  04 señales crescendo: taikos, coro, riser hasta "ubicación estimada"
  05 usos    pleno: melodía de metales sobre la progresión inspiracional
  06 plazo   tensión: reloj, ostinato a semicorcheas, timbal en redoble
  07 pregunta se vacía: piano y pad; riser al zoom
  08 fuente  respiración antes del final
  firma      clímax: tutti en Do mayor, braam, campanas y cola larga
La música baja ~10 dB bajo la voz. Sin saturación. Master a -14 LUFS.
"""
import json
import os
import subprocess
import sys
import unicodedata
import wave

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR = 44100
TL = json.load(open('src/timeline.json'))
DUR = TL['end'] / 30.0
N = int(SR * DUR)
rng = np.random.default_rng(2027)
out = np.zeros((2, N))   # orquesta
perc = np.zeros((2, N))  # percusión (menos reverb)


def fr(frame):
    return frame / 30.0


def mf(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def t_(d):
    return np.arange(int(d * SR)) / SR


def flt(x, kind, f, order=2):
    if kind == 'bp':
        sos = butter(order, [f[0] / (SR / 2), min(f[1], SR / 2 - 100) / (SR / 2)], 'bandpass', output='sos')
    else:
        sos = butter(order, f / (SR / 2), kind, output='sos')
    return sosfilt(sos, x)


def put(sig, at, gain=1.0, pan=0.0, bus=None):
    bus = out if bus is None else bus
    i = int(at * SR)
    if i >= N or i < 0:
        return
    sig = sig[: N - i]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    bus[0, i:i + len(sig)] += sig * gain * l
    bus[1, i:i + len(sig)] += sig * gain * r


def env(d, a, r):
    t = t_(d)
    return np.minimum(1, t / max(a, 1e-4)) * np.minimum(1, np.maximum(0, (d - t) / max(r, 1e-4)))


def saw(freq, d, voices=(0.0,), vib=0.0):
    t = t_(d)
    s = np.zeros(len(t))
    for k, dt in enumerate(voices):
        f = freq * (1 + dt) * (1 + vib * np.sin(2 * np.pi * (5.2 + k * 0.3) * t))
        ph = np.cumsum(f) / SR + rng.random()
        s += 2 * (ph % 1) - 1
    return s / len(voices)


# ---------- instrumentos ----------
ENS = (-0.008, -0.003, 0.0, 0.004, 0.009)


def strings(notes, d, bright=2600, a=0.35, r=0.5):
    s = sum(saw(mf(m), d, ENS, vib=0.003) for m in notes) / len(notes)
    return flt(s, 'lp', bright) * env(d, a, r)


def spiccato(m, d=0.12, bright=3200):
    s = saw(mf(m), d, (-0.004, 0.0, 0.005)) + saw(mf(m + 12), d, (0.002,)) * 0.4
    return flt(s, 'lp', bright) * env(d, 0.004, d * 0.7) * np.exp(-t_(d) * 10)


def brass(notes, d, bright=1400, a=0.25):
    s = sum(saw(mf(m), d, (-0.003, 0.003), vib=0.002) for m in notes) / len(notes)
    e = env(d, a, 0.4)
    # el brillo crece con la dinámica: los metales "se abren"
    return (flt(s, 'lp', bright) * 0.6 + flt(s, 'lp', bright * 2.2) * 0.4 * e) * e


def choir(notes, d, a=0.8):
    s = sum(saw(mf(m), d, ENS, vib=0.004) for m in notes) / len(notes)
    v = flt(s, 'bp', (600, 1100)) * 0.8 + flt(s, 'bp', (1000, 1500)) * 0.5 + flt(s, 'lp', 400) * 0.5
    return v * env(d, a, 0.8)


def piano(m, d=2.5):
    t = t_(d)
    s = sum(np.sin(2 * np.pi * mf(m) * k * t) * (0.6 ** (k - 1)) * np.exp(-t * (1.5 + k)) for k in range(1, 6))
    return s * np.minimum(1, t / 0.003)


def bell(m, d=3.5):
    t = t_(d)
    s = sum(np.sin(2 * np.pi * mf(m) * r * t) * a * np.exp(-t * dk) for r, a, dk in ((1, 1, 1.2), (2.76, 0.4, 2.5), (5.4, 0.2, 4), (2, 0.3, 1.8)))
    return s * np.minimum(1, t / 0.002)


def timpani(m=33, g=1.0):
    t = t_(1.6)
    f = mf(m) * (1 + 0.15 * np.exp(-t * 30))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.2) + flt(rng.standard_normal(len(t)), 'lp', 900) * np.exp(-t * 25) * 0.4
    return s * g


def taiko(g=1.0):
    t = t_(0.9)
    f = 55 + 70 * np.exp(-t * 20)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6) + flt(rng.standard_normal(len(t)), 'bp', (150, 1800)) * np.exp(-t * 35) * 0.6
    return s * g


def braam(notes, d=2.6):
    s = sum(saw(mf(m), d, (-0.01, 0, 0.01)) for m in notes) / len(notes)
    sweep = np.linspace(300, 2400, len(s)) ** 1
    y = np.zeros(len(s))
    blk = 2048
    for i in range(0, len(s), blk):
        y[i:i + blk] = flt(s, 'lp', float(sweep[min(i, len(s) - 1)]))[i:i + blk]
    return y * env(d, 0.02, 1.2)


def sub_drop(d=1.8):
    t = t_(d)
    f = 70 * np.exp(-t * 1.5) + 28
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.6)


def riser(d, f0=300, f1=8000):
    t = t_(d)
    n = rng.standard_normal(len(t))
    y = np.zeros(len(t))
    steps = 24
    for k in range(steps):
        a, b = k * len(t) // steps, (k + 1) * len(t) // steps
        fc = f0 * (f1 / f0) ** (k / steps)
        y[a:b] = flt(n, 'bp', (fc * 0.7, fc * 1.4))[a:b]
    return y * (t / d) ** 2


def revcym(d=1.5):
    t = t_(d)
    return flt(rng.standard_normal(len(t)), 'hp', 4000) * (t / d) ** 3


def tick():
    t = t_(0.05)
    return flt(rng.standard_normal(len(t)), 'bp', (2500, 6000)) * np.exp(-t * 120)


def roll(d, g=1.0):
    """Redoble de timbal que crece."""
    y = np.zeros(int(d * SR) + SR)
    step = 0.0625
    k = 0
    while k * step < d:
        tm = timpani(33, 0.25 + 0.75 * (k * step / d))
        i = int(k * step * SR)
        y[i:i + len(tm)] += tm[: len(y) - i] * 0.5
        k += 1
    return y * g


# ---------- utilidades de la línea de tiempo ----------
def norm(s):
    s = unicodedata.normalize('NFD', s.lower())
    return ''.join(c for c in s if c.isalnum() and unicodedata.category(c) != 'Mn')


def cue(lid, word, nth=0):
    """Fotograma global de una palabra; mismo cálculo que wf() en src/tl.ts (admite 'a|b')."""
    l = next(x for x in TL['lines'] if x['id'] == lid)
    for alt in word.split('|'):
        hits = [w for w in l['words'] if norm(w['w']).startswith(norm(alt))]
        if len(hits) > nth:
            return l['start'] + hits[nth]['f']
    raise KeyError(word)


def start(lid):
    return next(x for x in TL['lines'] if x['id'] == lid)['start']


SIGN, END = TL['sign'], TL['end']
S = {lid: fr(start(lid)) for lid in ('01', '02', '03', '04', '05', '06', '07', '08')}
BAR = 2.0  # 4 pulsos a 120 BPM
PROG = [  # (bajo, acorde) vi–IV–I–V
    (45, [57, 60, 64]),
    (41, [53, 57, 60]),
    (48, [55, 60, 64]),
    (43, [55, 59, 62]),
]


def section(t0, t1, fn):
    """Llama fn(t, k, bajo, acorde, dur) en cada compás de [t0, t1)."""
    t, k = t0, 0
    while t < t1 - 0.05:
        bass, chord = PROG[k % 4]
        fn(t, k, bass, chord, min(BAR, t1 - t))
        t += BAR
        k += 1


# ---------- apertura ----------
put(strings([33, 45], fr(TL['open']) + 1.5, 900, a=1.0), 0, 0.30)
put(revcym(fr(cue('01', 'veintisiete'))), 0, 0.10)

# ---------- 01: la fecha ----------
put(strings([57, 60, 64], S['02'] - S['01'] + 0.5, 1800, a=0.8), S['01'], 0.16, -0.2)
for j, m in enumerate((69, 72, 76, 74)):
    put(piano(m), S['01'] + 0.2 + j * 0.5, 0.10, 0.2)
c = fr(cue('01', 'veintisiete'))
put(braam([33, 45, 52]), c, 0.30)
put(timpani(33, 1.0), c, 0.45, bus=perc)
put(sub_drop(), c, 0.35, bus=perc)
put(timpani(40, 0.6), fr(cue('01', 'plazo')), 0.30, bus=perc)


# ---------- 02-03: ostinato y metales ----------
def ost(t, k, bass, chord, d, g=0.06, density=8):
    pat = [chord[0], chord[1], chord[2], chord[1]]
    for i in range(int(d * density / 2)):
        put(spiccato(pat[i % 4] + 12), t + i * (2 / density), g, 0.35 if i % 2 else -0.35)


def low(t, k, bass, chord, d, g=0.14):
    put(strings([bass - 12, bass], d + 0.3, 700, a=0.3), t, g)


def horns(t, k, bass, chord, d, g=0.07):
    put(brass([chord[0] - 12, chord[1] - 12], d, 1100, a=0.6), t, g, 0.1)


section(S['02'], S['04'], lambda *a: (ost(*a, g=0.045), low(*a)))
section(S['03'], S['04'], lambda *a: horns(*a))
for w in [cue('02', 'cincuenta'), cue('03', 'catorce')]:
    put(braam([33, 45, 52], 2.0), fr(w), 0.22)
    put(timpani(33), fr(w), 0.40, bus=perc)
put(taiko(1.0), fr(cue('02', 'ya')), 0.35, bus=perc)
put(bell(76, 2.0), fr(cue('02', 'ya')), 0.05)
put(timpani(40, 0.6), fr(cue('03', 'primaria')), 0.25, bus=perc)
for w in ('solicitante', 'dispositivo'):
    put(bell(81, 1.5), fr(cue('03', w)) + 0.1, 0.035, 0.3)

# ---------- 04: crescendo de las señales ----------
section(S['04'], S['05'], lambda *a: (ost(*a, g=0.06, density=16), low(*a, g=0.16), horns(*a, g=0.09)))
section(S['04'], S['05'], lambda t, k, b, c_, d: put(choir([c_[0], c_[1] + 12, c_[2]], d + 0.4, a=0.5), t, 0.07))
t = S['04']
while t < S['05'] - 0.1:
    put(taiko(0.8), t, 0.22, -0.2, bus=perc)
    put(taiko(0.5), t + 0.75, 0.14, 0.2, bus=perc)
    t += BAR
for j, w in enumerate(('dirección', 'tipo', 'proveedor', 'vpn', 'proxies', 'redes', 'zona', 'configuración')):
    put(bell(76 + [0, 3, 7, 10, 12, 15, 19, 22][j], 1.4), fr(cue('04', w)) + 0.13, 0.03, ((j % 3) - 1) * 0.4)
res = fr(cue('04', 'dispositivo')) + 0.2
put(riser(res - S['04'] - 4.0, 400, 9000), S['04'] + 4.0, 0.10)
put(braam([33, 45, 52, 57]), res, 0.28)
put(timpani(33, 1.0), res, 0.45, bus=perc)

# ---------- 05: pleno, melodía inspiracional ----------
MEL = [(76, 1.0), (74, 0.5), (72, 0.5), (72, 1.0), (69, 1.0), (72, 1.0), (74, 1.0), (79, 1.5), (76, 0.5)]


def full(t, k, bass, chord, d):
    ost(t, k, bass, chord, d, g=0.06, density=16)
    low(t, k, bass, chord, d, g=0.18)
    put(strings([chord[0] + 12, chord[1] + 12, chord[2] + 12], d + 0.3, 3000, a=0.2), t, 0.08, 0.2)
    put(brass([chord[0], chord[1], chord[2]], d, 1600, a=0.15), t, 0.08, -0.15)
    put(taiko(1.0), t, 0.24, bus=perc)
    put(timpani(bass - 12 + 24, 0.6), t + 1.0, 0.18, bus=perc)


section(S['05'], S['06'], full)
t = S['05'] + 0.5
for m, d in MEL * 2:
    if t + d > S['06']:
        break
    put(brass([m - 12], d * 0.98, 2000, a=0.08), t, 0.10, 0.1)
    t += d
put(braam([33, 45, 52]), fr(cue('05', 'dos')), 0.20)
put(timpani(33), fr(cue('05', 'frenar')), 0.30, bus=perc)

# ---------- 06: tensión del plazo ----------
section(S['06'], S['07'], lambda *a: (ost(*a, g=0.055, density=16), low(*a, g=0.15)))
put(braam([33, 45, 52]), fr(cue('06', 'nueve')), 0.26)
put(timpani(33), fr(cue('06', 'nueve')), 0.42, bus=perc)
t = S['06']
while t < S['07'] - 0.1:
    put(tick(), t, 0.10, 0.4, bus=perc)
    t += 0.5
put(roll(S['07'] - S['06'] - 0.4, 0.5), S['06'] + 0.2, 0.20, bus=perc)
for w in ('decidir', 'integrar', 'calibrar', 'documentar'):
    put(taiko(0.7), fr(cue('06', w)), 0.20, bus=perc)

# ---------- 07: vacío y pregunta ----------
put(strings([45, 57, 64], S['08'] - S['07'], 1200, a=0.4), S['07'], 0.12)
for j, m in enumerate((69, 72, 76, 72, 74, 71)):
    put(piano(m, 2.0), S['07'] + 0.25 + j * 0.75, 0.09, 0.15)
put(bell(76, 2.0), fr(cue('07', 'tecnología')), 0.04, -0.4)
put(bell(79, 2.0), fr(cue('07', 'cumplimiento')), 0.04, 0.4)
zoom = start('08')
put(riser(22 / 30 + 0.6, 300, 12000), fr(zoom) - 22 / 30 - 0.6, 0.14)
put(revcym(0.9), fr(zoom) - 0.9, 0.10)

# ---------- 08: respiración ----------
put(strings([48, 55, 64, 67], fr(SIGN) - S['08'] + 0.4, 1600, a=0.6), S['08'], 0.12)
put(choir([60, 64, 67], fr(SIGN) - S['08'] + 0.4, a=1.2), S['08'], 0.05)
put(roll(1.6, 0.6), fr(SIGN + 42) - 1.6, 0.25, bus=perc)

# ---------- firma: clímax ----------
B = fr(SIGN + 42)
tail = DUR - B
put(braam([36, 48, 55, 60]), B, 0.32)
put(timpani(36, 1.0), B, 0.5, bus=perc)
put(taiko(1.0), B, 0.4, bus=perc)
put(sub_drop(2.5), B, 0.35, bus=perc)
put(strings([36, 48, 55, 60, 64, 67, 72], tail, 3200, a=0.15, r=2.0), B, 0.22)
put(brass([48, 55, 60, 64], tail, 2200, a=0.2), B, 0.12)
put(choir([60, 64, 67, 72], tail, a=0.5), B, 0.08)
for j, m in enumerate((72, 76, 79, 84, 88)):
    put(bell(m, 4.0), B + j * 0.08, 0.05, (j - 2) * 0.3)
put(piano(72, 3.0), DUR - 3.2, 0.06)

# ---------- reverb de sala ----------
ir_t = t_(3.4)
ir = rng.standard_normal((2, len(ir_t))) * np.exp(-ir_t * 1.9)
ir[:, : int(0.02 * SR)] *= np.linspace(0, 1, int(0.02 * SR))
wet = np.stack([fftconvolve(out[c] + perc[c] * 0.4, ir[c])[:N] for c in range(2)]) * 0.010
music = out + perc + wet

# ---------- locución ----------
VOICE_DIR = os.environ.get('VOICE_DIR', 'voice')
voice = np.zeros(N)
for l in TL['lines']:
    vp = f"{VOICE_DIR}/{l['id']}.wav"
    if not os.path.exists(vp):
        continue  # sin voz: solo música
    w = wave.open(vp)
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
    if w.getnchannels() == 2:
        x = x.reshape(-1, 2).mean(1)
    if w.getframerate() != SR:
        x = np.interp(np.arange(int(len(x) * SR / w.getframerate())) * w.getframerate() / SR, np.arange(len(x)), x)
    i0 = int(fr(l['start']) * SR)
    voice[i0:i0 + len(x)] += x[: N - i0]
voice *= 0.9 / max(np.max(np.abs(voice)), 1e-9) if np.any(voice) else 0

# la música baja bajo la voz (envolvente de 150 ms) y respira entre frases
envl = np.convolve(np.abs(voice), np.ones(int(0.15 * SR)) / int(0.15 * SR), mode='same')
gate = np.clip(envl / 0.02, 0, 1)
music *= 1 - 0.66 * gate
music *= 0.5 / (np.max(np.abs(music)) + 1e-9)

mix = music * 0.9 + voice[None, :]
fade = np.ones(N)
fl = int(1.5 * SR)
fade[-fl:] = np.linspace(1, 0, fl) ** 2
mix *= fade
mix *= 0.89 / np.max(np.abs(mix))

path = sys.argv[1] if len(sys.argv) > 1 else 'public/mix.wav'
tmp = path + '.tmp.wav'
with wave.open(tmp, 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix.T * 32767).astype(np.int16).tobytes())
# sonoridad de redes: -14 LUFS, pico real -1,5 dBTP
subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', tmp, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', str(SR), path], check=True)
os.remove(tmp)
print('ok', path)
````

<!-- file: motion-graphics/template/review.mjs -->
````js
// Renderiza fotogramas sueltos con un solo bundle: node review.mjs 30 60 90 ...
import {bundle} from '@remotion/bundler';
import {selectComposition, renderStill} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';

const frames = process.argv.slice(2).map(Number);
const CHROME = '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell';
const browserExecutable = fs.existsSync(CHROME) ? CHROME : undefined;
fs.mkdirSync(process.env.OUTDIR ?? 'out/frames', {recursive: true});
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts')});
const composition = await selectComposition({serveUrl, id: process.env.COMP ?? 'Geo-1x1', browserExecutable});
for (const frame of frames) {
  await renderStill({serveUrl, composition, frame, output: `${process.env.OUTDIR ?? "out/frames"}/${process.env.COMP ?? ""}f${String(frame).padStart(3, '0')}.png`, browserExecutable, chromiumOptions: {gl: 'swangle'}});
  console.log('ok', frame);
}
````

<!-- file: motion-graphics/template/sheet.sh -->
````bash
#!/bin/bash
# Hoja de contactos: fotogramas indicados, en rejilla de 4 columnas a 480 px
# Uso: ./sheet.sh video.mp4 salida.png 30 60 90 ...
v=$1; o=$2; shift 2
tmp=$(mktemp -d)
i=0
for f in "$@"; do
  ffmpeg -nostdin -loglevel error -y -i "$v" -vf "select=eq(n\,$f),scale=480:-1,drawtext=text='f$f':x=8:y=8:fontsize=22:fontcolor=white:box=1:boxcolor=black@0.6" -frames:v 1 "$tmp/$(printf %03d $i).png"
  i=$((i+1))
done
ffmpeg -nostdin -loglevel error -y -pattern_type glob -i "$tmp/*.png" -vf "tile=4x$(( (i+3)/4 ))" -frames:v 1 "$o"
rm -rf "$tmp"
````

<!-- file: motion-graphics/recipes/showreel/README.md -->
````markdown
# Recetas del showreel (16:9, 1920×1080, sin voz)

Escenas sueltas del showreel aprobado. Usan `theme.ts` y `ui.tsx` de esta
carpeta (versión 16:9, con `CUTS` a 120 BPM). Para llevarlas a la plantilla,
cambia coordenadas a 1080×1080 y usa los componentes de `template/src/ui.tsx`.

| Archivo | Técnica |
|---|---|
| S1ColdOpen | línea → punto, letras con muelle, golpe "CUENTA." con onda |
| S2Kinetic | palabras en máscara desde lados alternos, eco en contorno, inversión de color en el pulso |
| S3Shapes | morph por puntos muestreados + rejilla de puntos con ruido y ondas |
| S4Data | matriz de riesgo 5×5, escáner, alerta, KPIs, curva con `evolvePath` |
| S5Depth | tarjetas 3D en fila, suelo en perspectiva, sello VERIFICADO |
| S6ZoomThrough | zoom a través de la "O" de MOTION con líneas de velocidad |
| S7Resolve | partículas que forman un anillo elíptico y logotipo con brillo |
| Showreel.tsx | montaje: secuencias, destellos, HUD, grano |
````

<!-- file: motion-graphics/recipes/showreel/theme.ts -->
````tsx
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

// Cortes alineados al pulso de 120 BPM (1 pulso = 15 fotogramas)
export const CUTS = {
  open: 0,
  type: 90,
  shapes: 210,
  data: 330,
  depth: 480,
  zoom: 600,
  logo: 690,
  end: 900,
};

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
````

<!-- file: motion-graphics/recipes/showreel/ui.tsx -->
````tsx
import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C, FONT, FPS, ease} from './theme';

// Rótulo de sección: llega con barra dorada que se estira y texto que sube por máscara
export const SectionLabel: React.FC<{n: string; title: string; dark?: boolean; at?: number}> = ({
  n,
  title,
  dark,
  at = 4,
}) => {
  const f = useCurrentFrame();
  const bar = ease(f, at, at + 14);
  const txt = ease(f, at + 4, at + 20);
  const col = dark ? C.navy : C.white;
  return (
    <div style={{position: 'absolute', left: 120, top: 104, fontFamily: FONT, display: 'flex', alignItems: 'center', gap: 22}}>
      <div style={{width: 64 * bar, height: 3, background: dark ? C.navy : C.gold}} />
      <div style={{overflow: 'hidden', height: 34}}>
        <div style={{transform: `translateY(${(1 - txt) * 34}px)`, color: col, fontSize: 24, fontWeight: 700, letterSpacing: 6, textTransform: 'uppercase'}}>
          <span style={{color: dark ? C.navy : C.gold}}>{n}</span>
          <span style={{opacity: 0.85}}> — {title}</span>
        </div>
      </div>
    </div>
  );
};

const pad = (n: number) => String(n).padStart(2, '0');

// Capa de "sala de edición": código de tiempo, esquinas de zona segura y grano
export const EditorHud: React.FC = () => {
  const f = useCurrentFrame();
  const s = Math.floor(f / FPS);
  const tc = `00:00:${pad(s)}:${pad(f % FPS)}`;
  const on = ease(f, 6, 24);
  const corner = (r: number, x: number, y: number) => (
    <div
      key={r}
      style={{
        position: 'absolute',
        left: x,
        top: y,
        width: 46,
        height: 46,
        borderTop: `2px solid ${C.mute}`,
        borderLeft: `2px solid ${C.mute}`,
        transform: `rotate(${r}deg)`,
        opacity: 0.45 * on,
      }}
    />
  );
  return (
    <AbsoluteFill style={{pointerEvents: 'none', fontFamily: FONT}}>
      {corner(0, 56, 56)}
      {corner(90, 1818, 56)}
      {corner(180, 1818, 978)}
      {corner(270, 56, 978)}
      <div style={{position: 'absolute', left: 120, bottom: 66, color: C.mute, fontSize: 20, fontWeight: 600, letterSpacing: 4, opacity: 0.8 * on, fontVariantNumeric: 'tabular-nums'}}>
        TC {tc}
      </div>
      <div style={{position: 'absolute', right: 120, bottom: 66, color: C.mute, fontSize: 20, fontWeight: 600, letterSpacing: 4, opacity: 0.8 * on, display: 'flex', alignItems: 'center', gap: 12}}>
        <div style={{width: 12, height: 12, borderRadius: 6, background: C.coral, opacity: Math.floor(f / 15) % 2 ? 0.35 : 1}} />
        1920×1080 · 30 FPS
      </div>
    </AbsoluteFill>
  );
};

export const Grain: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{pointerEvents: 'none', mixBlendMode: 'overlay', opacity: 0.16}}>
      <svg width="1920" height="1080">
        <filter id="g">
          <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed={f % 12} />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width="1920" height="1080" filter="url(#g)" />
      </svg>
    </AbsoluteFill>
  );
};

export const Vignette: React.FC = () => (
  <AbsoluteFill style={{pointerEvents: 'none', background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,0.55) 100%)'}} />
);

// Destello de corte: sube en 2 fotogramas y cae en 6
export const Flash: React.FC<{at: number; color?: string; max?: number}> = ({at, color = C.white, max = 0.7}) => {
  const f = useCurrentFrame();
  const o = f < at ? ease(f, at - 2, at, [0, max]) : ease(f, at, at + 6, [max, 0]);
  if (o <= 0) return null;
  return <AbsoluteFill style={{background: color, opacity: o, pointerEvents: 'none'}} />;
};
````

<!-- file: motion-graphics/recipes/showreel/Showreel.tsx -->
````tsx
import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile} from 'remotion';
import {CUTS, C} from './theme';
import {loadFonts} from './fonts';
import {EditorHud, Flash, Grain, Vignette} from './ui';
import {S1ColdOpen} from './scenes/S1ColdOpen';
import {S2Kinetic} from './scenes/S2Kinetic';
import {S3Shapes} from './scenes/S3Shapes';
import {S4Data} from './scenes/S4Data';
import {S5Depth} from './scenes/S5Depth';
import {S6ZoomThrough} from './scenes/S6ZoomThrough';
import {S7Resolve} from './scenes/S7Resolve';

loadFonts();

const SCENES = [
  {from: CUTS.open, to: CUTS.type, C: S1ColdOpen},
  {from: CUTS.type, to: CUTS.shapes, C: S2Kinetic},
  {from: CUTS.shapes, to: CUTS.data, C: S3Shapes},
  {from: CUTS.data, to: CUTS.depth, C: S4Data},
  {from: CUTS.depth, to: CUTS.zoom, C: S5Depth},
  {from: CUTS.zoom, to: CUTS.logo, C: S6ZoomThrough},
  {from: CUTS.logo, to: CUTS.end, C: S7Resolve},
];

export const Showreel: React.FC = () => (
  <AbsoluteFill style={{background: C.navy}}>
    {SCENES.map(({from, to, C: Scene}) => (
      <Sequence key={from} from={from} durationInFrames={to - from}>
        <Scene />
      </Sequence>
    ))}

    <Flash at={CUTS.type} />
    <Flash at={CUTS.depth} color={C.goldL} max={0.5} />
    <Flash at={CUTS.logo + 61} color={C.goldL} max={0.55} />

    <Vignette />
    <Grain />
    <Sequence from={CUTS.type} durationInFrames={CUTS.logo - CUTS.type}>
      <EditorHud />
    </Sequence>

    <Audio src={staticFile('score.wav')} />
  </AbsoluteFill>
);
````

<!-- file: motion-graphics/recipes/showreel/scenes/S1ColdOpen.tsx -->
````tsx
import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C, FONT, IN, ease, gold, shake, sp} from '../theme';

const LINE1 = 'CADA FOTOGRAMA';
const IMPACT = 58;

export const S1ColdOpen: React.FC = () => {
  const f = useCurrentFrame();

  // Línea dorada: crece desde el centro y colapsa a un punto
  const grow = ease(f, 0, 18);
  const collapse = ease(f, 20, 32, [0, 1], IN);
  const lineW = 1400 * grow * (1 - collapse);
  const dot = ease(f, 26, 34) * (1 - ease(f, 34, 42));

  // Golpe de "CUENTA."
  const slam = sp(f, IMPACT - 6, {damping: 12, stiffness: 260, mass: 0.6});
  const sh = shake(f, IMPACT, 22, 16);
  const wave = ease(f, IMPACT, IMPACT + 26);

  // Salida hacia el corte
  const exit = ease(f, 78, 90, [0, 1], IN);

  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: FONT}}>
      <AbsoluteFill
        style={{
          transform: `translate(${sh.x}px, ${sh.y}px) scale(${1 + exit * 0.18})`,
          filter: `blur(${exit * 14}px)`,
          opacity: 1 - exit * 0.6,
        }}
      >
        {/* línea y punto */}
        <div style={{position: 'absolute', left: 960 - lineW / 2, top: 539, width: lineW, height: 3, background: gold, boxShadow: `0 0 24px ${C.gold}`}} />
        <div style={{position: 'absolute', left: 960 - 9, top: 531, width: 18, height: 18, borderRadius: 9, background: C.goldL, transform: `scale(${dot * 1.4})`, boxShadow: `0 0 40px ${C.goldL}`}} />

        {/* onda expansiva */}
        {f >= IMPACT && (
          <svg width="1920" height="1080" style={{position: 'absolute'}}>
            {[0, 7].map((d) => {
              const w = ease(f, IMPACT + d, IMPACT + d + 30);
              return <circle key={d} cx="960" cy="610" r={80 + w * 1000} fill="none" stroke={C.gold} strokeWidth={10 * (1 - w)} opacity={1 - w} />;
            })}
          </svg>
        )}

        {/* CADA FOTOGRAMA: letra a letra */}
        <div style={{position: 'absolute', top: 360, width: '100%', display: 'flex', justifyContent: 'center'}}>
          {LINE1.split('').map((ch, i) => {
            const p = sp(f, 30 + i * 1.5, {damping: 14, stiffness: 180});
            return (
              <span
                key={i}
                style={{
                  display: 'inline-block',
                  minWidth: ch === ' ' ? 40 : undefined,
                  fontSize: 120,
                  fontWeight: 900,
                  letterSpacing: 6,
                  color: C.white,
                  opacity: Math.min(1, p * 1.4),
                  transform: `translateY(${(1 - p) * 70}px) rotate(${(1 - p) * 8}deg)`,
                  filter: `blur(${(1 - Math.min(1, p)) * 10}px)`,
                }}
              >
                {ch}
              </span>
            );
          })}
        </div>

        {/* CUENTA. */}
        <div
          style={{
            position: 'absolute',
            top: 500,
            width: '100%',
            textAlign: 'center',
            fontSize: 210,
            fontWeight: 900,
            letterSpacing: 4,
            backgroundImage: gold,
            WebkitBackgroundClip: 'text',
            color: 'transparent',
            opacity: f < IMPACT - 6 ? 0 : 1,
            transform: `scale(${3 - 2 * slam})`,
          }}
        >
          CUENTA.
        </div>
        <div style={{position: 'absolute', top: 760, width: '100%', textAlign: 'center', color: C.mute, fontSize: 26, fontWeight: 600, letterSpacing: 10, opacity: ease(f, 64, 76)}}>
          MOTION GRAPHICS · SHOWREEL
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
````

<!-- file: motion-graphics/recipes/showreel/scenes/S2Kinetic.tsx -->
````tsx
import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C, FONT, IN, ease, shake, sp} from '../theme';
import {SectionLabel} from '../ui';

const WORDS = [
  {t: 'RITMO', dir: -1},
  {t: 'PRECISIÓN', dir: 1},
  {t: 'IMPACTO', dir: -1},
];

const BEAT = 75; // inversión de color en el pulso
const BEAT_END = 99;

export const S2Kinetic: React.FC = () => {
  const f = useCurrentFrame();
  const inverted = f >= BEAT && f < BEAT_END;
  const bg = inverted ? C.gold : C.navy;
  const fg = inverted ? C.navy : C.white;
  const sh = shake(f, BEAT, 14, 10);

  return (
    <AbsoluteFill style={{background: bg, fontFamily: FONT}}>
      {/* franjas diagonales que barren el fondo */}
      <AbsoluteFill style={{overflow: 'hidden', opacity: inverted ? 0.12 : 0.06}}>
        {Array.from({length: 14}).map((_, i) => (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: -400 + i * 190 + ((f * 3) % 190),
              top: -200,
              width: 60,
              height: 1600,
              background: fg,
              transform: 'rotate(24deg)',
            }}
          />
        ))}
      </AbsoluteFill>

      <AbsoluteFill style={{transform: `translate(${sh.x}px, ${sh.y}px)`, justifyContent: 'center'}}>
        {WORDS.map((w, i) => {
          const p = sp(f, 6 + i * 12, {damping: 18, stiffness: 140});
          const lag = sp(f, 12 + i * 12, {damping: 26, stiffness: 70});
          const out = ease(f, 104 + i * 3, 116 + i * 3, [0, 1], IN);
          const underline = ease(f, BEAT + i * 3, BEAT + 12 + i * 3);
          return (
            <div key={w.t} style={{position: 'relative', height: 236, overflow: 'hidden', margin: '0 auto', width: 1700}}>
              {/* eco en contorno, con retardo: da profundidad */}
              <div
                style={{
                  position: 'absolute',
                  inset: 0,
                  textAlign: 'center',
                  fontSize: 230,
                  fontWeight: 900,
                  lineHeight: '236px',
                  color: 'transparent',
                  WebkitTextStroke: `2px ${inverted ? C.navy : C.gold}`,
                  opacity: 0.55,
                  transform: `translateX(${(1 - lag) * w.dir * 1900 + 26}px) translateY(${-out * 240}px)`,
                }}
              >
                {w.t}
              </div>
              <div
                style={{
                  position: 'absolute',
                  inset: 0,
                  textAlign: 'center',
                  fontSize: 230,
                  fontWeight: 900,
                  lineHeight: '236px',
                  color: i === 1 && !inverted ? C.gold : fg,
                  transform: `translateX(${(1 - p) * w.dir * 1900}px) translateY(${-out * 240}px) skewX(${(1 - p) * w.dir * -18}deg)`,
                }}
              >
                {w.t}
              </div>
              <div style={{position: 'absolute', bottom: 10, left: 850 - 300 * underline, width: 600 * underline, height: 8, background: fg}} />
            </div>
          );
        })}
      </AbsoluteFill>

      <SectionLabel n="01" title="Tipografía cinética" dark={inverted} />
    </AbsoluteFill>
  );
};
````

<!-- file: motion-graphics/recipes/showreel/scenes/S3Shapes.tsx -->
````tsx
import React from 'react';
import {AbsoluteFill, interpolateColors, useCurrentFrame} from 'remotion';
import {getLength, getPointAtLength, translatePath} from '@remotion/paths';
import {makeCircle, makePolygon, makeRect, makeStar, makeTriangle} from '@remotion/shapes';
import {noise3D} from '@remotion/noise';
import {C, FONT, IN, INOUT, ease, sp} from '../theme';
import {SectionLabel} from '../ui';

const BOX = 460;
const centered = (s: {path: string; width: number; height: number}) =>
  translatePath(s.path, (BOX - s.width) / 2, (BOX - s.height) / 2);

const SHAPES = [
  centered(makeCircle({radius: 190})),
  centered(makeRect({width: 340, height: 340, cornerRadius: 36})),
  centered(makeTriangle({length: 430, direction: 'up', cornerRadius: 24})),
  centered(makePolygon({points: 6, radius: 205, cornerRadius: 20})),
  centered(makeStar({points: 5, innerRadius: 95, outerRadius: 220, cornerRadius: 14})),
  centered(makeCircle({radius: 190})),
];
const MORPHS = [14, 34, 54, 74, 92]; // inicio de cada transformación
const MORPH_LEN = 12;

// Morph por puntos: cada forma se muestrea con el mismo número de puntos y se
// alinea el punto de arranque con la forma anterior para que no se retuerza.
const SAMPLES = 144;
type Pt = {x: number; y: number};
const sample = (d: string): Pt[] => {
  const len = getLength(d);
  return Array.from({length: SAMPLES}, (_, i) => getPointAtLength(d, (i / SAMPLES) * len) ?? {x: 0, y: 0});
};
const align = (a: Pt[], b: Pt[]): Pt[] => {
  let best = 0;
  let bestD = Infinity;
  for (let sh = 0; sh < SAMPLES; sh++) {
    let d = 0;
    for (let i = 0; i < SAMPLES; i += 4) {
      const q = b[(i + sh) % SAMPLES];
      d += (a[i].x - q.x) ** 2 + (a[i].y - q.y) ** 2;
    }
    if (d < bestD) {
      bestD = d;
      best = sh;
    }
  }
  return b.map((_, i) => b[(i + best) % SAMPLES]);
};
const PTS: Pt[][] = [];
SHAPES.forEach((d, i) => PTS.push(i === 0 ? sample(d) : align(PTS[i - 1], sample(d))));
const toPath = (pts: Pt[]) => 'M ' + pts.map((p) => `${p.x.toFixed(2)} ${p.y.toFixed(2)}`).join(' L ') + ' Z';
const lerpPts = (a: Pt[], b: Pt[], t: number) => a.map((p, i) => ({x: p.x + (b[i].x - p.x) * t, y: p.y + (b[i].y - p.y) * t}));

const shapeAt = (f: number) => {
  for (let i = MORPHS.length - 1; i >= 0; i--) {
    if (f >= MORPHS[i]) {
      const p = ease(f, MORPHS[i], MORPHS[i] + MORPH_LEN, [0, 1], INOUT);
      return toPath(lerpPts(PTS[i], PTS[i + 1], p));
    }
  }
  return toPath(PTS[0]);
};

const COLS = 32;
const ROWS = 18;
const GAP = 60;

export const S3Shapes: React.FC = () => {
  const f = useCurrentFrame();
  const enter = sp(f, 0, {damping: 12, stiffness: 120});
  // pequeño rebote al final de cada transformación
  const pop = MORPHS.reduce((acc, t) => acc + (sp(f, t + MORPH_LEN - 4, {damping: 8, stiffness: 300}) - sp(f, t + MORPH_LEN + 2, {damping: 8, stiffness: 300})) * 0.12, 0);
  const rot = ease(f, 0, 104, [-20, 70], INOUT);

  const exit = ease(f, 104, 120, [0, 1], IN);
  const fill = interpolateColors(exit, [0, 0.5], [C.gold, C.navy2]);
  const shape = shapeAt(f);
  const scale = (0.2 + 0.8 * enter + pop) * (1 + exit * 13);

  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: FONT}}>
      {/* rejilla de puntos: ruido + ondas en cada transformación */}
      <svg width="1920" height="1080" style={{position: 'absolute', opacity: 1 - exit}}>
        {Array.from({length: COLS * ROWS}).map((_, k) => {
          const c = k % COLS;
          const r = Math.floor(k / COLS);
          const x = 960 + (c - (COLS - 1) / 2) * GAP;
          const y = 540 + (r - (ROWS - 1) / 2) * GAP;
          const d = Math.hypot(x - 960, y - 540);
          const n = (noise3D('grid', c * 0.13, r * 0.13, f * 0.025) + 1) / 2;
          let bump = 0;
          for (const t of MORPHS) {
            const age = f - t;
            if (age < 0 || age > 40) continue;
            bump += Math.exp(-(((d - age * 30) / 70) ** 2)) * (1 - age / 40);
          }
          const appear = ease(f, d / 40, d / 40 + 10);
          return (
            <circle
              key={k}
              cx={x}
              cy={y}
              r={(1.5 + n * 2.5 + bump * 5) * appear}
              fill={bump > 0.15 ? C.goldL : C.mute}
              opacity={0.25 + n * 0.3 + bump * 0.5}
            />
          );
        })}
      </svg>

      {/* órbita con satélites */}
      <svg width="1920" height="1080" style={{position: 'absolute', opacity: enter * (1 - exit)}}>
        <circle cx="960" cy="540" r="340" fill="none" stroke={C.mute} strokeOpacity={0.35} strokeWidth={2} strokeDasharray="4 14" transform={`rotate(${f * 0.8} 960 540)`} />
        {[0, 1, 2].map((i) => {
          const a = ((f * 2.4 + i * 120) * Math.PI) / 180;
          return <circle key={i} cx={960 + Math.cos(a) * 340} cy={540 + Math.sin(a) * 340} r={i === 0 ? 10 : 6} fill={i === 0 ? C.teal : C.gold} />;
        })}
      </svg>

      {/* forma principal */}
      <div style={{position: 'absolute', left: 960 - BOX / 2, top: 540 - BOX / 2, width: BOX, height: BOX, transform: `scale(${scale}) rotate(${rot}deg)`}}>
        <svg width={BOX} height={BOX} style={{overflow: 'visible'}}>
          <defs>
            <linearGradient id="gg" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0" stopColor={exit > 0 ? fill : C.goldL} />
              <stop offset="1" stopColor={exit > 0 ? fill : C.goldD} />
            </linearGradient>
          </defs>
          <path d={shape} fill="url(#gg)" />
          <path d={shape} fill="none" stroke={C.cream} strokeOpacity={0.5 * (1 - exit)} strokeWidth={3} transform={`translate(${BOX / 2} ${BOX / 2}) scale(1.12) translate(${-BOX / 2} ${-BOX / 2})`} />
        </svg>
      </div>

      <div style={{opacity: 1 - exit}}>
        <SectionLabel n="02" title="Morphing y geometría" />
      </div>
    </AbsoluteFill>
  );
};
````

<!-- file: motion-graphics/recipes/showreel/scenes/S4Data.tsx -->
````tsx
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
````

<!-- file: motion-graphics/recipes/showreel/scenes/S5Depth.tsx -->
````tsx
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
  const orbit = ease(f, 0, 100, [-20, 12], INOUT);
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
              left: 64,
              bottom: 70,
              padding: '14px 26px',
              border: `6px solid ${C.coral}`,
              borderRadius: 12,
              color: C.coral,
              fontSize: 44,
              fontWeight: 900,
              letterSpacing: 5,
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
          const x = (i - 1) * 600;
          const a = (1 - i) * 22;
          const z = i === 1 ? 120 : -120;
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
                transform: `translateX(${x}px) translateZ(${z + fly * 2400}px) rotateY(${a}deg) translateY(${(1 - pop) * 500}px)`,
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
````

<!-- file: motion-graphics/recipes/showreel/scenes/S6ZoomThrough.tsx -->
````tsx
import React from 'react';
import {AbsoluteFill, Easing, useCurrentFrame} from 'remotion';
import {C, FONT, ease, sp} from '../theme';
import {SectionLabel} from '../ui';

// Cajas de ancho conocido por letra: la "O" queda en una posición conocida para el zoom
const LETTERS = ['M', 'O', 'T', 'I', 'O', 'N'];
const WIDTHS = [290, 262, 206, 118, 262, 254]; // avance óptico de Nunito Sans Black a 300 px
const TOTAL = WIDTHS.reduce((a, b) => a + b, 0);
const LEFTS = WIDTHS.map((_, i) => 960 - TOTAL / 2 + WIDTHS.slice(0, i).reduce((a, b) => a + b, 0));
const RING_X = LEFTS[1] + WIDTHS[1] / 2;
const RING_Y = 540;
const ZOOM_IN = 42;
const ZOOM_OUT = 84;

export const S6ZoomThrough: React.FC = () => {
  const f = useCurrentFrame();
  const z = ease(f, ZOOM_IN, ZOOM_OUT, [0, 1], Easing.in(Easing.exp));
  const scale = 1 + z * 90;
  const speed = ease(f, ZOOM_IN + 10, ZOOM_OUT - 4);

  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: FONT, overflow: 'hidden'}}>
      {/* líneas de velocidad durante el zoom */}
      {speed > 0 && (
        <svg width="1920" height="1080" style={{position: 'absolute', opacity: speed * 0.8}}>
          {Array.from({length: 48}).map((_, i) => {
            const a = (i / 48) * Math.PI * 2 + i * 0.37;
            const r0 = 300 + ((i * 97 + f * 40) % 700);
            const len = 120 + speed * 260;
            return (
              <line
                key={i}
                x1={960 + Math.cos(a) * r0}
                y1={540 + Math.sin(a) * r0}
                x2={960 + Math.cos(a) * (r0 + len)}
                y2={540 + Math.sin(a) * (r0 + len)}
                stroke={i % 5 === 0 ? C.gold : C.mute}
                strokeWidth={3}
                strokeLinecap="round"
              />
            );
          })}
        </svg>
      )}

      {/* desplazamos la O al centro mientras escalamos sobre ella */}
      <AbsoluteFill
        style={{
          transformOrigin: `${RING_X}px ${RING_Y}px`,
          transform: `translate(${(960 - RING_X) * z}px, 0) scale(${scale})`,
        }}
      >
        {LETTERS.map((ch, i) => {
          const p = sp(f, 2 + i * 3, {damping: 15, stiffness: 150});
          const style: React.CSSProperties = {
            position: 'absolute',
            left: LEFTS[i],
            top: RING_Y - 170,
            width: WIDTHS[i],
            height: 340,
            overflow: 'hidden',
          };
          if (i === 1) {
            return (
              <div key={i} style={style}>
                <svg width={WIDTHS[1]} height={340} style={{transform: `translateY(${(1 - p) * 340}px)`}}>
                  <circle cx={WIDTHS[1] / 2} cy={170} r={98} fill="none" stroke={C.gold} strokeWidth={46} />
                </svg>
              </div>
            );
          }
          return (
            <div key={i} style={style}>
              <div style={{transform: `translateY(${(1 - p) * 340}px)`, textAlign: 'center', fontSize: 300, fontWeight: 900, lineHeight: '340px', color: C.white}}>{ch}</div>
            </div>
          );
        })}
      </AbsoluteFill>

      <div style={{position: 'absolute', top: 760, width: '100%', textAlign: 'center', color: C.mute, fontSize: 26, fontWeight: 700, letterSpacing: 10, opacity: ease(f, 14, 26) * (1 - ease(f, ZOOM_IN, ZOOM_IN + 8))}}>
        ZOOM-THROUGH · MATCH CUT · WHIP PAN
      </div>
      <div style={{opacity: 1 - ease(f, ZOOM_IN, ZOOM_IN + 8)}}>
        <SectionLabel n="05" title="Transiciones" />
      </div>
    </AbsoluteFill>
  );
};
````

<!-- file: motion-graphics/recipes/showreel/scenes/S7Resolve.tsx -->
````tsx
import React from 'react';
import {AbsoluteFill, random, useCurrentFrame} from 'remotion';
import {C, FONT, IN, INOUT, OUT, ease, gold, sp} from '../theme';

const N = 220;
const RING = 300;
const RX = 1.55; // anillo elíptico: deja aire al logotipo
const BURST = 62; // los puntos cierran el anillo y estalla el logotipo
const WORD = 'SELENE';

const P = Array.from({length: N}).map((_, i) => {
  const a = random(`a${i}`) * Math.PI * 2;
  const dist = 900 + random(`d${i}`) * 900;
  return {
    sx: 960 + Math.cos(a) * dist,
    sy: 540 + Math.sin(a) * dist * 0.7,
    ta: (i / N) * Math.PI * 2,
    delay: random(`t${i}`) * 26,
    size: 2 + random(`s${i}`) * 4,
    gold: random(`c${i}`) > 0.35,
  };
});

export const S7Resolve: React.FC = () => {
  const f = useCurrentFrame();
  const spin = f * 0.6 + ease(f, BURST - 6, BURST + 30, [0, 120], OUT);
  const ringR = RING + ease(f, BURST - 4, BURST + 20, [0, 40], OUT);
  const close = ease(f, 176, 204, [0, 1], IN); // el anillo colapsa al punto inicial
  const tracking = ease(f, BURST, BURST + 50, [56, 20], OUT);
  const shine = ease(f, BURST + 20, BURST + 70, [-40, 140], INOUT);
  const logo = sp(f, BURST, {damping: 14, stiffness: 120});
  const sub = ease(f, BURST + 26, BURST + 44);
  const tag = ease(f, BURST + 44, BURST + 62);
  const fadeText = 1 - ease(f, 170, 184);

  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: FONT}}>
      <AbsoluteFill style={{background: `radial-gradient(circle at 50% 50%, ${C.deep} 0%, transparent 55%)`, opacity: ease(f, BURST - 10, BURST + 20) * fadeText}} />

      <svg width="1920" height="1080" style={{position: 'absolute'}}>
        {P.map((p, i) => {
          const t = ease(f, p.delay, p.delay + 36, [0, 1], INOUT);
          const a = p.ta + (spin * Math.PI) / 180;
          const r = ringR * (1 - close) + (i % 3) * 6 * (1 - close);
          const tx = 960 + Math.cos(a) * r * RX;
          const ty = 540 + Math.sin(a) * r;
          const x = p.sx + (tx - p.sx) * t;
          const y = p.sy + (ty - p.sy) * t;
          // estela: segmento hacia atrás proporcional a la velocidad
          const tPrev = ease(f - 2, p.delay, p.delay + 36, [0, 1], INOUT);
          const px = p.sx + (tx - p.sx) * tPrev;
          const py = p.sy + (ty - p.sy) * tPrev;
          return (
            <g key={i} opacity={1 - ease(f, 196, 206)}>
              <line x1={px} y1={py} x2={x} y2={y} stroke={p.gold ? C.gold : C.mute} strokeWidth={p.size} strokeLinecap="round" opacity={0.6} />
              <circle cx={x} cy={y} r={p.size * (1 - close * 0.5)} fill={p.gold ? C.goldL : C.white} />
            </g>
          );
        })}
        {/* destello del cierre del anillo */}
        {f >= BURST - 2 && (
          <ellipse cx="960" cy="540" rx={(RING + ease(f, BURST - 2, BURST + 24) * 700) * RX} ry={RING + ease(f, BURST - 2, BURST + 24) * 700} fill="none" stroke={C.goldL} strokeWidth={14 * (1 - ease(f, BURST - 2, BURST + 24))} opacity={1 - ease(f, BURST - 2, BURST + 24)} />
        )}
        {/* punto final: rima con la apertura */}
        <circle cx="960" cy="540" r={9 * ease(f, 198, 204) * (1 - ease(f, 206, 210))} fill={C.goldL} />
      </svg>

      {/* logotipo */}
      <div style={{position: 'absolute', top: 430, width: '100%', textAlign: 'center', opacity: fadeText}}>
        <div
          style={{
            display: 'inline-block',
            fontSize: 130,
            fontWeight: 900,
            letterSpacing: tracking,
            paddingLeft: tracking,
            backgroundImage: `linear-gradient(110deg, transparent ${shine - 12}%, rgba(255,255,255,0.95) ${shine}%, transparent ${shine + 12}%), ${gold}`,
            WebkitBackgroundClip: 'text',
            color: 'transparent',
            opacity: f < BURST ? 0 : 1,
            transform: `scale(${0.6 + 0.4 * logo})`,
            filter: `blur(${(1 - Math.min(1, logo)) * 16}px)`,
          }}
        >
          {WORD}
        </div>
        <div style={{marginTop: 4, color: C.white, fontSize: 26, fontWeight: 600, letterSpacing: 7, opacity: sub, transform: `translateY(${(1 - sub) * 24}px)`}}>
          SERRANO LAWYERS &amp; CONSULTANTS
        </div>
        <div style={{marginTop: 40, color: C.mute, fontSize: 19, fontWeight: 700, letterSpacing: 4, opacity: tag, transform: `translateY(${(1 - tag) * 20}px)`}}>
          MOTION GRAPHICS ESCRITOS EN CÓDIGO · REMOTION + REACT
        </div>
      </div>
    </AbsoluteFill>
  );
};
````

<!-- file: motion-graphics/recipes/showreel/score.py -->
````python
"""Banda sonora original para el showreel de motion graphics (30 s, 120 BPM, La menor).

Cada evento está anclado a un fotograma del montaje (30 fps):
  0.00-3.00  apertura: dron grave, riser corto, impacto en "CUENTA." (f58)
  3.00-22.80 groove: bombo, palmada, hats, bajo y pad  (Am - F - C - G cada 2 s)
             acentos: inversión de color (f165), cortes (f210/330/480/600),
             alerta (f402), sello (f542), riser del zoom (f642-684)
  22.80-23.0 silencio
  23.00-30.0 resolución: pad que crece, impacto + campana en el logotipo (f752), cola
"""
import sys
import wave

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR = 44100
DUR = 30.0
N = int(SR * DUR)
rng = np.random.default_rng(7)
out = np.zeros((2, N))
duck = np.ones(N)


def fr(frame):
    return frame / 30.0


def mf(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def t_(d):
    return np.arange(int(d * SR)) / SR


def flt(x, kind, f, order=2):
    if kind == 'bp':
        sos = butter(order, [f[0] / (SR / 2), f[1] / (SR / 2)], 'bandpass', output='sos')
    else:
        sos = butter(order, f / (SR / 2), kind, output='sos')
    return sosfilt(sos, x)


def put(sig, at, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= N:
        return
    sig = sig[: N - i]
    l = np.cos((pan + 1) * np.pi / 4)
    r = np.sin((pan + 1) * np.pi / 4)
    out[0, i : i + len(sig)] += sig * gain * l
    out[1, i : i + len(sig)] += sig * gain * r


def env(n, a, d):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)
    return e


# ---------- instrumentos ----------
def kick(g=1.0):
    t = t_(0.45)
    f = 45 + 110 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 7) * g + flt(rng.standard_normal(len(t)), 'hp', 3000) * np.exp(-t * 120) * 0.15


def clap():
    t = t_(0.3)
    n = flt(rng.standard_normal(len(t)), 'bp', (900, 3500))
    e = np.zeros(len(t))
    for o in (0, 0.011, 0.022):
        e += np.where(t >= o, np.exp(-(t - o) * 60), 0)
    return n * (e * 0.4 + np.exp(-t * 18) * 0.5)


def hat(open_=False):
    t = t_(0.25 if open_ else 0.06)
    return flt(rng.standard_normal(len(t)), 'hp', 7000) * np.exp(-t * (14 if open_ else 70))


def saw(freq, d, detune=(0.0,)):
    t = t_(d)
    s = np.zeros(len(t))
    for dt in detune:
        ph = (t * freq * (1 + dt)) % 1
        s += 2 * ph - 1
    return s / len(detune)


def bass(m, d):
    s = saw(mf(m), d, (0, 0.004)) + np.sin(2 * np.pi * mf(m - 12) * t_(d)) * 0.8
    s = flt(s, 'lp', 420)
    return s * env(len(s), 0.004, d * 0.6)


def pad(notes, d, bright=1800):
    s = sum(saw(mf(m), d, (-0.006, 0, 0.006)) for m in notes)
    s = flt(s, 'lp', bright)
    a = np.minimum(1, t_(d) / 0.25) * np.minimum(1, (d - t_(d)) / 0.3)
    return s * a / len(notes)


def riser(d, f0=300, f1=6000):
    t = t_(d)
    n = rng.standard_normal(len(t))
    out_ = np.zeros(len(t))
    steps = 24
    for k in range(steps):
        a, b = k * len(t) // steps, (k + 1) * len(t) // steps
        fc = f0 * (f1 / f0) ** (k / steps)
        out_[a:b] = flt(n, 'bp', (fc * 0.7, min(fc * 1.4, 20000)))[a:b]
    return out_ * (t / d) ** 2


def impact(g=1.0):
    t = t_(2.2)
    f = 32 + 60 * np.exp(-t * 6)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.2)
    crack = flt(rng.standard_normal(len(t)), 'lp', 5000) * np.exp(-t * 14)
    return (boom * 1.1 + crack * 0.5) * g


def whoosh(d=0.6):
    t = t_(d)
    n = rng.standard_normal(len(t))
    sh = np.sin(np.pi * t / d) ** 2
    return flt(n, 'bp', (500, 4000)) * sh


def bell(m, d=3.5):
    t = t_(d)
    s = sum(np.sin(2 * np.pi * mf(m) * r * t) * a * np.exp(-t * dk) for r, a, dk in ((1, 1, 1.3), (2.76, 0.4, 2.5), (5.4, 0.2, 4), (2, 0.3, 1.8)))
    return s * np.minimum(1, t / 0.002)


def blip(m):
    t = t_(0.12)
    return np.sin(2 * np.pi * mf(m) * t) * np.exp(-t * 35)


def drone(d):
    t = t_(d)
    s = saw(mf(33), d, (-0.003, 0.003)) + saw(mf(45), d, (0.002,)) * 0.5
    s = flt(s, 'lp', 260)
    return s * np.minimum(1, t / 1.2)


# ---------- apertura ----------
put(drone(3.0) * np.linspace(1, 0.6, int(3.0 * SR)), 0, 0.35)
put(riser(fr(58)), 0, 0.12)
put(impact(), fr(58), 0.7)
put(bell(69, 2.5), fr(58), 0.10)
put(riser(1.0, 400, 8000), 2.0, 0.14)

# ---------- groove ----------
CHORDS = [(57, [57, 60, 64, 69]), (53, [53, 57, 60, 65]), (48, [55, 60, 64, 67]), (55, [55, 59, 62, 67])]
G0, G1 = 3.0, 22.8
beat = 0.5
b = G0
i = 0
while b < G1 - 1e-6:
    put(kick(), b, 0.75)
    duck_idx = int(b * SR)
    dl = int(0.22 * SR)
    duck[duck_idx : duck_idx + dl] = np.minimum(duck[duck_idx : duck_idx + dl], 0.45 + 0.55 * np.linspace(0, 1, len(duck[duck_idx : duck_idx + dl])))
    if i % 2 == 1:
        put(clap(), b, 0.32)
    put(hat(i % 4 == 3), b + 0.25, 0.10, 0.3)
    put(hat(), b, 0.05, -0.3)
    i += 1
    b += beat

bus = np.zeros((2, N))
t0 = G0
k = 0
while t0 < G1 - 1e-6:
    root, notes = CHORDS[k % 4]
    d = min(2.0, G1 - t0)
    p = pad(notes, d)
    ii = int(t0 * SR)
    bus[0, ii : ii + len(p)] += p * 0.16
    bus[1, ii : ii + len(p)] += np.roll(p, 220) * 0.16
    for e in range(int(d / 0.25)):
        if e % 4 != 3:
            put(bass(root - 12 + (12 if e % 4 == 2 else 0), 0.24), t0 + e * 0.25, 0.30)
    t0 += 2.0
    k += 1
out += bus * duck

# acentos sincronizados con la imagen
put(impact(0.6), fr(165), 0.45)            # inversión de color
for c in (210, 330, 480, 600):
    put(whoosh(0.5), fr(c) - 0.3, 0.16, -0.4 if c % 2 else 0.4)
put(impact(0.5), fr(210), 0.25)
for j, m in enumerate((84, 88, 91)):
    put(blip(m), fr(402) + j * 0.09, 0.12)  # alerta en la matriz
put(impact(0.8), fr(542), 0.50)            # sello VERIFICADO
put(riser(fr(684) - fr(642), 300, 12000), fr(642), 0.22)
put(whoosh(1.2), fr(672), 0.22)

# ---------- resolución ----------
put(pad([45, 57, 64, 69], 7.0, 1200), 23.0, 0.10)
put(riser(fr(752) - 23.0, 200, 5000), 23.0, 0.12)
put(impact(1.0), fr(752), 0.75)
for j, m in enumerate((72, 76, 79, 83, 86)):
    put(bell(m, 4.5), fr(752) + j * 0.06, 0.07, (j - 2) * 0.25)
put(pad([48, 55, 60, 64, 67, 74], 30.0 - fr(752), 2200), fr(752), 0.13)
put(bell(60, 3.0), fr(898) - 2.6, 0.05)

# ---------- reverb y master ----------
ir_t = t_(2.4)
ir = rng.standard_normal((2, len(ir_t))) * np.exp(-ir_t * 2.6)
wet = np.stack([fftconvolve(out[c], ir[c])[:N] for c in range(2)]) * 0.012
mix = out + wet
fade = np.ones(N)
fl = int(1.2 * SR)
fade[-fl:] = np.linspace(1, 0, fl) ** 2
mix *= fade
mix = np.tanh(mix * 1.3) / np.tanh(1.3)
mix *= 0.89 / np.max(np.abs(mix))

pcm = (mix.T * 32767).astype(np.int16)
path = sys.argv[1] if len(sys.argv) > 1 else 'public/score.wav'
with wave.open(path, 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print('ok', path)
````

