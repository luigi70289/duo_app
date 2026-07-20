# ⚔️ Duolingo Logros Arena ⚔️

¡La competencia definitiva de idiomas entre amigos! 🚀

Este proyecto transforma los reportes semanales de **Duolingo for Schools** en un videojuego competitivo en tiempo real. Olvídate de los puntos aburridos: aquí los jugadores compiten por desbloquear medallas exclusivas basadas en su rendimiento real.

## 🎖️ Sistema de Logros (Medallas)
La aplicación analiza automáticamente el archivo `.csv` exportado y reparte las siguientes insignias:
* 🥇 **Titán de XP (`oro_xp.png`)**: Otorgada al jugador con más experiencia de la semana.
* ⏱️ **Cerebro de Oro (`hierro_tiempo.png`)**: Para el usuario que dedicó más minutos al estudio.
* 🔥 **Racha Legendaria (`racha_legendaria.png`)**: Para cualquiera que mantenga una racha activa de 7 días o más.
* 🎯 **Francotirador (`francotirador.png`)**: Para los que superan el 90% de precisión en sus lecciones.
* 🧠 **Corrector de Errores (`corrector_errores.png`)**: Para quienes repasan sus fallos en clase.

## 🛠️ Tecnologías utilizadas
* **Backend:** Python + Flask
* **Base de datos:** SQLite (para guardar el historial sin pérdidas)
* **Frontend:** HTML5, CSS3 (Bootstrap) con soporte para WebAPK (PWA)
* **Despliegue:** Preparado para funcionar 24/7 en la nube (Render / PythonAnywhere)

---
*Diseñado para ser escalable: ¡añade tus propias medallas a la carpeta `static/medallas/` y expande el torneo!*
