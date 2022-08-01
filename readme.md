# Enhanced tones NVDA Add-on #
This add-on redefines the way of manage the beep tones in NVDA.
To be in context. When NVDA beep a tone, do the following:

1. open a nvwave player.
2. generate the tone.
3. send the generated tone to the player.
4. closes the player.

This can be problematic in some sound cards, like high delays when playing the tones, or not playing the first tones at all.
I had this issue in the past with one of my computers. So, that was the reason to create this add-on.

If you try this add-on, even if you don't have issues with the original one, you can see that the tones are more fluid, overall in fastly repeated tones.

This add-on uses a thread to send the tones to the player, and the player is never closed.
Also, this add-on implements a own tone generator, but you can use NVDA's tone generator if you want.

I decided to keep my tone generator because some people liked it.



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

* Enable enhanced tones.
* select the tone generator that you prefer to use.

## contributions, reports and donations

If you like my project or this software is useful for you in your daily life and you would like to contribute in some way, you can donate via the following methods:

* [PayPal.](https://paypal.me/davicm)
* [Ko-fi.](https://ko-fi.com/davidacm)
* [cryptocurrencies and other methods.](https://davidacm.github.io/donations/)

If you want to fix bugs, report problems or new features, you can contact me at: <dhf360@gmail.com>.

  Or in the github repository of this project:
  [Enhanced tones on GitHub](https://github.com/davidacm/enhancedtones)

    You can get the latest release of this add-on in that repository.
