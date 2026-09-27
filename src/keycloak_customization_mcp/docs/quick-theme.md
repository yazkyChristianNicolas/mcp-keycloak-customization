---
title: Customizing with Quick Theme
source: https://www.keycloak.org/ui-customization/quick-theme
summary: Feature experimental para crear themes con logos y colores sin código.
---

# Customizing with Quick Theme

"Quick Theme" es una feature **experimental** para crear rápidamente un theme con logos y colores para la
Account Console, la Admin Console y las páginas de login. Extiende el theme por defecto de Keycloak en
vez de construir uno desde cero.

## Habilitar

```
bin/kc.[sh|bat] start --features=quick-theme
```

## Personalización

- Vista previa en tiempo real de los cambios de color e imagen.
- Las opciones de color se mapean a las **variables CSS globales de PatternFly**.
- Usa el selector de color nativo del navegador, con gotero (eyedropper) para tomar colores de la pantalla,
  útil para igualar los colores del logo con el fondo.

## Despliegue

1. Clic en **Download theme JAR**.
2. Opción 1: copiar el JAR a `providers/` y reiniciar el servidor.
3. Opción 2: extraer el contenido en `themes/`:

```
jar xf quick-theme.jar
```

**Seguridad:** nunca desplegar un theme de origen dudoso. Las imágenes son un posible vector de ataque, por
lo que no se despliega automáticamente desde la Admin Console.

## Probar

Aplicar el theme en *Realm settings → Themes* y probarlo con los procedimientos de la guía `themes`.
