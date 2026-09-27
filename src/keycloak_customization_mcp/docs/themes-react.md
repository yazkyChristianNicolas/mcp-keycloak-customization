---
title: Using the npm UI packages
source: https://www.keycloak.org/ui-customization/themes-react
summary: Usar los módulos React de Keycloak (admin-ui / account-ui) dentro de tu propia aplicación.
---

# Using the npm UI packages

Los módulos de UI de Keycloak (React) se pueden integrar en una aplicación propia mediante dos paquetes npm:

1. `@keycloak/keycloak-admin-ui`: base del theme de la Admin Console
2. `@keycloak/keycloak-account-ui`: base del theme de la Account Console

## Instalación

```bash
pnpm install @keycloak/keycloak-account-ui
```

## Integración

### 1. Agregar KeycloakProvider

```javascript
import { KeycloakProvider } from "@keycloak/keycloak-ui-shared";

<KeycloakProvider environment={{
      serverBaseUrl: "http://localhost:8080",
      realm: "master",
      clientId: "security-admin-console"
  }}>
  {/* rest of you application */}
</KeycloakProvider>
```

### 2. Configurar traducciones

Configurar `i18next` según la documentación de `react-i18next`, agregar `i18next-http-backend` y configurar:

```javascript
backend: {
  loadPath: `http://localhost:8080/resources/master/account/{lng}}`,
  parse: (data: string) => {
    const messages = JSON.parse(data);

    const result: Record<string, string> = {};
    messages.forEach((v) => (result[v.key] = v.value)); //need to convert to record
    return result;
  },
},
```

(El `{lng}}` con llave doble aparece así en la guía original; probablemente sea un typo y deba ser `{lng}`.)

Para más detalle ver la guía `creating-your-own-console`.
