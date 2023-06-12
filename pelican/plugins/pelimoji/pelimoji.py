import logging
import re
from os.path import abspath, dirname
from pathlib import Path

from jinja2 import Template
from PIL import Image, ImageColor

from pelican import signals

PLUGIN_ROOT = Path(dirname(dirname(abspath(__file__))))
logger = logging.getLogger(__name__)


def init(pelican_object):
    # Global variables for file extensions, emojis, prefix
    global pelimoji_ext, pelimoji_prog, pelimoji_replace
    # Let's build a list of installed emoji
    content_root = Path(pelican_object.settings.get("PATH", ()))
    search_path = Path(
        content_root, pelican_object.settings.get("PELIMOJI_SOURCE", "emoji")
    )
    output_path = Path(content_root, "emoji_map")
    pelican_object.settings["STATIC_PATHS"].append(str(output_path))
    pelimoji_ext = pelican_object.settings.get(
        "PELIMOJI_FILE_EXTENSIONS", ["md", "html", "rst"]
    )
    prefix = pelican_object.settings.get("PELIMOJI_PREFIX", "")
    output_map_path = "/emoji_map/emoji.png"
    if prefix:
        prefix = prefix + "-"

    emoji_images = list(search_path.rglob("*.png"))
    emoji_images.extend(list(search_path.rglob("*.gif")))
    emoji_images.extend(list(search_path.rglob("*.webp")))
    images = list(map(lambda x: Image.open(x), emoji_images))
    logger.debug(f"Found: {list(map(lambda x: str(x), emoji_images))}")
    width = max(image.size[0] for image in images)
    height = max(image.size[1] for image in images)
    cell_size = (width, height)

    count = len(images)
    grid_size = (cell_size[0] * count, cell_size[1])

    output_map: Image = Image.new("RGBA", grid_size, ImageColor.getrgb("#00000000"))
    context_images = []
    context = {
        "images": context_images,
        "prefix": prefix,
        "cell": {
            "width": cell_size[0],
            "height": cell_size[1],
            "count": count,
        },
        "grid": {
            "vertical": False,
            "width": grid_size[0],
            "height": grid_size[1],
        },
        "output": output_map_path,
    }
    image: Image
    for position, image in enumerate(images):
        x_offset = (cell_size[0] - image.size[0]) // 2
        y_offset = (cell_size[1] - image.size[1]) // 2
        x, y = position * cell_size[0], 0
        output_map.alpha_composite(image.convert("RGBA"), (x + x_offset, y + y_offset))
        imgpath = Path(image.filename)
        context_images.append(
            {
                "index": position + 1,
                "index0": position,
                "filename": imgpath.name,
                "stem": imgpath.stem,
                "position": {
                    "x": x,
                    "y": y,
                },
                "offset": {
                    "x": x_offset,
                    "y": y_offset,
                },
                "width": image.size[0],
                "height": image.size[1],
            }
        )
    output_map.save(output_path / "emoji.png")
    with open(Path(__file__).parent / "css.j2") as f:
        template = Template(f.read())
    with open(output_path / "emoji.css", "w") as f:
        f.write(template.render(context))

    # return output
    # Now let's create a search-list of emoji names
    emojis = map(lambda x: x.stem, emoji_images)
    # And a regex pattern to find to avoid iterating
    pattern = ":" + prefix + "(?P<emoji>(" + ")|(".join(emojis) + ")):"
    # compile pattern to global for speed, given how massive it'll (potentially) be
    pelimoji_prog = re.compile(pattern)
    # And the pattern to replace it with!
    pelimoji_replace = r'<i class="cemoji cemoji-\g<emoji>" aria-label="\g<emoji>" title="\g<emoji>"></i>'  # NOQA: E501


def replace(content):
    fileext = str(content).split(".")[-1].lower()
    if fileext in pelimoji_ext:
        try:
            content._content = pelimoji_prog.sub(pelimoji_replace, content._content)
        except TypeError:
            logger.warning(
                "Something went wrong editing {} for pelimoji, sorry".format(
                    str(content)
                )
            )


def register():
    signals.initialized.connect(init)
    signals.content_object_init.connect(replace)
