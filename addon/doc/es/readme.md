# Complemento Enhanced tones para NVDA.

Este complemento cambia la forma de gestionar los tonos en NVDA.
Para estar en contexto. Cuando NVDA emita un tono, hace lo siguiente:

1. abrir el reproductor nvwave.
2. generar el tono.
3. envía el tono generado al reproductor.
4. cierra el reproductor.

Esto puede ser problemático en algunas tarjetas de sonido, como alta latencia al reproducir los tonos, o no reproducir los primeros tonos en absoluto.
Tuve este problema en el pasado con uno de mis ordenadores. Así que esa fue la razón para crear este complemento.

Si pruebas este complemento, incluso si no tienes problemas con la forma original, podrás ver que los tonos son más fluidos, especialmente en los tonos que se repiten rápidamente.

Este complemento utiliza un hilo para enviar los tonos al reproductor, y el reproductor nunca se cierra.
Además, este complemento implementa un generador de tonos personalizado, que está configurado por defecto. Pero puedes cambiarlo por el generador de tonos de NVDA.
Mi generador de tonos personalizado está escrito puramente en Python. Por lo tanto, es menos eficiente que el generador de tonos del NVDA, pero la diferencia no es notable.

Decidí mantener mi generador de tonos porque a algunas personas les gustó, incluido yo mismo. Un usuario con pérdida de audición informó que se sentía más cómodo con mi generador de tonos.

Nota. La generación de tonos no es lo mismo que la función para emitir los tonos. Así que incluso si usas el generador de tonos nativo de NVDA, podrás observar las mejoras.

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
* Biblioteca para la generación de tonos.

## contribuciones, informes y donaciones

Si te gusta mi proyecto o este software te es útil en tu vida diaria y quieres contribuir de alguna manera, puedes donar a través de los siguientes métodos:

* [PayPal.](https://paypal.me/davicm)
* [Ko-fi.](https://ko-fi.com/davidacm)
* [criptomonedas y otros métodos.](https://davidacm.github.io/donations/)

Si quieres corregir errores, informar de problemas o nuevas características, puedes contactar conmigo en: <dhf360@gmail.com>.

  O en el repositorio de github de este proyecto:
  [enhanced tones en GitHub](https://github.com/davidacm/enhancedtones)

    Puedes obtener la última versión de este complemento en ese repositorio.
