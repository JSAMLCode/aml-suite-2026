/**
 * Diagnóstico de IA para la Gerencia de Sucursal · Google Forms + Sheets + Gmail
 * Serrano Lawyers & Consultants · Procompliance · SELENE
 *
 * INSTRUCCIONES (una sola vez, 3 minutos):
 * 1. Entre a https://script.google.com con su cuenta de Google y cree un "Nuevo proyecto".
 * 2. Borre el contenido, pegue TODO este archivo y guarde (ícono de disquete).
 * 3. En el selector de funciones elija "crearDiagnostico" y pulse "Ejecutar".
 *    Autorice los permisos que Google solicita (Formularios, Hojas de cálculo y Gmail).
 * 4. Abra "Ver > Registros de ejecución": verá el ENLACE PARA COMPARTIR, el enlace de edición
 *    y el enlace de la hoja de respuestas. Comparta el primero por WhatsApp o correo.
 *
 * Resultado:
 * - El participante responde sin cuenta de Claude (si no inicia sesión en Google, igual puede responder).
 * - Cada respuesta llega a la hoja "Diagnóstico IA · Respuestas" (descargable como Excel: Archivo > Descargar > .xlsx).
 * - Al enviar, el participante recibe por correo su nivel, dominio por área y plan de refuerzo.
 * - Usted recibe una copia de cada resultado.
 */

