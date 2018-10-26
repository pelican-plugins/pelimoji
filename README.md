### Pelimoji
## Simple emoji replacement for Pelican

Installation is simple! Drop this into your plugins directory and add it to be loaded. Copy `pelimoji.css` to a static path in your theme and ensure it'll be loaded in, whether using the `assets` plugin to compile it or not.

You'll need to set `PELIMOJI_PATH` to a directory within your `content` folder that is part of your `STATIC_PATHS` set, such as `images/emoji` if `images` is in your `STATIC_PATHS` setting.

 To that directory, add any square image files at least 16x16 ending in `.png`. These will be your emoji, addressable via the filename before the extension, such as `:gentoo:` if you had a file named `gentoo.png` in your `PELIMOJI_PATH`. This is case-sensitive if your filesystem is case-sensitive. 64x64 works best, but any size will do, including 512x512. Just remember, this will affect load speed for your pages.

 And that's it! Feel free to submit any suggestions!