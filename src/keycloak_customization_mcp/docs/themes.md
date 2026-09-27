---
title: Working with themes
source: https://www.keycloak.org/ui-customization/themes
summary: Tipos de theme, estructura, theme.properties, plantillas FreeMarker, emails, despliegue, dark mode y SPIs.
---

# Working with themes

## Tipos de theme

- **account**: Account Console
- **admin**: Admin Console
- **email**: mensajes de email
- **login**: formularios de login
- **welcome**: página de bienvenida

Todos menos `welcome` se eligen en la Admin Console: *Realm Settings → Themes* → elegir theme y guardar.
El theme `welcome` se configura por línea de comandos (ver guía `welcome-theme`).

Los themes por defecto vienen en `keycloak-themes-{project_version}.jar`. Se recomienda **extender** los
existentes (`parent`) en vez de editarlos, para simplificar las actualizaciones.

Un theme se compone de: plantillas HTML (FreeMarker), imágenes, bundles de mensajes, hojas de estilo,
scripts y `theme.properties`.

## Estructura de directorios

```
themes/mytheme/
├── login/
│   ├── theme.properties
│   ├── resources/
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│   ├── messages/
│   │   └── messages_en.properties
│   └── login.ftl
└── email/
    └── messages/
        └── messages_en.properties
```

## Desarrollo: desactivar cachés

```
bin/kc.[sh|bat] start --spi-theme--static-max-age=-1 --spi-theme--cache-themes=false --spi-theme--cache-templates=false
```

Para limpiar la caché a mano, borrar el directorio `data/tmp/kc-gzip-cache`.

## Ejemplo de theme.properties

```properties
parent=base
import=common/keycloak
styles=css/login.css css/styles.css
scripts=js/script.js
locales=en,de,fr
```

## Propiedades de theme.properties

| Propiedad | Uso |
|---|---|
| `parent` | Theme padre que se extiende |
| `import` | Importa recursos de otro theme |
| `abstract` | Booleano: theme solo base, no seleccionable en la Admin Console |
| `common` | Sobrescribe la ruta de recursos comunes (por defecto `common/keycloak`) |
| `styles` | Hojas de estilo separadas por espacio |
| `stylesCommon` | Hojas de estilo comunes separadas por espacio |
| `scripts` | Scripts separados por espacio |
| `favicons` | Favicons separados por espacio, o entradas con notación de punto |
| `locales` | Locales soportados, separados por coma |
| `contentHashPattern` | Regex de nombres de archivo con hash de contenido |

## Configuración avanzada de recursos (notación de punto)

### Stylesheets

```properties
styles.file1=css/file1.css
styles.file1.media=(prefers-color-scheme: light)
styles.file2=css/file2.css
styles.file2.media=(prefers-color-scheme: dark)
```

Atributos soportados: `media`, `integrity`, `crossorigin`.

### Scripts

```properties
scripts.analytics=js/analytics.js
scripts.analytics.integrity=sha384-abc...
scripts.analytics.defer=true
scripts.analytics.type=module
```

Atributos soportados: `integrity`, `defer`, `async`, `type`, `crossorigin`, `blocking`.

### Favicons

```properties
favicons.svg=favicon/favicon.svg
favicons.light=favicon/favicon-light.png
favicons.light.media=(prefers-color-scheme: light)
favicons.dark=favicon/favicon-dark.png
favicons.dark.media=(prefers-color-scheme: dark)
favicons.ico=favicon/favicon.ico
```

Atributos soportados: `media`, `type`, `rel`.

### Orden

```properties
styles.order=dark,light
styles.light=css/light.css
styles.dark=css/dark.css
```

## Ejemplos de recursos

CSS:

```css
.login-pf body {
    background: DimGrey none;
}
```

JavaScript:

```javascript
alert('Hello');
```

## Sustitución de propiedades de sistema y variables de entorno

```properties
javaVersion=${java.version}
unixHome=${env.HOME:Unix home not found}
windowsHome=${env.HOMEPATH:Windows home not found}
```

