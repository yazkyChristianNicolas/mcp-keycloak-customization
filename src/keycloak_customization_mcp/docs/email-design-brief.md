---
title: Brief para diseñar los emails de Keycloak (agnóstico de sistema de diseño)
source: Elaborado a partir de la guía `emails` de este MCP y del tema base de email de Keycloak 26.0
summary: Prompt reutilizable para pedirle a una herramienta de diseño (Claude Design, Figma, un agente) los emails de Keycloak con cualquier sistema de diseño; con restricciones de clientes de correo, variables y entregables.
---

# Brief para diseñar los emails de Keycloak

Prompt listo para copiar. No asume ningún sistema de diseño: completar los campos `[ENTRE CORCHETES]` con el de cada marca y adjuntar (o referenciar) su design system. Los 12 diseños cubren los 15 emails del catálogo de la guía `emails` (el de credencial agrupa cambio y baja de contraseña/OTP). Si la marca no usa organizaciones, IdPs externos o verificación con código, quitar esos puntos de la lista.

## Cómo usarlo

1. Completar la sección "Marca" con los datos del design system (o dejar la instrucción de leerlo del archivo adjunto).
2. Quitar de la lista los emails que el realm no dispara (ver `emails`, "Catálogo de emails" y "Emails de eventos").
3. Pedir el entregable como HTML con placeholders `{{variable}}`, que después se mapean a FreeMarker (`${link}`, `${msg(...)}`) en `html/<nombre>.ftl`.
4. Los textos que devuelva la herramienta pasan a `messages_<locale>.properties` (la tabla de textos del entregable está pensada para eso).

## Prompt

````markdown
# Emails transaccionales de [MARCA] (Keycloak)

Diseñá los emails que dispara Keycloak (registro, recuperación de acceso, avisos de seguridad de la cuenta) con el sistema de diseño de [MARCA]: [ADJUNTO / LINK / "el que tenés cargado"]. Voy a convertir tu salida en plantillas FreeMarker de un tema de email de Keycloak, así que el diseño tiene que funcionar en clientes de correo reales.

## Marca (completar)
- Nombre y escritura del wordmark: [ej. "berlinesa", siempre en minúsculas].
- Paleta: fondo del correo [HEX], tarjeta [HEX], encabezado [HEX], texto principal [HEX], texto secundario [HEX], texto terciario [HEX], color de acción (botón y links) [HEX] con texto del botón [HEX], borde [HEX].
- Tipografías: display [FAMILIA], UI [FAMILIA], monoespaciada [FAMILIA]. Fallbacks seguros para correo: [ej. Helvetica, Arial, sans-serif].
- Radios, bordes y sombras: [valores del sistema].
- Logo: [lockup/isotipo, versión para fondo oscuro y claro, formato PNG]. URL absoluta marcada como `{{logo_url}}`.
- Voz: idioma y registro [ej. español rioplatense, "vos"], largo de frases, casing, qué evitar (emoji, humor en avisos de seguridad, signos de exclamación), vocabulario fijo.
- Reglas del sistema que no se pueden romper: [ej. "el degradado de marca solo en login y landing", "el verde es solo para estado X"].

## Quién recibe esto
[Descripción breve del público y del producto.] Llegan desde un link o botón del login, casi siempre desde el celular, en Gmail, Apple Mail u Outlook.

## Restricciones técnicas (no negociables)
- HTML de email: layout con `<table role="presentation">`, CSS 100% inline, ancho máximo 560px, fluido en mobile. Sin flexbox/grid, sin variables CSS, sin JS, sin `position`.
- Fuentes: las tipografías propias no se cargan en la mayoría de los clientes. Declará el stack con fallback y diseñá para que se vea bien con el fallback. Sin Google Fonts ni `@font-face`.
- Imágenes: solo el logo, en PNG con URL absoluta (`{{logo_url}}`), con `alt`, y el mail tiene que entenderse sin imágenes. Sin ilustraciones ni fotos salvo que el sistema las pida.
- Botón "bulletproof": tabla + `<a>` con padding inline. Debajo del botón, siempre el link en texto plano por si el botón no funciona.
- Sin degradados ni imágenes de fondo (los clientes los rompen): fondos planos.
- Modo claro por defecto, con `<meta name="color-scheme" content="light">`. Dark mode solo como extra mínimo que no rompa Gmail.
- Contraste AA para el texto corrido; si el color de acción no llega a 4.5:1 con el texto del botón, usarlo solo en etiquetas de botón cortas y en negrita.
- Cada email lleva versión en texto plano (solo el copy) y un preheader oculto de ~90 caracteres.
- Una sola acción principal por email.

