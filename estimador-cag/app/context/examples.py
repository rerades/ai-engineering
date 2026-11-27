"""Estimaciones históricas (ficticias) que se inyectan en el prompt como few-shot examples.

Todas siguen el mismo formato para que el modelo lo imite: desglose de tareas con
horas y coste (tarifa 50 €/h), total, equipo y duración.
"""

ESTIMATION_EXAMPLES = [
    {
        "meeting_summary": (
            "Una distribuidora de material de oficina necesita una plataforma web de gestión "
            "de inventario: alta y baja de productos, control de stock por almacén, alertas de "
            "stock mínimo, usuarios con roles (administrador y operario) y un dashboard con "
            "métricas de rotación. Sin app móvil por ahora."
        ),
        "estimation": """\
## Estimación: Plataforma de Gestión de Inventario

### Desglose de tareas:
1. Diseño UI/UX: 40 horas (2.000 €)
2. Backend API (CRUD inventario y almacenes): 60 horas (3.000 €)
3. Autenticación y roles: 20 horas (1.000 €)
4. Dashboard con métricas: 30 horas (1.500 €)
5. Testing y QA: 25 horas (1.250 €)

**Total estimado: 175 horas (8.750 €)**
**Equipo recomendado: 2 desarrolladores full-stack + 1 diseñador UX (part-time)**
**Duración estimada: 6-8 semanas**
""",
    },
    {
        "meeting_summary": (
            "Una red de clínicas de fisioterapia quiere una app móvil (iOS y Android) para que "
            "los pacientes reserven citas, reciban recordatorios y paguen la sesión por "
            "adelantado. Los fisioterapeutas gestionan su agenda desde la misma app."
        ),
        "estimation": """\
## Estimación: App Móvil de Reservas para Clínicas

### Desglose de tareas:
1. Diseño UI/UX (paciente y profesional): 35 horas (1.750 €)
2. App móvil multiplataforma (React Native): 90 horas (4.500 €)
3. Backend API de reservas y agendas: 50 horas (2.500 €)
4. Notificaciones push y recordatorios: 20 horas (1.000 €)
5. Integración con pasarela de pago: 25 horas (1.250 €)
6. Testing, QA y publicación en stores: 30 horas (1.500 €)

**Total estimado: 250 horas (12.500 €)**
**Equipo recomendado: 1 desarrollador móvil + 1 desarrollador backend + 1 diseñador UX (part-time)**
**Duración estimada: 8-10 semanas**
""",
    },
    {
        "meeting_summary": (
            "Un e-commerce de electrónica necesita sincronizar su tienda online con el ERP: "
            "catálogo y stock del ERP hacia la tienda cada 15 minutos, y pedidos y facturas de "
            "la tienda hacia el ERP en tiempo real. Ahora lo hacen a mano con hojas de cálculo."
        ),
        "estimation": """\
## Estimación: Integración E-commerce ↔ ERP

### Desglose de tareas:
1. Análisis de las APIs del ERP y de la tienda: 15 horas (750 €)
2. Conector de sincronización de catálogo y stock: 45 horas (2.250 €)
3. Sincronización de pedidos y facturas: 40 horas (2.000 €)
4. Gestión de errores, reintentos y logs: 20 horas (1.000 €)
5. Panel de monitorización de sincronizaciones: 15 horas (750 €)
6. Testing de integración: 25 horas (1.250 €)

**Total estimado: 160 horas (8.000 €)**
**Equipo recomendado: 1 desarrollador backend senior + 1 desarrollador backend**
**Duración estimada: 5-6 semanas**
""",
    },
]
