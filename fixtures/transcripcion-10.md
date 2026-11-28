Reunión — FitZone Gimnasios (evolutivo de app existente)
Fecha: 27/11/2026 · Duración: 40 min
Asistentes: Marcos Ibáñez (CEO), Natalia Ríos (responsable de marketing), David (tech lead, nosotros)

David: Nos decíais que ya tenéis una app.

Marcos: Sí, la hizo otra empresa hace tres años. Está en React Native con un backend en Node y una base de datos MongoDB. La empresa cerró y nos quedamos sin nadie que la mantenga.

David: ¿Tenéis acceso al código?

Marcos: Tenemos el repositorio en GitHub y acceso a la cuenta de AWS. Documentación, casi ninguna. Y los tests, me dijeron que había pocos.

David: ¿Qué hace la app ahora?

Natalia: Los socios reservan clases dirigidas, ven su QR para entrar al gimnasio y consultan sus pagos. Tenemos 6 gimnasios y unos 9.000 socios activos con la app instalada.

David: ¿Qué problemas tenéis?

Marcos: Varios. Apple nos ha avisado de que tenemos que actualizar a la nueva versión del SDK o nos retiran la app de la tienda en febrero. Las notificaciones push dejaron de funcionar en Android hace dos meses. Y en hora punta, sobre las siete de la tarde, las reservas van muy lentas o fallan.

Natalia: Y luego queremos cosas nuevas: una sección de entrenamientos con vídeos, que el entrenador asigne una rutina a cada socio, y un sistema de "trae a un amigo" con descuento.

David: ¿Qué es lo más urgente?

Marcos: Lo de Apple, sin duda. Luego las push y la lentitud. Lo nuevo puede esperar a después del verano.

David: Lo primero que haríamos sería una auditoría del código para ver en qué estado está. Puede que algunas partes convenga rehacerlas.

Marcos: Lo entiendo. Pero no quiero que me digáis que hay que tirarlo todo y empezar de cero.

David: Os daremos la estimación por fases: auditoría, correcciones urgentes, estabilización y funcionalidades nuevas.
