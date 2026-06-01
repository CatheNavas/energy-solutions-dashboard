# Energy Solutions · Dashboard OTs

Dashboard de seguimiento de Órdenes de Trabajo de Energy Solutions.

## Actualización automática
El dashboard se actualiza automáticamente **cada día de lunes a viernes a las 6am (hora Colombia)** usando GitHub Actions.

## Estructura
```
├── index.html          # Dashboard listo (se regenera automáticamente)
├── template.html       # Plantilla base del dashboard
├── generate.py         # Script que llama a Metabase y regenera index.html
└── .github/
    └── workflows/
        └── update.yml  # Configuración de actualización automática
```

## Configuración inicial
1. Ir a **Settings → Secrets → Actions**
2. Crear secret: `METABASE_API_KEY` con el valor de la API key

## Actualización manual
En la pestaña **Actions → Actualizar Dashboard → Run workflow**
