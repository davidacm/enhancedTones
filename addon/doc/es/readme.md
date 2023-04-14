# Complemento Enhanced tones para NVDA.

Este complemento cambia la forma de gestionar los tonos en NVDA para hacer el proceso más eficiente.

Además, este complemento implementa varios generadores de ondas para que el usuario pueda personalizar el sonido del pitido. Te permite implementar más generadores muy fácilmente.

Si está interesado en crear su propio generador de ondas e integrarlo en este complemento, consulte la sección para desarrolladores.

## Características:

* Mejora el proceso de tonos al reproducir el tono en fragmentos hasta que se completa o se interrumpe con un nuevo tono.
* Implementa varios tipos de generadores de ondas, que suenan muy diferentes entre sí. Diviértete probando los diferentes generadores, ¡tal vez alguno te guste!
* Si un tono es interrumpido por otro de la misma frecuencia, la onda no se interrumpirá, solo prolongará su duración. Evitando así los molestos saltos cuando 2 o más tonos se reproducen  rápidamente. no siempre es posible evitar esta situación, debido a diferentes factores.
* Si un tono es interrumpido por otro de diferente frecuencia, se realizará un barrido de frecuencia para saltar a la nueva frecuencia. Esto también le permite evitar saltos entre tonos, cambiando de una frecuencia a otra suavemente para el oído.

Las últimas dos funciones permiten un sonido más agradable cuando se usan funciones como el seguimiento del mouse con sonido.

## Descarga.
 El último release se puede [Descargar en este enlace.](https://davidacm.github.io/getlatest/gh/davidacm/enhancedTones)

## Idea inicial de este complemento.

Este complemento se creó para resolver algunos problemas con tarjetas de sonido específicas, esos problemas son menos comunes ahora que tenemos mejores controladores de tarjetas de sonido. Pero algunas personas informaron que esos problemas aún están presentes, como alta latencia al reproducir los tonos, o no reproducir los primeros tonos en absoluto. Actualmente, este complemento posee más funcionalidades, por lo que puede ser útil incluso si no tiene problemas con la generación de tonos nativos. Intente esto usted mismo y vea si funciona para usted.

## Descripción de la función original "beep" de NVDA.

Para estar en contexto. Cuando NVDA emite un tono, hace lo siguiente

1. importa generateBeep.
2. detiene el reproductor.
3. genera la forma de onda para el tono.
4. envía el tono generado al reproductor.


Esto puede ser problemático en algunas tarjetas de sonido, como altos retrasos al reproducir los tonos, o no reproducir los primeros tonos en absoluto. Parece que el problema ocurre al detener el reproductor, especialmente cuando esto se repite rápidamente.

Yo tuve este problema en el pasado con uno de mis ordenadores. Así que esa fue la razón para crear este complemento. Mi complemento no detiene el reproductor, y eso arregló el problema.

## Descripción de la función "beep" del complemento.

1. Primero, se crea un hilo de fondo, este hilo se encargará de los pitidos y la comunicación con la salida del reproductor.
2. El hilo se mantiene a la espera de datos para emitir un beep, utilizando un bloqueo de eventos.
3. Cuando se llama a la función beep, la información se envía al hilo y se libera el bloqueo del hilo.
4. El hilo llama a la función que inicia la generación de la onda para el tono, y bloquea la señal de evento de nuevo.
5. Pide al generador la forma de onda en fragmentos y envía cada trozo al reproductor de salida. El generador puede generar la forma de onda en paralelo mientras se envía, o generar toda la forma de onda al principio.
6. Si mientras se envía la onda  al reproductor se libera el bloqueo, significa que se recibió una petición de un nuevo beep, entonces este deja de enviar los datos y salta al paso número 3 para emitir el nuevo beep requerido.
7. Si toda la forma de onda fue enviada al reproductor sin interrupción, salta al paso número 2 para esperar otra señal de beep. Recuerde que el bloqueo se bloqueó en el paso 4 así que el paso 2 quedará en espera nuevamente.

De esta manera, el reproductor de salida nunca es detenido y el proceso es más eficiente.

## Notas sobre este complemento.

Si pruebas este complemento, incluso si no tienes problemas con la forma original de generación de tonos, puedes ver que los tonos son más fluidos, especialmente en los tonos que se repiten rápidamente.

Además, este complemento implementa varios generadores de tonos, el generador sinusoidal está habilitado de forma predeterminada. Pero puedes cambiarlo al generador de tonos de NVDA.
Mis generadores de tonos personalizados están escritos puramente en Python. Por lo tanto, son menos eficientes que el generador de tonos NVDA, pero la diferencia no se nota debido a la mejor forma de gestionar el proceso de reproducción y a que la onda no es generada por completo desde el principio, si no que es generada al vuelo durante la reproducción.

Decidí crear otros generadores de tonos para permitir a los usuarios personalizar el sonido del pitido y a algunas personas les gustó, incluyéndome a mí. Un usuario con pérdida auditiva informó que se sentía más cómodo con el generador de tonos sinusoidales.

Nota: La generación de tonos no es lo mismo que la función de salida de los tonos a su tarjeta de sonido. Así que incluso si usas el generador de tonos nativo de NVDA, seguirás viendo mejoras.

## Descarga.
	La última versión está disponible en
[este enlace](https://davidacm.github.io/getlatest/gh/davidacm/EnhancedTones)

## Requisitos
  Necesitas NVDA 2018.3 o posterior.

## Instalación
  Sólo tienes que instalarlo como un complemento de NVDA.

## Uso
  La funcionalidad del complemento se habilitará una vez que lo instales.  
  Para habilitarla o deshabilitarla, ve a la configuración de NVDA y selecciona "Tonos mejorados". En esa categoría puedes establecer los siguientes parámetros:

* Habilitar el complemento. Si se deshabilita, la función original será usada en su lugar.
* Generador productor de tonos: aquí puedes cambiar el generador de tonos. Seleccione uno y presione enter para guardar la configuración, luego pruebe el generador seleccionado.

## Para desarrolladores.

Si desea implementar nuevas formas de onda de generación de tonos, simplemente haga una clase similar a los generadores de tonos disponibles en el código y regístrelo usando la función registerGenerator.

Para cada clase de generador, debe proporcionar los métodos id, name, startGenerate y nextChunk.

puede implementar la clase AbstractGenerator que implementa los métodos más importantes. Los pasos mínimos para extender esta clase correctamente son implementar la función sampleGenerator, y debe proporcionar una identificación y un nombre para crear un generador válido. Es más fácil que crear un generador desde cero.

## contribuciones, reportes y donaciones

Si te gusta mi proyecto o este software te es útil en tu vida diaria y quieres contribuir de alguna manera, puedes donar a través de los siguientes métodos:

* [PayPal.](https://paypal.me/davicm)
* [Ko-fi.](https://ko-fi.com/davidacm)
* [criptomonedas y otros métodos.](https://davidacm.github.io/donations/)

Si quieres corregir errores, informar de problemas o nuevas características, puedes contactar conmigo en: <dhf360@gmail.com>.

  O en el repositorio de github de este proyecto:
  [enhanced tones en GitHub](https://github.com/davidacm/enhancedtones)

    Puedes obtener la última versión de este complemento en ese repositorio.