const DATA = {
 "LEVELS": {
  "1": "Básico",
  "2": "Intermedio",
  "3": "Avanzado",
  "4": "Experto"
 },
 "AREAS": {
  "G": {
   "n": "Datos, reserva y riesgo",
   "m": "Módulo 00"
  },
  "F": {
   "n": "Fundamentos de IA",
   "m": "Módulo 01"
  },
  "P": {
   "n": "Prompts",
   "m": "Módulo 02"
  },
  "O": {
   "n": "Outlook",
   "m": "Módulo 03"
  },
  "W": {
   "n": "Word",
   "m": "Módulo 04"
  },
  "X": {
   "n": "Excel",
   "m": "Módulo 05"
  },
  "T": {
   "n": "PowerPoint y Teams",
   "m": "Módulo 06"
  },
  "C": {
   "n": "Copilot Chat, Pages y Notebooks",
   "m": "Módulo 07"
  },
  "A": {
   "n": "Agentes",
   "m": "Módulo 08"
  },
  "U": {
   "n": "Automatización",
   "m": "Módulo 09"
  }
 },
 "USAGE": [
  "Copilot en Outlook (resumir, redactar, coaching)",
  "Copilot en Word",
  "Copilot en Excel",
  "Copilot en Teams (reuniones y chats)",
  "Copilot Chat en modo Trabajo",
  "Pages o Notebooks",
  "Prompts guardados o programados",
  "Agentes (creados por mí o por otros)"
 ],
 "USAGE_SCALE": [
  "Nunca",
  "Ocasional",
  "Semanal",
  "Diario"
 ],
 "Q": [
  {
   "id": 1,
   "a": "F",
   "l": 1,
   "s": "¿Qué es una “alucinación” en un asistente de IA como Copilot?",
   "o": [
    "Una respuesta lenta por exceso de usuarios",
    "Una respuesta incorrecta o inventada que se presenta con total seguridad",
    "Un error técnico que cierra la aplicación",
    "Un aviso de seguridad cuando se comparte un archivo",
    "No lo sé"
   ],
   "c": "Una respuesta incorrecta o inventada que se presenta con total seguridad",
   "e": "El modelo genera texto verosímil, no necesariamente verdadero. Por eso cifras, tasas y requisitos se validan con fuentes oficiales."
  },
  {
   "id": 2,
   "a": "F",
   "l": 1,
   "s": "Copilot le indica una tasa para préstamo de auto al preparar una propuesta. ¿Qué hace?",
   "o": [
    "La usa, porque Copilot está conectado al banco",
    "La verifica en la ficha oficial vigente del producto antes de usarla",
    "La redondea para que luzca más atractiva",
    "Le pide a Copilot que confirme si está seguro",
    "No lo sé"
   ],
   "c": "La verifica en la ficha oficial vigente del producto antes de usarla",
   "e": "Condiciones, tasas y requisitos se toman de las fichas oficiales. Preguntarle a Copilot “¿estás seguro?” no es una verificación."
  },
  {
   "id": 3,
   "a": "F",
   "l": 2,
   "s": "Tras una conversación muy larga, Copilot empieza a ignorar instrucciones que le dio al inicio. ¿Qué es lo más efectivo?",
   "o": [
    "Pedir un resumen de lo trabajado e iniciar un chat nuevo con ese resumen y las instrucciones",
    "Seguir en el mismo chat hasta que se corrija",
    "Escribir las instrucciones en mayúsculas",
    "Cambiar de navegador",
    "No lo sé"
   ],
   "c": "Pedir un resumen de lo trabajado e iniciar un chat nuevo con ese resumen y las instrucciones",
   "e": "La ventana de contexto es limitada. Un chat por tema y reiniciar con un resumen mantiene la calidad."
  },
  {
   "id": 4,
   "a": "G",
   "l": 1,
   "s": "¿Dónde puede trabajar información de clientes (nombres, saldos, préstamos) con IA?",
   "o": [
    "En cualquier IA si luego borra la conversación",
    "Solo en el Copilot corporativo autorizado por el banco y según su política interna",
    "En su cuenta personal de Copilot, si es Premium",
    "En ninguna herramienta, nunca",
    "No lo sé"
   ],
   "c": "Solo en el Copilot corporativo autorizado por el banco y según su política interna",
   "e": "La reserva bancaria y la Ley 81 de 2019 aplican igual con IA. Solo el entorno corporativo autorizado ofrece los controles requeridos."
  },
  {
   "id": 5,
   "a": "G",
   "l": 2,
   "s": "Copilot le muestra en una respuesta un archivo de otra área que usted no debería ver. ¿Cuál es la causa más probable?",
   "o": [
    "El archivo tenía permisos que ya le daban acceso a usted; Copilot solo lo hizo visible. Debe reportarlo a TI o al dueño del archivo",
    "Copilot tiene acceso a todos los archivos del banco",
    "Fue una alucinación",
    "Otro usuario le compartió su chat",
    "No lo sé"
   ],
   "c": "El archivo tenía permisos que ya le daban acceso a usted; Copilot solo lo hizo visible. Debe reportarlo a TI o al dueño del archivo",
   "e": "Copilot respeta los permisos existentes: si encuentra algo indebido, el problema es de permisos y debe corregirse."
  },
  {
   "id": 6,
   "a": "G",
   "l": 3,
   "s": "Un ejecutivo le pide usar Copilot para escribirle a un cliente que “su transferencia está retenida porque Cumplimiento sospecha de ella”. ¿Qué corresponde?",
   "o": [
    "No enviar ese mensaje: se usa una comunicación neutral sin mencionar alertas ni revisiones, y se coordina con Cumplimiento",
    "Enviarlo, porque el cliente tiene derecho a saberlo",
    "Redactarlo con tono amable para no molestar al cliente",
    "Pedirle a Copilot que lo suavice y enviarlo",
    "No lo sé"
   ],
   "c": "No enviar ese mensaje: se usa una comunicación neutral sin mencionar alertas ni revisiones, y se coordina con Cumplimiento",
   "e": "Revelar al cliente la existencia de un análisis o reporte es una falta grave (tipping-off). Toda comunicación sensible se coordina con Cumplimiento."
  },
  {
   "id": 7,
   "a": "G",
   "l": 2,
   "s": "Quiere preguntar “¿qué me pidió la gerencia regional por correo esta semana?”. ¿En qué modo de Copilot Chat?",
   "o": [
    "Modo Trabajo",
    "Cualquiera, dan lo mismo",
    "Modo Web",
    "Ninguno: Copilot no puede leer correos",
    "No lo sé"
   ],
   "c": "Modo Trabajo",
   "e": "El modo Trabajo usa sus correos, reuniones, chats y archivos; el modo Web usa información pública."
  },
  {
   "id": 8,
   "a": "P",
   "l": 1,
   "s": "¿Cuáles son los cuatro elementos básicos de un buen prompt?",
   "o": [
    "Título, palabras clave, idioma y extensión",
    "Saludo, pregunta, agradecimiento y firma",
    "Rol, contexto, tarea y formato",
    "Archivo, fecha, destinatario y prioridad",
    "No lo sé"
   ],
   "c": "Rol, contexto, tarea y formato",
   "e": "Rol + Contexto + Tarea + Formato. El método del curso añade límites, audiencia/tono y verificación."
  },
  {
   "id": 9,
   "a": "P",
   "l": 2,
   "s": "¿Cuál de estos prompts dará el resultado más útil?",
   "o": [
    "Analiza las metas.",
    "Dime cómo vamos este mes.",
    "Actúa como gerente comercial. Con /Avance_metas.xlsx calcula el % de cumplimiento por ejecutivo y producto y la colocación diaria necesaria para cerrar. Tabla de menor a mayor. No inventes cifras.",
    "Hazme un análisis completo y profesional de todo.",
    "No lo sé"
   ],
   "c": "Actúa como gerente comercial. Con /Avance_metas.xlsx calcula el % de cumplimiento por ejecutivo y producto y la colocación diaria necesaria para cerrar. Tabla de menor a mayor. No inventes cifras.",
   "e": "Incluye rol, fuente concreta, tarea medible, formato y un límite."
  },
  {
   "id": 10,
   "a": "P",
   "l": 2,
   "s": "Copilot le entregó un buen correo, pero demasiado largo. ¿Qué hace?",
   "o": [
    "Lo recorta usted manualmente siempre",
    "Le pide en el mismo chat: “Mantén el contenido, redúcelo a 100 palabras y deja la pregunta final”",
    "Empieza de nuevo con otro prompt desde cero",
    "Cambia a modo Web",
    "No lo sé"
   ],
   "c": "Le pide en el mismo chat: “Mantén el contenido, redúcelo a 100 palabras y deja la pregunta final”",
   "e": "Iterar sobre la respuesta es más rápido y conserva lo que ya está bien."
  },
  {
   "id": 11,
   "a": "P",
   "l": 3,
   "s": "Tiene lista una propuesta comercial para una empresa. ¿Qué técnica la mejora antes de enviarla?",
   "o": [
    "Pedirle a Copilot que la critique desde la perspectiva del cliente y liste sus posibles objeciones",
    "Traducirla al inglés y de vuelta",
    "Pedirle que agregue más adjetivos",
    "Pedirle que la haga más larga",
    "No lo sé"
   ],
   "c": "Pedirle a Copilot que la critique desde la perspectiva del cliente y liste sus posibles objeciones",
   "e": "La autocrítica con rol (“revísala como el cliente / la regional”) revela debilidades antes de enviar."
  },
  {
   "id": 12,
   "a": "O",
   "l": 1,
   "s": "Recibe un hilo de 25 correos sobre un cliente empresarial. ¿Qué es lo más rápido?",
   "o": [
    "Usar el botón “Resumir” de Copilot en el hilo",
    "Leer todos los correos",
    "Reenviarlo a un ejecutivo",
    "Imprimirlo",
    "No lo sé"
   ],
   "c": "Usar el botón “Resumir” de Copilot en el hilo",
   "e": "Resumir con Copilot en Outlook da los puntos clave y las acciones pendientes en segundos."
  },
  {
   "id": 13,
   "a": "O",
   "l": 2,
   "s": "Va a responder un reclamo delicado y quiere revisar el tono antes de enviar. ¿Qué función usa?",
   "o": [
    "Coaching de Copilot sobre el borrador",
    "Corrector ortográfico",
    "Respuesta automática",
    "Traducir",
    "No lo sé"
   ],
   "c": "Coaching de Copilot sobre el borrador",
   "e": "Coaching evalúa tono, claridad y sentimiento del lector y sugiere mejoras."
  },
  {
   "id": 14,
   "a": "O",
   "l": 2,
   "s": "Quiere saber qué compromisos asumió por correo con clientes y aún no ha cumplido. ¿Cómo?",
   "o": [
    "Preguntar a Copilot (modo Trabajo u Outlook): “¿Qué compromisos asumí por correo esta semana que siguen pendientes?”",
    "Revisar solo la carpeta de enviados",
    "Buscar manualmente por palabra “compromiso”",
    "No es posible con Copilot",
    "No lo sé"
   ],
   "c": "Preguntar a Copilot (modo Trabajo u Outlook): “¿Qué compromisos asumí por correo esta semana que siguen pendientes?”",
   "e": "Copilot puede razonar sobre su correo y devolver una lista con origen y fecha."
  },
  {
   "id": 15,
   "a": "W",
   "l": 1,
   "s": "Para que Copilot en Word redacte una propuesta usando la ficha del producto y sus notas de visita, ¿qué hace?",
   "o": [
    "Copia y pega todo el texto en el documento primero",
    "Envía los archivos por correo a Copilot",
    "En el cuadro de Copilot escribe “/” y selecciona los archivos como referencia",
    "Copilot los encuentra solo, sin indicarlos",
    "No lo sé"
   ],
   "c": "En el cuadro de Copilot escribe “/” y selecciona los archivos como referencia",
   "e": "Referenciar archivos con “/” ancla la redacción a fuentes concretas."
  },
  {
   "id": 16,
   "a": "W",
   "l": 2,
   "s": "Le pide a Copilot revisar y mejorar un procedimiento existente. ¿Cómo ve exactamente qué cambió?",
   "o": [
    "Comparando de memoria",
    "Activando el control de cambios antes de pedir las modificaciones",
    "No es posible saberlo",
    "Pidiéndole que lo marque en negrita",
    "No lo sé"
   ],
   "c": "Activando el control de cambios antes de pedir las modificaciones",
   "e": "Con control de cambios usted aprueba o rechaza cada modificación."
  },
  {
   "id": 17,
   "a": "X",
   "l": 1,
   "s": "¿Qué requisito ayuda más a que Copilot funcione bien en Excel?",
   "o": [
    "Tener el archivo en el escritorio del computador",
    "Datos en formato Tabla con encabezados claros, sin celdas combinadas, y archivo en OneDrive o SharePoint",
    "Usar muchos colores",
    "Que el archivo tenga una sola columna",
    "No lo sé"
   ],
   "c": "Datos en formato Tabla con encabezados claros, sin celdas combinadas, y archivo en OneDrive o SharePoint",
   "e": "Copilot necesita datos estructurados y el archivo en la nube del banco."
  },
  {
   "id": 18,
   "a": "X",
   "l": 2,
   "s": "Le pide a Copilot una columna con la colocación diaria necesaria para cumplir la meta. ¿Qué hace después?",
   "o": [
    "La usa en el reporte a la regional de inmediato",
    "La borra porque Copilot no hace fórmulas",
    "Pide que explique la fórmula y valida 2 o 3 cálculos manualmente",
    "Copia los valores sin la fórmula",
    "No lo sé"
   ],
   "c": "Pide que explique la fórmula y valida 2 o 3 cálculos manualmente",
   "e": "Las fórmulas generadas se validan antes de usarlas en un reporte oficial."
  },
  {
   "id": 19,
   "a": "X",
   "l": 3,
   "s": "Tiene 500 comentarios de encuestas de servicio en una columna y quiere clasificarlos por tema. ¿Qué es más eficiente?",
   "o": [
    "Borrar los comentarios vacíos y adivinar",
    "Leerlos uno por uno",
    "Usar la función =COPILOT() en una columna nueva con las categorías definidas",
    "Pedirlo en PowerPoint",
    "No lo sé"
   ],
   "c": "Usar la función =COPILOT() en una columna nueva con las categorías definidas",
   "e": "La función COPILOT en celda aplica la misma instrucción fila por fila (por ejemplo: precio, tiempo, servicio, producto, otro)."
  },
  {
   "id": 20,
   "a": "X",
   "l": 3,
   "s": "Quiere analizar 12 meses de colocaciones: estacionalidad, mejores canales y proyección. ¿Qué herramienta es la más adecuada?",
   "o": [
    "El agente Analyst o Agent Mode en Excel, pidiendo que explique su metodología",
    "El botón Resumir de Outlook",
    "Copilot en Word",
    "Un prompt programado",
    "No lo sé"
   ],
   "c": "El agente Analyst o Agent Mode en Excel, pidiendo que explique su metodología",
   "e": "Analyst y Agent Mode planifican y ejecutan análisis de varios pasos, incluso con Python."
  },
  {
   "id": 21,
   "a": "T",
   "l": 1,
   "s": "¿Qué necesita para que Copilot en Teams genere el acta del huddle con los compromisos de cada ejecutivo?",
   "o": [
    "Que la reunión tenga la transcripción (o grabación) activada",
    "Invitar a Copilot como participante por correo",
    "Tomar notas a mano",
    "Nada; Copilot escucha todas las llamadas",
    "No lo sé"
   ],
   "c": "Que la reunión tenga la transcripción (o grabación) activada",
   "e": "Copilot en reuniones trabaja sobre la transcripción; sin ella, no tiene qué resumir después."
  },
  {
   "id": 22,
   "a": "T",
   "l": 2,
   "s": "Entra 15 minutos tarde a una reunión de Teams. ¿Qué hace para ponerse al día sin interrumpir?",
   "o": [
    "Pide a todos que repitan",
    "Espera al acta del día siguiente",
    "Pregunta a Copilot en la reunión: “¿Qué se ha discutido y qué se ha decidido hasta ahora?”",
    "Sale y vuelve a entrar",
    "No lo sé"
   ],
   "c": "Pregunta a Copilot en la reunión: “¿Qué se ha discutido y qué se ha decidido hasta ahora?”",
   "e": "Copilot responde durante la reunión con base en la transcripción en curso."
  },
  {
   "id": 23,
   "a": "T",
   "l": 2,
   "s": "Quiere la presentación mensual para la regional a partir del informe que ya redactó en Word. ¿Cómo?",
   "o": [
    "Copiar y pegar párrafo por párrafo en diapositivas",
    "En PowerPoint, pedir a Copilot crear la presentación desde el archivo referenciado, indicando número y temas de diapositivas",
    "Exportar el Word como PDF",
    "Pedirlo en Outlook",
    "No lo sé"
   ],
   "c": "En PowerPoint, pedir a Copilot crear la presentación desde el archivo referenciado, indicando número y temas de diapositivas",
   "e": "Copilot en PowerPoint crea la presentación a partir de un documento y puede agregar notas del orador."
  },
  {
   "id": 24,
   "a": "C",
   "l": 2,
   "s": "¿Qué es una Copilot Page?",
   "o": [
    "Un correo programado",
    "Un lienzo persistente y editable, creado desde una respuesta de Copilot, que se puede compartir y trabajar en equipo",
    "Una página web pública del banco",
    "Un archivo de Excel",
    "No lo sé"
   ],
   "c": "Un lienzo persistente y editable, creado desde una respuesta de Copilot, que se puede compartir y trabajar en equipo",
   "e": "Las Pages convierten una respuesta en un documento vivo para colaborar (por ejemplo, el plan de campaña con el equipo)."
  },
  {
   "id": 25,
   "a": "C",
   "l": 3,
   "s": "¿Para qué sirve un Copilot Notebook (cuaderno)?",
   "o": [
    "Para guardar contraseñas",
    "Para agrupar archivos, páginas y notas de un tema y hacerle preguntas a Copilot sobre ese conjunto",
    "Para tomar notas a mano alzada",
    "Para enviar correos masivos",
    "No lo sé"
   ],
   "c": "Para agrupar archivos, páginas y notas de un tema y hacerle preguntas a Copilot sobre ese conjunto",
   "e": "Un notebook “Metas 2026” con fichas, plan e informes permite consultas enfocadas en esas fuentes."
  },
  {
   "id": 26,
   "a": "C",
   "l": 2,
   "s": "Quiere recibir cada mañana a las 7:30 un resumen de reuniones, correos pendientes y menciones. ¿Qué usa?",
   "o": [
    "Una alarma del teléfono",
    "Una regla de Outlook",
    "Un prompt programado en Copilot Chat",
    "Un agente de SharePoint",
    "No lo sé"
   ],
   "c": "Un prompt programado en Copilot Chat",
   "e": "Los prompts programados ejecutan la misma instrucción con la frecuencia elegida."
  },
  {
   "id": 27,
   "a": "C",
   "l": 3,
   "s": "¿Cuándo es apropiado usar el agente Researcher?",
   "o": [
    "Para una investigación profunda de varias fuentes con informe y citas, como analizar la zona de influencia de la sucursal",
    "Para enviar un correo rápido",
    "Para corregir ortografía",
    "Para aprobar créditos",
    "No lo sé"
   ],
   "c": "Para una investigación profunda de varias fuentes con informe y citas, como analizar la zona de influencia de la sucursal",
   "e": "Researcher planifica búsquedas en web y datos de trabajo y entrega un informe citado. Más lento, más profundo."
  },
  {
   "id": 28,
   "a": "C",
   "l": 1,
   "s": "¿Para qué sirve la Prompt Gallery (galería de prompts)?",
   "o": [
    "Para guardar, reutilizar y compartir prompts con el equipo",
    "Para almacenar archivos de clientes",
    "Para ver imágenes generadas",
    "Para cambiar el idioma de Copilot",
    "No lo sé"
   ],
   "c": "Para guardar, reutilizar y compartir prompts con el equipo",
   "e": "Permite tener una biblioteca de prompts estándar de la sucursal."
  },
  {
   "id": 29,
   "a": "C",
   "l": 2,
   "s": "¿Qué logran las instrucciones personalizadas de Copilot?",
   "o": [
    "Que Copilot aplique sus preferencias (rol, tono, formato) en todas las conversaciones sin repetirlas",
    "Que las respuestas sean más rápidas",
    "Que Copilot tenga acceso a más archivos",
    "Que Copilot no cometa errores",
    "No lo sé"
   ],
   "c": "Que Copilot aplique sus preferencias (rol, tono, formato) en todas las conversaciones sin repetirlas",
   "e": "Se configuran una vez en Personalización y mejoran todas las respuestas."
  },
  {
   "id": 30,
   "a": "A",
   "l": 3,
   "s": "¿Qué distingue a un agente de un chat normal con Copilot?",
   "o": [
    "Que es más caro",
    "Que tiene instrucciones, conocimiento y capacidades propias para un rol específico, y puede compartirse",
    "Que solo funciona en inglés",
    "Que no necesita revisión humana",
    "No lo sé"
   ],
   "c": "Que tiene instrucciones, conocimiento y capacidades propias para un rol específico, y puede compartirse",
   "e": "Un agente es un Copilot especializado (por ejemplo, Coach Comercial) que todo el equipo puede usar igual."
  },
  {
   "id": 31,
   "a": "A",
   "l": 3,
   "s": "Crea el agente “Coach Comercial”. ¿Dónde coloca las fichas oficiales de productos?",
   "o": [
    "En las instrucciones, copiando todo el texto",
    "Como fuente de conocimiento (por ejemplo, la carpeta de SharePoint con las fichas vigentes)",
    "En un correo al agente",
    "No hace falta; el agente ya las conoce",
    "No lo sé"
   ],
   "c": "Como fuente de conocimiento (por ejemplo, la carpeta de SharePoint con las fichas vigentes)",
   "e": "El conocimiento conectado se mantiene actualizado sin reescribir las instrucciones."
  },
  {
   "id": 32,
   "a": "A",
   "l": 4,
   "s": "Quiere un agente que, además de conversar, registre oportunidades en una lista de SharePoint y pida aprobación a la gerente en casos especiales. ¿Con qué se construye?",
   "o": [
    "Con Copilot Studio, usando temas, herramientas y flujos (Power Automate) con aprobaciones",
    "Con un prompt programado",
    "Con Agent Builder básico, solo con instrucciones",
    "Con Copilot en Word",
    "No lo sé"
   ],
   "c": "Con Copilot Studio, usando temas, herramientas y flujos (Power Automate) con aprobaciones",
   "e": "Las acciones sobre sistemas, la lógica y las aprobaciones requieren Copilot Studio y flujos."
  },
  {
   "id": 33,
   "a": "A",
   "l": 3,
   "s": "Antes de compartir un agente con el equipo, ¿qué es lo correcto?",
   "o": [
    "Probar una sola pregunta",
    "Compartirlo con todo el banco para que más gente lo use",
    "Probarlo con un banco de preguntas, incluidas preguntas fuera de alcance y pedidos indebidos, y compartirlo solo con el equipo de la sucursal",
    "No requiere pruebas",
    "No lo sé"
   ],
   "c": "Probarlo con un banco de preguntas, incluidas preguntas fuera de alcance y pedidos indebidos, y compartirlo solo con el equipo de la sucursal",
   "e": "Las pruebas verifican que respete límites (no prometer tasas, no aceptar datos reales, no saltarse políticas)."
  },
  {
   "id": 34,
   "a": "U",
   "l": 4,
   "s": "Cada mañana, cada ejecutivo debe recibir en Teams sus oportunidades con próximo paso vencido. ¿Cómo se automatiza?",
   "o": [
    "Con un flujo programado de Power Automate que lee la lista de SharePoint, filtra por fecha y envía un mensaje a cada ejecutivo",
    "Recordándoselo en el huddle",
    "Con la función =COPILOT() en Excel",
    "Con el botón Resumir de Outlook",
    "No lo sé"
   ],
   "c": "Con un flujo programado de Power Automate que lee la lista de SharePoint, filtra por fecha y envía un mensaje a cada ejecutivo",
   "e": "Datos estructurados + disparador programado + filtro + notificación: patrón clásico de Power Automate."
  },
  {
   "id": 35,
   "a": "U",
   "l": 4,
   "s": "¿Cuál de estas tareas NO debe quedar totalmente automatizada sin revisión humana?",
   "o": [
    "Recordar a un ejecutivo un seguimiento vencido",
    "Enviar a clientes comunicaciones con condiciones de crédito redactadas por IA",
    "Enviar a la gerente un resumen semanal de oportunidades",
    "Clasificar encuestas de servicio por tema",
    "No lo sé"
   ],
   "c": "Enviar a clientes comunicaciones con condiciones de crédito redactadas por IA",
   "e": "Comunicaciones a clientes con condiciones y decisiones de crédito siempre pasan por revisión y aprobación."
  },
  {
   "id": 36,
   "a": "U",
   "l": 4,
   "s": "¿Cuál es el orden recomendado para automatizar una rutina de la gerencia?",
   "o": [
    "Flujo de Power Automate → prompt programado → prompt guardado",
    "Agente autónomo desde el primer día",
    "Prompt guardado → prompt programado → flujo de Power Automate",
    "Directamente un flujo sin probar el prompt",
    "No lo sé"
   ],
   "c": "Prompt guardado → prompt programado → flujo de Power Automate",
   "e": "Escalera de automatización: se sube de escalón solo cuando el anterior funciona bien."
  }
 ]
};
const MARCA = 'Serrano Lawyers &amp; Consultants · Procompliance · SELENE';
const NAVY = '#0B1F3A', GOLD = '#C9A227';

