---
title: Emails de Keycloak: catálogo, variables y plantillas
source: Keycloak 26.0, tema base de email (org.keycloak.keycloak-themes, theme/base/email) verificado en una instancia real
summary: Los 15 emails que dispara Keycloak, cuándo salen, qué claves de mensaje y variables FreeMarker usa cada uno, cómo se activan los de eventos y cómo armar un tema de email.
---

# Emails de Keycloak

Referencia práctica de los emails que envía Keycloak 26 y de cómo personalizarlos. Complementa la sección "Emails" de la guía `themes`. Contenido extraído del tema base (`theme/base/email` dentro de `org.keycloak.keycloak-themes-*.jar`) y probado contra un Keycloak 26.0 con un tema propio. Verificar contra la versión que se use: las claves y los argumentos pueden cambiar entre versiones.

## Catálogo de emails

Cada email es una plantilla `html/<nombre>.ftl` y `text/<nombre>.ftl`, y tres claves de mensaje: `<clave>Subject`, `<clave>Body` (texto plano) y `<clave>BodyHtml`.

| Email | Plantilla (`html/` y `text/`) | Clave de mensaje | Cuándo sale |
|---|---|---|---|
| Verificar email | `email-verification.ftl` | `emailVerification` | Registro con `verifyEmail` activo, o acción requerida VERIFY_EMAIL |
| Verificación con código | `email-verification-with-code.ftl` | `emailVerificationWithCode` | Variante con código en lugar de link |
| Nueva contraseña | `password-reset.ftl` | `passwordReset` | "¿Olvidaste tu contraseña?" (`resetPasswordAllowed`) |
| Acciones requeridas | `executeActions.ftl` | `executeActions` | Un admin o la API llama a `execute-actions-email` |
| Confirmar nuevo email | `email-update-confirmation.ftl` | `emailUpdateConfirmation` | Cambio de email con la feature `UPDATE_EMAIL` |
| Vincular cuenta externa | `identity-provider-link.ftl` | `identityProviderLink` | Login con un IdP cuyo email ya existe |
| Invitación a organización | `org-invite.ftl` | `orgInvite` | Organizaciones de Keycloak |
| Prueba de SMTP | `email-test.ftl` | `emailTest` | Botón de prueba de la consola de admin |
| Intento de login fallido | `event-login_error.ftl` | `eventLoginError` | Evento LOGIN_ERROR |
| Contraseña cambiada | `event-update_password.ftl` | `eventUpdatePassword` | Evento UPDATE_PASSWORD |
| OTP cambiado / eliminado | `event-update_totp.ftl`, `event-remove_totp.ftl` | `eventUpdateTotp`, `eventRemoveTotp` | Eventos UPDATE_TOTP / REMOVE_TOTP |
| Credencial cambiada / eliminada | `event-update_credential.ftl`, `event-remove_credential.ftl` | `eventUpdateCredential`, `eventRemoveCredential` | Eventos UPDATE_CREDENTIAL / REMOVE_CREDENTIAL |
| Bloqueo temporal | `event-user_disabled_by_temporary_lockout.ftl` | `eventUserDisabledByTemporaryLockout` | Fuerza bruta con bloqueo temporal |
| Bloqueo permanente | `event-user_disabled_by_permanent_lockout.ftl` | `eventUserDisabledByPermanentLockout` | Fuerza bruta con `permanentLockout` |

Además existe `template.ftl`, el marco común (macro `emailLayout`).

## Emails de eventos: requieren el listener `email`

Los `event-*` solo salen si el realm tiene el listener de eventos `email` activo (Realm settings → Events → Event listeners, o `eventsListeners` en el JSON del realm). Por defecto solo está `jboss-logging`. Los eventos que mandan email son un subconjunto fijo (los de la tabla); activar el listener no genera mails para otros eventos. El usuario tiene que tener email, y el realm, SMTP configurado.

Los emails de verificación, nueva contraseña y acciones requeridas no dependen de eventos: salen por el flujo correspondiente.

## Variables por plantilla

Argumentos de `msg(...)` en la plantilla `html/<nombre>.ftl` (los de `text/` son los mismos). Los números son los `{0}`, `{1}`… de las claves de mensaje.

