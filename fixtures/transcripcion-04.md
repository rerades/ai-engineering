Transcripción automática — Hotel Casa Brava (integración PMS)
Fecha: 21/11/2026

[00:00:12] Iker (consultor): Vale, ya estamos grabando. Contadme el problema.
[00:00:20] Nuria Sanz (directora, Casa Brava): Somos un hotel boutique de 28 habitaciones. Usamos un PMS que se llama HotelDesk para la gestión interna, y vendemos en Booking, Expedia y nuestra web.
[00:00:41] Nuria Sanz: El problema es que las tarifas y la disponibilidad las cambiamos a mano en cada canal. El verano pasado tuvimos tres overbookings.
[00:01:05] Iker: ¿HotelDesk tiene API?
[00:01:09] Carlos Pino (IT, Casa Brava): Sí, una API REST, aunque la documentación es regular. Lo he probado con Postman y funciona para leer reservas y habitaciones. Escribir tarifas no sé si se puede.
[00:01:30] Iker: ¿Habéis mirado algún channel manager comercial?
[00:01:35] Nuria Sanz: Sí, pero cobran un porcentaje por reserva y el que tenía conector con HotelDesk era carísimo. Preferimos algo a medida o algo intermedio.
[00:02:02] Iker: ¿Qué tendría que sincronizar exactamente?
[00:02:06] Nuria Sanz: Disponibilidad y tarifas desde HotelDesk hacia los tres canales. Y las reservas que entran por los canales, que se creen solas en HotelDesk.
[00:02:25] Carlos Pino: Con un retraso máximo de un par de minutos. Si no, volvemos a tener overbooking.
[00:02:40] Iker: ¿Y la web propia qué motor usa?
[00:02:44] Carlos Pino: Un motor de reservas que nos hizo una agencia en WordPress. Tiene un plugin con webhooks.
[00:03:10] Nuria Sanz: También quiero un panel sencillo donde vea si alguna sincronización ha fallado y por qué. Y que me llegue un aviso al móvil si algo falla.
[00:03:32] Iker: ¿Tenéis cuentas de desarrollador en Booking y Expedia?
[00:03:36] Carlos Pino: No. ¿Hace falta?
[00:03:40] Iker: Para conectarse directamente, sí, y el proceso de homologación puede tardar semanas. Lo tendremos en cuenta.
[00:04:05] Nuria Sanz: Nos vendría bien tenerlo para abril, antes de Semana Santa.