Formato: `${some.system.property}` o `${env.ENV_VAR:defaultValue}`.

## Footer personalizado (footer.ftl)

```freemarker
<#macro content>
<#-- footer at the end of the login box -->
<div>
    <ul id="kc-login-footer-links">
        <li><a href="#home">Home</a></li>
        <li><a href="#about">About</a></li>
        <li><a href="#contact">Contact</a></li>
    </ul>
</div>
</#macro>
```

## Imágenes

En stylesheets:

```css
body {
    background-image: url('../img/image.jpg');
    background-size: cover;
}
```

En plantillas HTML (no email):

```freemarker
<img src="${url.resourcesPath}/img/image.jpg" alt="My image description">
```

En plantillas de email (los clientes de correo requieren URL **absolutas**: usar `resourcesUrl` /
`resourcesCommonUrl`, no las variantes `Path`):

```freemarker
<img src="${url.resourcesUrl}/img/image.jpg" alt="My image description">
<img src="${url.resourcesCommonUrl}/img/logo.png" alt="My logo">
```

## Íconos de Identity Providers

En `theme.properties`, patrón `kcLogoIdP-<alias> = <clase-de-ícono>`:

```properties
kcLogoIdP-myProvider = fa fa-lock
```

## Plantillas HTML propias

Se crean como `<THEME_TYPE>/<TEMPLATE>.ftl` (FreeMarker). Ejemplo de modificación:

```freemarker
<#import "template.ftl" as layout>
<h1>HELLO WORLD!</h1>
...
```

Recomendación: aprovechar las plantillas integradas mediante CSS y la configuración de User Profile,
en vez de reemplazar plantillas completas.

## Emails

Crear `themes/mytheme/email/messages/messages_en.properties`. Cada email necesita **tres** claves:
`Subject`, `Body` y `BodyHtml`.

```properties
passwordResetSubject=My password recovery
passwordResetBody=Reset password link: {0}
passwordResetBodyHtml=<a href="{0}">Reset password</a>
```

## Despliegue

### Directorio

Copiar el directorio del theme a `themes/`.

### Archivo (JAR)

```
mytheme.jar
├── META-INF/
│   └── keycloak-themes.json
└── theme/
    └── mytheme/
        ├── login/
        │   ├── theme.properties
        │   ├── login.ftl
        │   ├── resources/
        │   │   ├── css/styles.css
        │   │   └── img/image.png
        │   └── messages/messages_en.properties
        └── email/
            └── messages/messages_en.properties
```

`META-INF/keycloak-themes.json`:

```json
{
    "themes": [{
        "name" : "mytheme",
        "types": [ "login", "email" ]
    }]
}
```

Copiar el JAR a `providers/`; reiniciar si el server ya estaba corriendo.

**Seguridad:** los themes contienen plantillas FreeMarker que el servidor renderiza en runtime, por lo que
una plantilla maliciosa puede ejecutar código como el proceso de Keycloak. Instalar themes solo de fuentes
confiables y restringir el acceso de escritura al directorio `themes`.

## Dark mode

Se activa/desactiva en *Admin Console → Realm Settings → Themes → "Dark mode"*. Al activarlo se aplica la
variante oscura según la preferencia del SO o del user agent. Solo funciona con themes que soporten
variantes dark/light.

## SPIs de themes

- **Theme Selector SPI**: implementar `ThemeSelectorProviderFactory` y `ThemeSelectorProvider` para
  sobrescribir la selección de theme (p. ej. distinto theme en mobile vs. desktop).
- **Theme Resources SPI**: JAR con plantillas en `theme-resources/templates`, recursos en
  `theme-resources/resources` y mensajes en `theme-resources/messages`; implementar
  `ThemeResourceProviderFactory` y `ThemeResourceProvider` para control más fino.
- **Locale Selector SPI**: implementar `LocaleSelectorProvider` y `LocaleSelectorProviderFactory`. Un único
  método: `resolveLocale(RealmModel, UserModel)`. Se puede extender `DefaultLocaleSelectorProvider` (p. ej.
  para ignorar el header `Accept-Language`).
