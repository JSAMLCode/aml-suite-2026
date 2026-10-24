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
