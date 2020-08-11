# Pelimoji
### Simple emoji replacement for Pelican

Installation is simple! Drop this into your plugins directory and add it to be loaded.

Within your `PATH` content root create a directory called `emoji`. To that directory, add any square image files at least 16x16 ending in `.png`. These will be your emoji, addressable via the filename before the extension, such as `:gentoo:` if you had a file named `gentoo.png` in your `PELIMOJI_PATH`. This is case-sensitive if your filesystem is case-sensitive. 64x64 works best, but any size will do, including 512x512. Just remember, this will affect load speed for your pages.
 
 When compiling your site, the following directory will be created and automatically added to your STATIC_PATHS: `PATH/emoji_map/`. You'll need to ensure that `PATH/emoji_map/emoji.css` is loaded as a stylesheet, whether using something like `webassets` or `cssmin`, or if adding directly. 

You may optionally also specify a `PELIMOJI_PREFIX` to require if you might have multiple sets of colon-tags that'd overlap. Whereas I might normally use `:thumbs-up:`, I could then specify `PELIMOJI_PREFIX = "emoji"`, and my tag would instead be `:emoji-thumbs-up:`.

Installation of `glue` may require additional development header packages be installed to your system, or you may install `glue` from your OS's package manager if version `0.13` or newer is available.
