
# AGENTS.md — YokiPet

> Instrucciones para agentes de programación (Codex, Cursor, Copilot, Gemini CLI y otros). Leer `especificacion.md` **antes** de modificar el código. En caso de conflicto, pedir aclaración en lugar de inventar requisitos.

## Qué es este proyecto

YokiPet es un **prototipo académico** que ayuda a dueños de mascotas a encontrar cuidadores ficticios compatibles por servicio, zona, fechas y presupuesto, y a simular solicitudes de reserva. **No** es un servicio de reservas reales ni debe presentarse como tal.

## Cómo está hecho

- **Lenguaje:** Python 3.12.
- **Interfaz:** Streamlit (ruta A, desplegable en Streamlit Community Cloud).
- **IA opcional:** API de Gemini mediante SDK `google-genai`; identificador de modelo está en la constante `MODELO` de `app.py`.
- **Archivos:** `app.py`, `requirements.txt`, `README.md`, `especificacion.md`, `AGENTS.md`, `data/cuidadores.json`, `data/mascotas.json`, `tests/`, `.gitignore`, `.streamlit/secrets.toml.example`.
- **Especificación completa:** `./especificacion.md`.
- **Objetivo de costes:** usar solo herramientas gratuitas cuando sea posible; nunca asumir que una API o despliegue tendrá cuota gratuita ilimitada.

## Reglas

1. **Seguridad de secretos:** leer `GEMINI_API_KEY` desde `st.secrets` o variable de entorno; nunca ponerla en código, pruebas, README, prompts o logs. Mantener `.streamlit/secrets.toml` fuera de Git.
2. **Modo sin IA:** la app debe arrancar y permitir buscar y simular reservas sin ninguna clave configurada.
3. **Llamadas a Gemini:** usar `try/except`, timeouts cuando los admita el SDK, manejo de cuota y mensajes comprensibles. No mostrar stack traces al usuario.
4. **IA no autoritativa:** nunca dejar que Gemini invente perfiles, precios, fechas, disponibilidad, verificaciones o estados de reserva. Validar y limitar cualquier salida estructurada.
5. **Filtrado determinista:** servicio, especie, tamaño, disponibilidad, capacidad y presupuesto son restricciones obligatorias. El ranking solo usa datos presentes en el catálogo.
6. **Privacidad:** utilizar únicamente datos ficticios. No solicitar ni almacenar identificaciones, domicilios exactos, teléfonos, datos bancarios o información médica real.
7. **Mensajes de interfaz:** español claro, tono cálido y profesional; etiquetas accesibles y diseño usable en móvil.
8. **Aviso visible:** mostrar en la interfaz «Prototipo con datos ficticios. No se realizan reservas reales».
9. **Cambios pequeños:** implementar una tarea por vez. Antes de cambios grandes, describir el plan; al terminar, explicar archivos modificados, razones y cómo probar.
10. **Dependencias:** si se agrega una librería, actualizar `requirements.txt`; evitar dependencias innecesarias y documentar su uso.
11. **Pruebas:** ejecutar las pruebas disponibles tras cada cambio relevante. No afirmar que pasaron si no se ejecutaron; reportar fallos y limitaciones.
12. **Código mantenible:** funciones pequeñas, nombres descriptivos, separación entre datos/reglas de negocio/interfaz cuando sea viable, anotaciones de tipos en lógica crítica y manejo explícito de errores.
13. **No ampliar alcance:** no introducir pagos, cuentas reales, chat, geolocalización precisa, servicios veterinarios ni arquitectura de producción sin aprobación.
14. **No modificar arquitectura/modelo por cuenta propia:** pedir autorización antes de cambiar Streamlit, Gemini, la estructura general o el alcance del prototipo.
15. **No desplegar ni hacer push:** requiere revisión y aprobación explícita de la propietaria.
16. **No borrar ni reescribir el README:** salvo autorización; actualizar secciones puntuales cuando sea necesario.

## Contratos de comportamiento

- El sistema debe funcionar de forma determinista sin Gemini.
- Si el usuario escribe texto ambiguo, mostrar campos propuestos y exigir confirmación antes de buscar.
- No enviar a Gemini datos personales reales ni información que no sea necesaria para explicar resultados.
- Los resultados de búsqueda deben excluir cuidadores que incumplan cualquier filtro obligatorio.
- Los precios deben calcularse en USD y mostrar unidad de tarifa y total estimado.
- Una solicitud solo puede pasar de `pendiente` a `aceptada` o `rechazada` dentro de la sesión.
- No usar `st.session_state` como si fuera una base de datos segura o persistente.
- En ausencia de resultados, mostrar estado vacío útil, no una lista fabricada por IA.

## Cómo comprobar que funciona

Ruta A: `streamlit run app.py` en local (con `.streamlit/secrets.toml`), o haz push y revisa la app en Streamlit Cloud.

### Casos de prueba mínimos

| Caso | Resultado esperado |
|---|---|
| Perro mediano, visita a domicilio, San José, fecha válida y presupuesto suficiente | Se muestran solo cuidadores ficticios compatibles y disponibles. |
| Perro grande con cuidador que solo acepta perros pequeños | El cuidador queda excluido. |
| Presupuesto insuficiente o sin disponibilidad | Se muestra estado vacío claro; no se inventan resultados. |
| Fecha de fin anterior al inicio o campos vacíos | Validación comprensible; no se envía solicitud. |
| Gemini sin configurar o cuota agotada | Búsqueda y reservas simuladas siguen funcionando. |
| Texto libre ambiguo | Se pide confirmar campos antes de ejecutar búsqueda. |
| Solicitud pendiente aceptada/rechazada | Estado actualizado en la sesión, sin pago ni reserva real. |
| Pregunta ajena al servicio | El asistente redirige al propósito de SayiPet. |

## Qué no hacer

- No borrar ni reescribir el README sin preguntar.
- No cambiar modelo, arquitectura o alcance sin preguntar.
- No hacer `git push`, despliegues ni publicar secretos sin autorización.
- No conectar pagos, cuentas reales ni APIs externas adicionales sin autorización.
- No presentar perfiles, disponibilidad, precios o reservas simuladas como información real.
- No usar IA para tomar decisiones de seguridad o certificar cuidadores.

## Formato de respuesta del agente al finalizar cada tarea

- **Implementado:** breve descripción.
- **Archivos modificados:** rutas y propósito.
- **Pruebas realizadas:** comandos y resultados reales.
- **Limitaciones o pendientes:** riesgos y siguiente paso recomendado.
