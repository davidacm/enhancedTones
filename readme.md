# Enhanced tones NVDA Add-on #
This add-on redefines the way of manage the beep tones in NVDA.
To be in context. When NVDA beep a tone, it does the following:

1. open a nvwave player.
2. generate the tone.
3. send the generated tone to the player.
4. closes the player.

This can be problematic in some sound cards, like high delays when playing the tones, or not playing the first tones at all.
I had this issue in the past with one of my computers. So, that was the reason to create this add-on.

If you try this add-on, even if you don't have issues with the original way of tone generation, you can see that the tones are more fluid, especially in fastly repeated tones.

This add-on uses a thread to send the tones to the player, and the player is never closed.

Also, this add-on implements a custom tone generator, that is enabled by default. But you can change it to the NVDA's tones generator.
My custom tone generator is written purely in Python. So, is less eficient than the NVDA tone generator, but the difference is not noticeable.

I decided to mantain my tone generator because some people liked it, including myself. An user with hearing loss reported that he felt more comfortable with my tone generator.

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
* Library to generate tones:

## contributions, reports and donations

If you like my project or this software is useful for you in your daily life and you would like to contribute in some way, you can donate via the following methods:

* [PayPal.](https://paypal.me/davicm)
* [Ko-fi.](https://ko-fi.com/davidacm)
* [cryptocurrencies and other methods.](https://davidacm.github.io/donations/)

If you want to fix bugs, report problems or new features, you can contact me at: <dhf360@gmail.com>.

  Or in the github repository of this project:
  [Enhanced tones on GitHub](https://github.com/davidacm/enhancedtones)

    You can get the latest release of this add-on in that repository.
