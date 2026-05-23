# Manual de Usuario - Control de Grúa Torre Pro 🏗️

Bienvenido a la interfaz avanzada de control para tu Grúa Torre. Esta aplicación web te permite manejar la grúa de forma manual, personalizar la apariencia visual, automatizar rutinas y controlarla mediante los sensores de movimiento de tu teléfono.

---

## ⚙️ 1. Configuración Visual y Diseño

La interfaz ha sido diseñada para adaptarse a tus preferencias personales. Cualquier cambio que realices aquí se guardará automáticamente en tu dispositivo.

### Cambiar el Tema (Colores)
1. Presiona el botón con el ícono de engranaje **`⚙️`** en la esquina superior derecha.
2. Selecciona un tema en el menú desplegable:
   - **Industrial**: Modo oscuro profesional con acentos verdes (ideal para ahorrar batería).
   - **Cyberpunk Neón**: Estética futurista con contrastes brillantes.
   - **Diurno**: Fondo blanco de alto contraste, ideal si estás controlando la grúa al aire libre bajo el sol.

### Reordenar los Botones
Si eres zurdo o simplemente prefieres tener los controles de "Giro" en la parte superior, puedes mover los paneles de control:
1. Busca las flechas **`▲`** y **`▼`** en la esquina superior derecha de cualquier panel (Carro, Elevación o Giro).
2. Presiona las flechas para subir o bajar el panel seleccionado. ¡El nuevo orden se guardará automáticamente!

---

## 🤖 2. Automatización de Rutinas (Macros)

Puedes enseñarle a la grúa una secuencia de movimientos para que la repita sola, respetando los tiempos exactos.

1. **Iniciar Grabación**: Presiona el botón **`🔴 Grabar`**. El botón se pondrá rojo parpadeante para indicar que está escuchando.
2. **Manejar la Grúa**: Usa los botones normales (Adelante, Subir, Girar). El sistema medirá cuántos milisegundos mantienes presionado cada botón.
3. **Detener Grabación**: Presiona el botón **`⏹️ Parar`**.
4. **Reproducir**: Asegúrate de que la grúa esté en una posición segura y presiona **`▶️ Rutina`**. La grúa ejecutará todos los movimientos en orden.
   - *Tip: Si hay una emergencia mientras la rutina se ejecuta, simplemente presiona el botón rojo grande de **STOP** para cancelar la automatización al instante.*

---

## 📱 3. Modo Inmersivo (Control por Movimiento experimental)

El Modo Inmersivo transforma tu celular en un control de movimiento al estilo de la Nintendo Wii, leyendo el giroscopio de tu teléfono.

### ¿Cómo manejarlo?
1. Sostén el celular horizontalmente frente a ti.
2. Presiona el botón **`📱 Inmersivo`**. Verás que debajo aparece un texto leyendo los datos de tu sensor (`P` y `R`).
3. **Mover el Carro**: Inclina el teléfono hacia adelante para mover el carro hacia adelante, e inclínalo hacia ti para traer el carro hacia atrás.
4. **Girar la Grúa**: Gira el celular hacia la izquierda o derecha (como si fuera un volante de automóvil).
   - *Nota: Hay una "zona muerta" de 20 grados en el centro para que tu pulso no active la grúa por accidente.*
5. Para salir, presiona el botón nuevamente o presiona **STOP**.

---

## ⚠️ SOLUCIÓN DE PROBLEMAS: El Modo Inmersivo no detecta movimiento

> [!WARNING]
> Si al presionar el Modo Inmersivo el texto inferior dice **"Datos Nulos"** o se queda pegado en **"Esperando movimiento..."**, significa que la seguridad de tu navegador web está bloqueando el sensor porque estás en una red local (`http://`) sin certificado de seguridad.

### Cómo solucionarlo en el celular del presentador/evaluador:

Si alguien más quiere probarlo en su propio teléfono, pídele que haga estos pasos (toma menos de 1 minuto):

**Para Google Chrome o Microsoft Edge (Android):**
1. Abre una pestaña nueva y escribe en la barra superior: `chrome://flags` (o `edge://flags`).
2. En la barra de búsqueda que aparece, escribe: `insecure origins treated as secure`.
3. En la caja de texto debajo de esa opción, escribe la dirección exacta de la grúa incluyendo el `http://` (Por ejemplo: `http://192.168.xxx.xxx`).
4. Cambia el botón de *Default/Disabled* a **Enabled**.

5. Presiona el botón azul **Relaunch** (Reiniciar navegador) en la parte inferior.

**Para Opera GX:**
1. Escribe en la barra de direcciones: `opera://flags`.
2. Sigue los mismos pasos (2, 3 y 4) mencionados arriba.

**Para iPhone (Safari):**
Debido a las altísimas restricciones de Apple, este truco a veces no es suficiente. Lo más recomendable es instalar la aplicación de **Google Chrome** en el iPhone y, si aún falla, utilizar un dispositivo Android para hacer la demostración de esta función específica.
