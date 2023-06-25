# Pelimoji

[![Build Status](https://img.shields.io/github/actions/workflow/status/pelican-plugins/pelimoji/main.yml?branch=main)](https://github.com/pelican-plugins/pelimoji/actions)
[![PyPI Version](https://img.shields.io/pypi/v/pelican-markdown-include)](https://pypi.org/project/pelican-markdown-include/)
![License](https://img.shields.io/pypi/l/pelican-markdown-include?color=blue)

Pelimoji is a [Pelican][] plugin that adds support for custom emoji to your site.

Installation
------------

This plugin can be installed via:

    python -m pip install pelimoji

As long as you have not explicitly added a `PLUGINS` setting to your Pelican settings file, then the newly-installed plugin should be automatically detected and enabled. Otherwise, you must add `pelimoji` to your existing `PLUGINS` list. For more information, please see the [How to Use Plugins](https://docs.getpelican.com/en/latest/plugins.html#how-to-use-plugins) documentation.

Usage
-----

Within your `PATH` content root create a directory called `emoji`. To that directory, add any square image files at least 16x16 ending in `.png`. These will be your emoji, addressable via the filename before the extension, such as `:gentoo:` if you had a file named `gentoo.png` in your `PELIMOJI_PATH`. This is case-sensitive if your filesystem is case-sensitive. 64x64 works best, but any size will do, including 512x512. Just remember, this will affect load speed for your pages.

When compiling your site, the following directory will be created and automatically added to your `STATIC_PATHS`: `PATH/emoji_map/`. You'll need to ensure that `PATH/emoji_map/emoji.css` is loaded as a stylesheet, whether using something like `webassets` or `cssmin`, or by adding directly.

You may optionally also specify a `PELIMOJI_PREFIX` to require if you might have multiple sets of colon-tags that'd overlap. Whereas I might normally use `:thumbs-up:`, I could then specify `PELIMOJI_PREFIX = "emoji"`, and my tag would instead be `:emoji-thumbs-up:`.

By default this plugin operates on source content files with the following file extensions: `["md", "html", "rst"]`, corresponding to Markdown, HTML, and reStructuredText. If you, say, want this plugin to also process files ending in `.txt`, you should add the following to your settings file:

```python
PELIMOJI_FILE_EXTENSIONS = ["md", "html", "rst", "txt"]
```

Contributing
------------

Contributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].

To start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.

[Pelican]: https://getpelican.com
[existing issues]: https://github.com/pelican-plugins/pelimoji/issues
[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html
