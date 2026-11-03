# YokiPet

**Enlace a la app:** [https://yokipet.streamlit.app](https://yokipet.streamlit.app)  
**Autor/a:** Ericka Reyes

## Pitch

Encontrar cuidadores de mascotas confiables y disponibles suele depender de recomendaciones informales en redes sociales que no garantizan compatibilidad con tus mascotas ni con tu horario. **YokiPet** resuelve esto mediante un catálogo interactivo con filtros deterministas (servicio, zona, especie, tamaño y presupuesto) combinado con un asistente analítico basado en IA. El modelo de IA interpreta la descripción de la mascota en lenguaje natural para explicar de forma sencilla por qué un cuidador específico del catálogo se ajusta a sus requerimientos. En el desarrollo de esta versión, aprendimos que es esencial encapsular la IA para que sea no autoritativa y nunca invente datos (precios o disponibilidad) fuera del catálogo estricto. Nuestro siguiente paso sería migrar a un entorno multi-inquilino real con pasarelas de pago integradas como pago a cuentas bancarias, por tarjeta de crédito/débito o  incluso por otras plataformas como PayPal.

## El problema

Los propietarios de mascotas que deben viajar o trabajar se enfrentan a la frustrante tarea de buscar cuidadores sin conocer de antemano su disponibilidad real, precios o experiencia con especies y tamaños específicos. Actualmente, resuelven esto recurriendo a chats informales de vecinos o familiares, un proceso lento y sin garantías de seguridad ni idoneidad para la mascota. Vale la pena resolver este problema para profesionalizar el cuidado de mascotas, abrir nuevas oportunidades de generación de ingresos para las personas que buscan un ingreso estable o extra, centralizar la información verificada de perfiles y brindar tranquilidad a las familias multiespecie.

## Qué hace la app

El usuario realiza los siguientes pasos en la aplicación:
1. **Editar Perfiles:** El usuario visualiza o edita la información de su mascota (perro, gato, tamaño, comportamiento) y sus datos de dueño ficticio (posteriormente se implementaría para usuarios reales).
2. **Búsqueda Personalizada:** Completa el formulario seleccionando el tipo de servicio (hospedaje, guardería, paseos), zona geográfica, fechas, especie de mascota y presupuesto máximo.
3. **Filtro Determinista:** La aplicación aplica reglas estrictas sobre el catálogo de cuidadores cargado en el archivo JSON local.
4. **Lectura de Recomendación Inteligente:** Si la API Key de Gemini está configurada, visualiza una explicación cálida y justificada en lenguaje natural sobre por qué los cuidadores resultantes son óptimos.
5. **Simulación de Reserva:** Solicita el servicio de manera ficticia; el cuidador puede visualizar la solicitud entrante y cambiar su estado en tiempo real dentro del prototipo.

## La pieza de IA

- **Qué usa:** La API de Gemini mediante el SDK `google-genai` ejecutando el modelo `gemini-2.5-flash`.
- **Por qué esa opción:** Ofrece una excelente latencia, soporte completo para español-castellano, y un procesamiento preciso de instrucciones tipo *Zero-Shot* para no salirse de las restricciones del catálogo.
- **Qué pasa si falla:** La app funciona bajo un estricto **modo sin IA**. Si la clave de API (`GEMINI_API_KEY`) no está configurada, o si la llamada a la API falla (por ejemplo, por rebasar la cuota gratuita), el bloque `try/except` atrapa el error y la app muestra las tarjetas de los cuidadores filtrados deterministicamente acompañados de un mensaje amigable: *"La IA explicativa no está disponible temporalmente debido a límites de cuota o conexión. Sin embargo, tus resultados deterministas que ves abajo son 100% confiables."*

## Cómo la he construido

- **Herramientas:** Diseñado utilizando Google Colab como entorno inicial de pruebas para la interacción con la API de Gemini, programado en Python, maquetado con Streamlit y depurado mediante el soporte conversacional de IA.
- **Fichero de contexto del agente:** [AGENTS.md](./AGENTS.md)
- **Prompts clave:**
  - *Prompt de generación explicativa:* `"Actúa como un asistente experto de YokiPet. Analiza los siguientes cuidadores filtrados deterministicamente: {YokiSitters - cuidadores}. Explica de forma concisa por qué coinciden perfectamente con las necesidades de la mascota {mascota_info} sin inventar datos de precios, disponibilidad o ubicaciones que no estén en la lista de origen."`
- **Qué delegué al agente y qué revisé a mano:** Delegué al agente el diseño de la estructura CSS para las tarjetas visuales de los cuidadores y el código boilerplate de inicialización del cliente de Gemini. Revisé manualmente y depuré la lógica estricta de filtros deterministas y la validación para asegurar que la API Key se lea exclusivamente de `st.secrets` sin que se exponga jamás en el historial de Git.

## Prueba y mejora

| Quién la probó | Qué probó | Qué pasó | Qué cambié |
La he probado yo especialmente. Probé las funcionalidades desde la perspectiva de dueña (YokiParent) y de cuidadora (YokiSitter). Los perfiles no estaban funcionando apropiadamente, las solicitudes se enviaban pero no existía visibilidad de status, el perfil de cuidador no tenía opciones para modificar sus datos. He cambiado estos errores que he encontrado para verficar que sí se guarde la información y sea accesible para cada uno de los perfiles.

