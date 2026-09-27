---
title: Localization
source: https://www.keycloak.org/ui-customization/localization
summary: Mensajes en themes, agregar idiomas y overrides de traducción por realm.
---

# Localization

**Prerrequisito:** habilitar la internacionalización en *Realm Settings* de la Admin Console.

## Localizar mensajes en un theme

El texto de las plantillas se carga desde bundles de mensajes. Cuando un theme extiende a otro, el hijo
hereda todos los mensajes del bundle del padre.

Crear `themes/mytheme/login/messages/messages_en.properties`:

```properties
usernameOrEmail=Your Username
```

Valores como `{0}` y `{1}` se sustituyen con argumentos en runtime (p. ej. `{0}` en "Log in to {0}" es el
nombre del realm).

Descripciones de theme: claves con formato `theme.<theme-name>.<type>.description`
(p. ej. `theme.keycloak.v3.account.description`).

## Agregar un idioma a un theme

1. Crear `<THEME TYPE>/messages/messages_<LOCALE>.properties` (convenciones de locale de `ResourceBundle`).
2. Ejemplo noruego, `themes/mytheme/login/messages/messages_no.properties`:

```properties
usernameOrEmail=Brukernavn
password=Passord
```

3. En `themes/mytheme/login/theme.properties`:

```properties
locales=en,no
```

4. Replicar para otros tipos de theme:
   - `themes/mytheme/account/messages/messages_no.properties`
   - `themes/mytheme/email/messages/messages_no.properties`
   - copiar `theme.properties` a los directorios `account` y `email`.
5. Traducir el nombre en el selector de idioma, agregando en
   `themes/mytheme/account/messages/messages_en.properties` y
   `themes/mytheme/login/messages/messages_en.properties`:

```properties
locale_no=Norsk
```

## Codificación

Los archivos usan UTF-8 por defecto (con fallback a ISO-8859-1). El escape Unicode sigue el estándar de
`PropertyResourceBundle` de Java.

## Chino

Los códigos antiguos `zh-TW` y `zh-CN` pasan a `zh-Hant` y `zh-Hans`, con una jerarquía de precedencia.

## Overrides por realm (sin crear un theme)

1. Admin Console → seleccionar realm.
2. *Realm Settings → Localization → Realm overrides*.
3. Elegir idioma y clic en **Add translation**.
4. Crear pares clave/valor en el diálogo modal.

La subpestaña **Effective message bundles** permite consultar combinaciones de theme/idioma/tipo para
probar el resultado.