| Clave | Argumentos |
|---|---|
| `emailVerification`, `passwordReset` | `{0}` link, `{1}` minutos de vigencia, `{2}` nombre del realm, `{3}` vigencia formateada ("12 horas") |
| `emailVerificationWithCode` (clave `emailVerificationBodyCode`) | `{0}` código |
| `executeActions` | `{0}` link, `{1}` minutos, `{2}` realm, `{3}` acciones requeridas (texto), `{4}` vigencia formateada |
| `emailUpdateConfirmation` | `{0}` link, `{1}` email nuevo, `{2}` realm, `{3}` vigencia formateada |
| `identityProviderLink` | `{0}` nombre visible del IdP, `{1}` realm, `{2}` usuario en el IdP, `{3}` link, `{4}` minutos, `{5}` vigencia formateada |
| `orgInvite` (`orgInviteBodyHtml`) | `{0}` link, `{1}` minutos, `{2}` realm, `{3}` nombre de la organización, `{4}` vigencia formateada. La variante `orgInviteBodyPersonalized…` suma `{5}` nombre y `{6}` apellido. En el asunto, `{0}` es la organización |
| `eventLoginError`, `eventUpdatePassword`, `eventUpdateTotp`, `eventRemoveTotp` | `{0}` fecha del evento, `{1}` IP |
| `eventUserDisabledByTemporaryLockout`, `…PermanentLockout` | `{0}` fecha. Ojo: la clave HTML se llama `eventUserDisabledBy…LockoutHtml` (sin `Body`) |
| `eventUpdateCredential`, `eventRemoveCredential` | `{0}` tipo de credencial (`event.getDetail("credential_type")`, "unknown" si falta), `{1}` fecha, `{2}` IP |
| `emailTest` | `{0}` nombre del realm (la plantilla base lo pasa solo al HTML) |

Variables FreeMarker disponibles en la plantilla (las que usa el tema base): `link`, `linkExpiration`, `linkExpirationFormatter(linkExpiration)`, `realmName`, `requiredActionsText` (se arma con `requiredAction.<ACCION>` en los mensajes), `newEmail`, `code`, `identityProviderDisplayName`, `identityProviderContext.username`, `event.date`, `event.ipAddress`, `event.details`, `locale`, `url.resourcesUrl`.

El `realmName` es el nombre visible del realm (`displayName`); si no está definido, Keycloak usa el id. Un realm sin `displayName` produce textos como "una cuenta de Mi-realm".

## Armar un tema de email

Estructura mínima (tema nativo, también dentro del JAR de un tema Keycloakify en `src/email/`):

```
email/
├── theme.properties            parent=base
├── html/template.ftl           marco común (macro emailLayout)
├── html/<nombre>.ftl           una por email que se quiera rediseñar
├── text/<nombre>.ftl           opcional: versión en texto plano
├── messages/messages_es.properties
└── resources/img/logo.png      opcional
```

- `parent=base` hereda todo lo que no se pise: alcanza con sobreescribir `html/template.ftl` para cambiar el marco de todos los emails y los mensajes para el copy.
- En Keycloakify 11, la carpeta `src/email` con un `theme.properties` se detecta como tema de email nativo y se copia tal cual al JAR (no hace falta `initialize-email-theme`, que es interactivo).
- Elegir el tema: Realm settings → Themes → Email theme, o `emailTheme` en el realm (`kcadm update realms/<realm> -s emailTheme=<nombre>`).
- Dos archivos de mensajes: los textos van en `messages/messages_<locale>.properties`; el locale del email sale del usuario o del `defaultLocale` del realm, y hay que habilitar el idioma en el realm (`internationalizationEnabled`, `supportedLocales`).

## Trampas

- **kcSanitize quita los estilos.** Las plantillas base hacen `${kcSanitize(msg("…BodyHtml", …))?no_esc}`. El sanitizador de Keycloak elimina atributos `style` y elementos fuera de una lista corta, así que un `BodyHtml` con CSS en línea llega sin estilos. Solución: pisar la plantilla `html/<nombre>.ftl`, armar el marcado en la plantilla (con estilos en línea) y usar `msg(...)` solo para textos planos (FreeMarker los escapa solo).
- **Apóstrofes.** Los mensajes pasan por `MessageFormat`: un apóstrofe se escribe doble (`didn''t`), y las llaves con texto literal van entre comillas simples.
- **Escape.** En `.ftl` de emails la salida está en modo HTML con autoescape: `${msg(...)}` escapa; `?no_esc` solo después de `kcSanitize`.
- **Imágenes.** Los clientes de correo necesitan URL absolutas: `${url.resourcesUrl}/img/logo.png` (no `resourcesPath`). Solo funcionan si Keycloak es alcanzable desde internet; muchos clientes las bloquean por defecto, así que el mail tiene que entenderse sin imágenes.
- **Probar sin enviar a nadie.** Con Docker: Keycloak + Mailpit (SMTP de captura, UI en el puerto 8025). Un mail de cada tipo se dispara con la Admin API: `PUT /admin/realms/<realm>/users/<id>/execute-actions-email` (body: lista de acciones; query `client_id` y `redirect_uri`), `PUT .../users/<id>/send-verify-email` y el flujo "olvidé mi contraseña". Con `kcadm.sh update users/<id>/execute-actions-email -r <realm> -b '["VERIFY_EMAIL"]' -q client_id=… -q redirect_uri=…`.
- **Cachés de tema.** En desarrollo, `--spi-theme-cache-themes=false` y `--spi-theme-cache-templates=false`, y reiniciar después de regenerar el JAR.
