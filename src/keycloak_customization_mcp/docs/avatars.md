---
title: Using Avatars
source: https://www.keycloak.org/ui-customization/avatars
summary: Avatares en Admin y Account Console mediante el claim OIDC picture.
---

# Using Avatars

Keycloak soporta avatares en la Admin Console y la Account Console usando el claim estándar de OpenID
Connect `picture`.

El claim `picture` debe tener como valor una **URI** que apunte al avatar que se mostrará en el masthead de
la Admin Console o la Account Console.

## Configuración

1. Entrar a la Admin Console.
2. *Realm Settings → User profile*.
3. Agregar un atributo `picture` a la configuración del user profile.

Una vez guardada una URI en el atributo `picture`, el avatar aparece en la Account Console.

## Seguridad

Permitir que los usuarios especifiquen su propia URI puede generar problemas de seguridad: **un avatar puede
contener malware**.

Mitigación:
- Restringir las fuentes a orígenes confiables.
- Agregar un **validador de expresión regular** al atributo `picture` para controlar las URIs aceptadas.