function crearDiagnostico() {
  const form = FormApp.create('Diagnóstico de IA · Gerencia de Sucursal con Microsoft 365 Copilot');
  form.setDescription('Evaluación del nivel de dominio de Microsoft 365 Copilot en el rol de Gerente de Sucursal bancaria. ' +
    'Responda según lo que sabe y hace hoy, sin consultar a Copilot. "No lo sé" no penaliza. Duración: 25 minutos. ' +
    'Al enviar recibirá su resultado por correo.\n\nMaterial de formación independiente de Serrano Lawyers & Consultants; no es material oficial de ninguna entidad bancaria.');
  form.setIsQuiz(true);
  try { form.setEmailCollectionType(FormApp.EmailCollectionType.RESPONDER_INPUT); }
  catch (e) { form.setCollectEmail(true); }
  form.setProgressBar(true);
  form.setShuffleQuestions(false);
  form.setConfirmationMessage('¡Gracias! En unos minutos recibirá su resultado en el correo indicado.');

  // Inicio
  form.addSectionHeaderItem().setTitle('Datos de la evaluación');
  form.addTextItem().setTitle('Nombre').setRequired(true);
  form.addTextItem().setTitle('Rol').setHelpText('Ejemplo: Gerente de Sucursal');
  form.addMultipleChoiceItem().setTitle('Licencia de Copilot que usa en el trabajo')
    .setChoiceValues(['Microsoft 365 Copilot corporativo (asignado por el banco)', 'Copilot Chat con cuenta del banco (sin licencia completa)', 'Microsoft 365 Premium personal', 'No estoy segura']);

  // Parte 1
  form.addPageBreakItem().setTitle('Parte 1 · Uso actual').setHelpText('¿Con qué frecuencia usa hoy cada capacidad? No suma puntaje.');
  form.addGridItem().setTitle('Frecuencia de uso').setRows(DATA.USAGE).setColumns(DATA.USAGE_SCALE);

  // Parte 2 por área
  form.addPageBreakItem().setTitle('Parte 2 · Conocimiento aplicado').setHelpText('36 preguntas de situación. Elija una opción por pregunta.');
  const order = Object.keys(DATA.AREAS);
  let n = 0;
  order.forEach(area => {
    const qs = DATA.Q.filter(q => q.a === area);
    if (!qs.length) return;
    form.addSectionHeaderItem().setTitle(DATA.AREAS[area].n);
    qs.forEach(q => {
      n++;
      const it = form.addMultipleChoiceItem();
      it.setTitle(n + '. ' + q.s).setHelpText('Nivel: ' + DATA.LEVELS[q.l]).setRequired(true).setPoints(q.l);
      it.setChoices(q.o.map(t => it.createChoice(t, t === q.c)));
      const fb = FormApp.createFeedback().setText(q.e).build();
      it.setFeedbackForCorrect(fb).setFeedbackForIncorrect(fb);
    });
  });

  // Parte 3
  form.addPageBreakItem().setTitle('Parte 3 · Ejercicio práctico');
  form.addParagraphTextItem().setTitle('Reescriba este prompt para que Copilot entregue un resultado utilizable de inmediato: "Ayúdame con las metas del mes."');

  // Hoja de respuestas
  const ss = SpreadsheetApp.create('Diagnóstico IA · Respuestas');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());
  const res = ss.insertSheet('Resultados');
  res.appendRow(['Fecha', 'Nombre', 'Correo', 'Licencia', 'Nivel', '% global', 'Básico', 'Intermedio', 'Avanzado', 'Experto']
    .concat(order.map(k => DATA.AREAS[k].n + ' %')).concat(['Elementos del prompt (de 6)', 'Prompt práctico']));
  res.getRange(1, 1, 1, res.getLastColumn()).setFontWeight('bold').setBackground(NAVY).setFontColor('#FFFFFF');
  res.setFrozenRows(1);

  PropertiesService.getScriptProperties().setProperty('SHEET_ID', ss.getId());
  ScriptApp.getProjectTriggers().forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('alEnviar').forForm(form).onFormSubmit().create();

  Logger.log('ENLACE PARA COMPARTIR: ' + form.getPublishedUrl());
  Logger.log('Editar formulario: ' + form.getEditUrl());
  Logger.log('Hoja de respuestas (Excel): ' + ss.getUrl());
}

