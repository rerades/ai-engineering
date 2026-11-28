Reunión — Panaderías Hornomar (cuadros de mando)
Fecha: 17/11/2026 · Duración: 35 min
Asistentes: Jorge Lozano (director general), Inés Calvo (controller financiera), Álex (analista de datos, nosotros)

Álex: ¿Qué información os falta hoy?

Jorge: Tenemos 18 tiendas y un obrador central. Cada tienda tiene su TPV y cada noche se genera un fichero con las ventas. Inés los junta a mano en Excel una vez al mes, y para entonces ya es tarde para reaccionar.

Inés: Tardo unos tres días cada mes. Y a veces hay errores al copiar.

Álex: ¿Qué TPV usáis?

Inés: Todas las tiendas el mismo, GestPan. Exporta CSV a una carpeta de un servidor FTP. Tiene una API, pero creo que hay que pagarla aparte.

Álex: ¿Qué os gustaría ver?

Jorge: Ventas por tienda, por día y por franja horaria. Los productos más vendidos y los que menos. Comparativa con el mismo periodo del año anterior.

Inés: Y la merma: lo que se produce en el obrador y no se vende. Los datos de producción están en otro programa, en una base de datos SQL Server en el obrador.

Álex: ¿Quién vería los cuadros de mando?

Jorge: Yo, Inés y los 18 encargados de tienda. Cada encargado solo debería ver su tienda.

Álex: ¿Tenéis alguna herramienta de BI?

Inés: Tenemos licencias de Microsoft 365, así que Power BI nos parecería bien si no sale caro.

Álex: ¿Histórico?

Inés: Tenemos los CSV de los últimos tres años, aunque el formato cambió en 2024 cuando actualizaron el TPV.

Jorge: Y si se pudiera, una previsión de cuánto producir cada día por tienda para reducir la merma. Eso sería lo ideal, pero entiendo que es otra fase.
