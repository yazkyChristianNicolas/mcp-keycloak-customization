---
title: Introduction
source: https://www.keycloak.org/ui-customization/introduction
summary: Visión general de qué UIs de Keycloak se pueden personalizar.
---

# Introduction

Keycloak incluye interfaces de usuario para el **login**, la **Admin Console** y la **Account Console**,
además de la pantalla de **bienvenida** (setup inicial del administrador).

Se pueden personalizar, extender y modificar para casos de uso de producción: cambiar logos y colores
para branding corporativo, o agregar funcionalidad nueva.

## Niveles de esfuerzo

1. **Quick Theme**: logos y colores, sin código (experimental). Ver `quick-theme`.
2. **Theme propio**: CSS, plantillas FreeMarker, mensajes y scripts. Ver `themes`.
3. **Consola propia en React**: paquetes npm `@keycloak/keycloak-admin-ui` y `@keycloak/keycloak-account-ui`.
   Ver `creating-your-own-console` y `themes-react`.
