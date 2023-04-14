# Enhanced tones NVDA Add-on #
This add-on redefines the way of manage the beep tones in NVDA to do the process more eficient.

Also, this add-on implements several wave generators, to let the user to customize the beep sound. It allows you to implement more generators very easily.

If you are interested in creating your own wave generator and integrating it into this add-on, see the  developer section.

## Features:

* Improves the beeping process by playing the tone in chunks until it completes, or is interrupted by a new tone.
* It implements several types of wave generators, which sound very different from each other. Have fun trying the different generators, maybe one you like!
* If a tone is interrupted by another with the same frequency, the wave will not be interrupted, it will only extend its duration. Thus avoiding annoying breaks when tones are played quickly. it's not always possible to avoid this situation, due to different factors.
* If a tone is interrupted by another of a different frequency, a frequency sweep will be made to jump to the new frequency. This also allows you to avoid breaks between tones.

The last two features allow for more pleasant sound when using features like sound mouse tracking.

## Download.
 The latest release is available to [download in this link](https://davidacm.github.io/getlatest/gh/davidacm/enhancedTones)

## Initial idea of this add-on.

This add-on was created to solve some issues with specific soundcards, those issues are less common now that we have better soundcard drivers. But some people reported that those issues are still present, like high delays when playing the tones, or not playing the first tones at all. Now, this add-on has more features, so this can be useful even if you don't have issues with the native tone generation. Try this yourself and see if it works for you.

### Description of the original beep process.

To be in context. When NVDA beep a tone, it does the following:

1. import the generateBeep.
2. stops the player.
3. generates the waveform tone.
4. sends the generated tone to the player.

This can be problematic in some sound cards, like high delays when playing the tones, or not playing the first tones at all. Seems that the issue happen by stopping the player, especially when this is repeated quickly.
I had this issue in the past with one of my computers. So, that was the reason to create this add-on. My add-on doesn't stop the player, and that fixed the issue.

### Description of the add-on beep process.

1. First, a background thread is created, this thread whill handle the beeps and communication with the player output.
2. The thread is kept waiting for data to emit a beep, using an event lock.
3. When the beep function is called, the information is sent to the thread and the thread lock is released.
4. The thread calls the function that initiates the generation of the waveform for the tone, and locks the event signal again.
5. It asks the generator for the waveform in form of chunks and sends each chunk to the output player. The generator can generate the waveform in parallel while sending, or generate the whole waveform at the beginning.
6. If while sending the waveform to the player the lock is released, it means that a request for a new beep was received, then it stops sending the data and jumps to step number 3 to start handling the required new beep.
7. If the entire waveform was sent to the player without interruption, it jumps to step number 2 to wait for another beep signal. Remember that the lock was blocked in step 4 so step 2 will be on hold again.

By this way, the output player is never stopped and the process is more efficient.

## Notes about this add-on.

If you try this add-on, even if you don't have issues with the original way of tone generation, you can see that the tones are more fluid, especially in fastly repeated tones.

Also, this add-on implements several tone generators, sine generator is enabled by default. But you can change it to the NVDA's tones generator.
My custom tone generators are written purely in Python. So, they are less eficient than the NVDA tone generator, but the difference is not noticeable.

I decided to create other tone generators to let users to customize the beep sound and some people liked it, including myself. An user with hearing loss reported that he felt more comfortable with sine tone generator.

Note: Tone generation is not the same as the function to output the tones to your sound card. So even if you use NVDA's native tone generator, you will still see improvements.

## Download.
	The latest release is available to
[download in this link](https://davidacm.github.io/getlatest/gh/davidacm/EnhancedTones)

## Requirements
  You need NVDA 2018.3 or later.

## Installation
  Just install it as a NVDA add-on.

## Usage
  The add-on functionality will be enabled once you install it.  
  To enable or disable it, go to NVDA settings and select "Enhanced tones". In that category you can set the following parameters:

* Enable this add-on. If disabled, the original function of NVDA will be used.
Generator to produce tones: you can change the tone generator here. Select one and press enter to save settings, then try the selected generator.

## for developers.

If you want to implement new tone generation waveforms, just make a class similar to the tone generators available in the code, and register it using the registerGenerator function.

For each generator class you must provide an id, name, startGenerate and nextChunk methods.

you can implement the AbstractGenerator class that implement the most important methods. The minimum steps to extend this class correctly is to implement the sampleGenerator function, and you need to provide an ID and name to create a valid generator. It's easier than create a generator from scratch.

## contributions, reports and donations

If you like my project or this software is useful for you in your daily life and you would like to contribute in some way, you can donate via the following methods:

* [PayPal.](https://paypal.me/davicm)
* [Ko-fi.](https://ko-fi.com/davidacm)
* [cryptocurrencies and other methods.](https://davidacm.github.io/donations/)

If you want to fix bugs, report problems or new features, you can contact me at: <dhf360@gmail.com>.

  Or in the github repository of this project:
  [Enhanced tones on GitHub](https://github.com/davidacm/enhancedtones)

    You can get the latest release of this add-on in that repository.