## Contenido
Decí qué pasó y qué tiene que hacer la persona. En los avisos de seguridad, informá con calma qué cambió, cuándo y desde dónde, y qué hacer si no fue ella. No prometas datos que Keycloak no entrega (por ejemplo la hora exacta de un desbloqueo).

## Variables
Usá estos placeholders exactos:
`{{logo_url}}`, `{{link}}` (URL de acción), `{{expiracion}}` (ej. "12 horas"), `{{nombre_app}}`, `{{email_nuevo}}`, `{{acciones}}` (lista de acciones requeridas, texto), `{{fecha}}`, `{{ip}}`, `{{credencial}}` ("contraseña", "OTP"), `{{proveedor}}` (proveedor de identidad externo), `{{organizacion}}`, `{{usuario_externo}}`, `{{codigo}}`.

## Emails a diseñar (por prioridad)
1. **Verificar email**: al crear la cuenta. Variables: `link`, `expiracion`. Aclarar que si no creó la cuenta, ignore el mensaje.
2. **Nueva contraseña**: recuperación de contraseña. Variables: `link`, `expiracion`. Si no lo pidió, la contraseña no cambia.
3. **Contraseña cambiada**: aviso de seguridad, sin botón: fecha e IP y qué hacer si no fue la persona. Variables: `fecha`, `ip`.
4. **Cuenta bloqueada temporalmente**: por intentos fallidos; se desbloquea sola. Variables: `fecha`.
5. **Intento de acceso fallido**: aviso de seguridad. Variables: `fecha`, `ip`.
6. **Credencial agregada, cambiada o eliminada**: un diseño parametrizado por `credencial` y por el verbo. Variables: `credencial`, `fecha`, `ip`.
7. **Acciones requeridas**: un administrador pide actualizar la cuenta. Variables: `link`, `expiracion`, `acciones`.
8. **Confirmar nuevo email**: Variables: `link`, `email_nuevo`, `expiracion`.
9. **Verificación con código**: el código en monoespaciada, grande, con `tabular-nums`. Variables: `codigo`, `expiracion`.
10. **Vincular cuenta externa**: Variables: `link`, `proveedor`, `usuario_externo`, `expiracion`.
11. **Invitación a una organización**: Variables: `link`, `organizacion`, `expiracion`.
12. **Mensaje de prueba de SMTP**: mínimo, para el administrador. Sin variables.

Primero definí el marco compartido (encabezado, tarjeta, botón y pie con una línea de "mensaje automático, no hace falta que lo respondas") y después variá solo el contenido.

## Entregable
- Un HTML por email (`email-verification.html`, `password-reset.html`, `event-update-password.html`, `event-lockout.html`, `event-login-error.html`, `event-credential.html`, `execute-actions.html`, `email-update-confirmation.html`, `email-verification-with-code.html`, `identity-provider-link.html`, `org-invite.html`, `email-test.html`) y su `.txt`.
- Una página de vista previa con todos los emails, en ancho 560px y 360px.
- Una tabla con los textos de cada email (asunto, preheader, título, cuerpo, botón, pie), para pasarlos a `messages_<locale>.properties` sin sacarlos del HTML.
- Sin emoji, sin imágenes distintas del logo y sin colores fuera de la paleta indicada.
````

## Del HTML al tema

Con el entregable en la mano: el marco compartido va a `html/template.ftl` (macro `emailLayout`); el cuerpo de cada email, a `html/<nombre>.ftl` con el marcado y los estilos en la plantilla (no en `BodyHtml`, ver "Trampas" en `emails`), y los textos a `messages_<locale>.properties`. Los placeholders se mapean así: `{{link}}`→`${link}`, `{{expiracion}}`→`${linkExpirationFormatter(linkExpiration)}`, `{{nombre_app}}`→`${realmName}`, `{{email_nuevo}}`→`${newEmail}`, `{{acciones}}`→`${requiredActionsText}`, `{{fecha}}`→`${event.date}`, `{{ip}}`→`${event.ipAddress}`, `{{logo_url}}`→`${url.resourcesUrl}/img/<archivo>`. Después, probar cada uno con Mailpit.
