import pelican, sys, glob, os.path

def init(pelican_object):
    global emojis, emojipath
    # Let's build a list of installed emoji
    contentroot = pelican_object.settings.get('PATH',())
    emojipath = pelican_object.settings.get('PELIMOJI_PATH', ())
    searchpath = "%s/%s/*.png" % (contentroot,emojipath)
    installed_emoji = glob.glob(searchpath)
    # Great! Now let's create a search-list 
    emojis = [ os.path.basename(x)[:-4] for x in installed_emoji ]

def replace(path, context):
    # Now, we'll open any written files to search for the matching search-strings
    with open(path, 'r') as f:
        s = f.read()
        for emoji in emojis:
            search = ':%s:' % (emoji,)
            s = s.replace(search, emoji_html(emoji))
    with open(path, 'w') as f:
        f.write(s)

def emoji_html(emoji):
    html = '<img class="pelimoji" src="/%s/%s.png" class="pelimoji" title=":%s:" alt=":%s:" />' % (emojipath,emoji,emoji,emoji)
    return html

def register():
    pelican.signals.initialized.connect(init)
    pelican.signals.content_written.connect(replace)
