---
title: Creating your own Console
source: https://www.keycloak.org/ui-customization/creating-your-own-console
summary: Crear una versión propia de la Admin o Account Console con React, pnpm y Maven.
---

# Creating your own Console

Permite crear versiones personalizadas de la Admin Console o la Account Console con los paquetes npm
basados en React que publica Keycloak:

- `@keycloak/keycloak-admin-ui`: theme base de la Admin Console
- `@keycloak/keycloak-account-ui`: theme base de la Account Console

Ambos están en el repositorio npm público.

## Empezar

```bash
pnpm install -g create-keycloak-theme
pnpm create keycloak-theme my-theme -t account    # usar -t admin para la Admin Console
cd my-theme
pnpm install
pnpm run dev
```

Levantar Keycloak:

```bash
pnpm run start-keycloak
```

El server de desarrollo usa Vite con hot-reload. La Account Console queda en
`http://localhost:8080/realms/master/account` con usuario `admin` y password `admin`.

## Agregar una página nueva

Crear el componente importando de la librería de account UI:

```typescript
import {
  AccountEnvironment,
  Page,
  UserRepresentation,
  getPersonalInfo,
  savePersonalInfo,
  useAlerts,
  useEnvironment,
  usePromise,
} from "@keycloak/keycloak-account-ui";
```

Registrar la ruta en `routes.tsx`:

```typescript
import { MyPage } from "./MyPage";

export const MyPageRoute: RouteObject = {
  path: "myPage",
  element: <MyPage />,
};

export const RootRoute: RouteObject = {
  path: decodeURIComponent(new URL(environment.baseUrl).pathname),
  element: <App />,
  errorElement: <>Error</>,
  children: [
    PersonalInfoRoute,
    DeviceActivityRoute,
    LinkedAccountsRoute,
    SigningInRoute,
    ApplicationsRoute,
    GroupsRoute,
    ResourcesRoute,
    MyPageRoute,
  ],
};
```

Las claves de navegación se mapean a propiedades de localización en
`maven-resources/theme/my-account/account/messages/messages_en.properties`.

## Modificar una página existente (ejemplo: DeviceActivity.tsx)

1. Bajar el fuente de GitHub: `js/apps/account-ui/src/account-security/DeviceActivity.tsx`.
2. Editar la plantilla para quitar los elementos no deseados.
3. Actualizar los imports para usar la librería:

```typescript
import {
  AccountEnvironment,
  Page,
  usePromise,
  DeviceRepresentation,
  SessionRepresentation,
  deleteSession,
  getDevices,
  useAlerts,
  useEnvironment,
} from "@keycloak/keycloak-account-ui";
```

4. Instalar los íconos de PatternFly si hacen falta:

```bash
pnpm install @patternfly/react-icons
```

5. Actualizar `routes.tsx` para importar tu versión:

```typescript
import { DeviceActivity } from "./DeviceActivity";
```

## Despliegue

Requiere Maven instalado.

```bash
mvn package
```

Se genera un JAR en `/target`; copiarlo al directorio `/providers` del servidor Keycloak.

## Ubicaciones clave

- Páginas propias: `/src/`
- Rutas: `/routes.tsx`
- Localización: `/maven-resources/theme/my-account/account/messages/messages_en.properties`
- Build: `/target/`
