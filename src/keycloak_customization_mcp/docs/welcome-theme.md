---
title: Customizing the Welcome Theme
source: https://www.keycloak.org/ui-customization/welcome-theme
summary: Cómo cambiar el theme de bienvenida (setup del primer admin) con --spi-theme--welcome-theme.
---

# Customizing the Welcome Theme

El welcome theme se muestra al acceder a la página por defecto del servidor (p. ej. `http://localhost:8080`).
Por defecto **solo se usa durante el setup inicial** para crear el primer usuario admin; una vez que existe
un admin, redirige a la Admin Console.

Es independiente de los realms y **no se puede seleccionar desde la Admin Console** como los demás themes.

## Pasos

1. Crear y desplegar un theme `welcome` nuevo siguiendo la guía `themes`.
2. Arrancar el servidor indicando el theme:

```
bin/kc.[sh|bat] start --spi-theme--welcome-theme=custom-theme
```

Reemplazar `custom-theme` por el nombre real del theme. Nótese el doble guion en `--spi-theme--welcome-theme`.