function alEnviar(e) {
  const r = e.response;
  const items = r.getItemResponses();
  const get = t => { const x = items.find(i => i.getItem().getTitle() === t); return x ? x.getResponse() : ''; };
  const nombre = get('Nombre') || 'Participante';
  const licencia = get('Licencia de Copilot que usa en el trabajo');
  const correo = r.getRespondentEmail();
  const practico = items.filter(i => i.getItem().getTitle().indexOf('Reescriba este prompt') === 0).map(i => i.getResponse())[0] || '';

  // Puntaje
  const byTitle = {};
  items.forEach(i => byTitle[i.getItem().getTitle()] = i.getResponse());
  const tier = {1: [0, 0], 2: [0, 0], 3: [0, 0], 4: [0, 0]}, area = {};
  let pts = 0, max = 0, n = 0;
  Object.keys(DATA.AREAS).forEach(a => DATA.Q.filter(q => q.a === a).forEach(q => {
    n++;
    const ok = byTitle[n + '. ' + q.s] === q.c;
    tier[q.l][1]++; if (ok) tier[q.l][0]++;
    area[q.a] = area[q.a] || [0, 0]; area[q.a][1]++; if (ok) area[q.a][0]++;
    max += q.l; if (ok) pts += q.l;
  }));
  const tp = l => tier[l][1] ? tier[l][0] / tier[l][1] * 100 : 0;
  let level = 0; for (let l = 1; l <= 4; l++) { if (tp(l) >= 70) level = l; else break; }
  const pct = Math.round(pts / max * 100);
  const NIV = {0: 'Inicial', 1: 'Básico', 2: 'Intermedio', 3: 'Avanzado', 4: 'Experto'};
  const TXT = {
    0: 'Aún no consolida las bases. Prioridad: reglas de datos, conceptos y método de prompts antes de usar Copilot con información del banco.',
    1: 'Usa Copilot para resumir y redactar y conoce las reglas de datos. Siguiente paso: dominar el método de prompts y el uso diario en Outlook, Word y Excel.',
    2: 'Escribe prompts estructurados y usa Copilot en las aplicaciones. Siguiente paso: Notebooks, Pages, Researcher, Analyst y su primer agente.',
    3: 'Organiza su trabajo con las herramientas premium y entiende los agentes. Siguiente paso: automatizaciones con Power Automate y agentes con acciones.',
    4: 'Domina el ecosistema hasta la automatización. Puede liderar la adopción de IA en la sucursal y formar a su equipo.'
  };

  // Ejercicio práctico
  const s = String(practico).toLowerCase();
  const checks = [
    ['Rol', /act[uú]a como|eres un|eres una|como gerente|como analista/.test(s)],
    ['Contexto o archivo', /\/|archivo|excel|xlsx|sucursal|ejecutivos|meta de|usd|\d{2,}/.test(s)],
    ['Tarea concreta', /calcula|identifica|compara|resume|analiza|proyecta|lista|redacta|clasifica/.test(s)],
    ['Formato', /tabla|vi[ñn]etas|lista|gr[aá]fico|correo|palabras|columnas|diapositiva/.test(s)],
    ['Límites', /no inventes|solo|únicamente|unicamente|no uses|sin |m[aá]ximo/.test(s)],
    ['Verificación', /supuestos|confirmar|verificar|valida|explica la f[oó]rmula|metodolog/.test(s)]
  ];
  const nPrac = checks.filter(c => c[1]).length;

  // Hoja
  const ss = SpreadsheetApp.openById(PropertiesService.getScriptProperties().getProperty('SHEET_ID'));
  const keys = Object.keys(DATA.AREAS);
  ss.getSheetByName('Resultados').appendRow([new Date(), nombre, correo, licencia, NIV[level], pct]
    .concat([1, 2, 3, 4].map(l => tier[l][0] + '/' + tier[l][1]))
    .concat(keys.map(k => Math.round(area[k][0] / area[k][1] * 100)))
    .concat([nPrac, practico]));

  // Correo
  const filas = keys.map(k => {
    const p = Math.round(area[k][0] / area[k][1] * 100);
    const col = p >= 70 ? '#1F7A4D' : p >= 40 ? '#B7791F' : '#B42318';
    return '<tr><td style="padding:6px 10px;border-bottom:1px solid #DCE1EA">' + DATA.AREAS[k].n + '</td>' +
      '<td style="padding:6px 10px;border-bottom:1px solid #DCE1EA;text-align:center">' + area[k][0] + '/' + area[k][1] + '</td>' +
      '<td style="padding:6px 10px;border-bottom:1px solid #DCE1EA;text-align:right;color:' + col + ';font-weight:700">' + p + '%</td></tr>';
  }).join('');
  const debiles = keys.filter(k => area[k][0] / area[k][1] < 0.7)
    .map(k => '<li>' + DATA.AREAS[k].n + ' · ' + DATA.AREAS[k].m + '</li>').join('');
  const html =
    '<div style="font-family:Nunito Sans,Segoe UI,Arial,sans-serif;max-width:620px;margin:auto;color:#1F2733">' +
    '<div style="background:' + NAVY + ';color:#fff;padding:24px;border-radius:12px 12px 0 0">' +
    '<div style="color:' + GOLD + ';font-size:11px;letter-spacing:2px;font-weight:800">' + MARCA.toUpperCase() + '</div>' +
    '<h2 style="margin:8px 0 0">Diagnóstico de IA · Gerencia de Sucursal</h2></div>' +
    '<div style="border:1px solid #DCE1EA;border-top:0;padding:24px;border-radius:0 0 12px 12px">' +
    '<p>Hola ' + nombre + ',</p><p>Este es el resultado de su diagnóstico de Microsoft 365 Copilot:</p>' +
    '<div style="background:#F4EBCF;border-left:5px solid ' + GOLD + ';padding:14px 16px;border-radius:8px">' +
    '<div style="font-size:12px;letter-spacing:1px;color:' + NAVY + ';font-weight:800">NIVEL DIAGNOSTICADO</div>' +
    '<div style="font-size:26px;font-weight:900;color:' + NAVY + '">' + NIV[level] + ' · ' + pct + '%</div>' +
    '<div>' + TXT[level] + '</div></div>' +
    '<h3 style="color:' + NAVY + '">Dominio por área</h3><table style="width:100%;border-collapse:collapse;font-size:14px">' +
    '<tr style="background:' + NAVY + ';color:#fff"><th style="padding:6px 10px;text-align:left">Área</th><th>Aciertos</th><th style="text-align:right;padding:6px 10px">%</th></tr>' + filas + '</table>' +
    (debiles ? '<h3 style="color:' + NAVY + '">Áreas a reforzar</h3><ul>' + debiles + '</ul>' : '<p>Todas las áreas superan el 70%.</p>') +
    '<h3 style="color:' + NAVY + '">Ejercicio práctico</h3><p>Elementos detectados: ' + nPrac + ' de 6 (' +
    checks.map(c => (c[1] ? '✓ ' : '✗ ') + c[0]).join(' · ') + ').</p>' +
    '<p>Su facilitador, José Serrano, revisará el resultado con usted en la próxima sesión.</p>' +
    '<p style="color:#5B6576;font-size:12px;margin-top:24px">' + MARCA + '</p></div></div>';

  const asunto = 'Su resultado · Diagnóstico de IA para la Gerencia de Sucursal';
  if (correo) MailApp.sendEmail({to: correo, subject: asunto, htmlBody: html, name: 'Serrano Lawyers & Consultants'});
  const owner = Session.getEffectiveUser().getEmail();
  if (owner) MailApp.sendEmail({to: owner, subject: '[Copia] ' + nombre + ' · ' + NIV[level] + ' ' + pct + '%', htmlBody: html});
}
