import pelican, sys, subprocess, os.path, glob

def init(pelican_object):
    global emojis, prefix
    # Let's build a list of installed emoji
    content_root = pelican_object.settings.get('PATH',())
    search_path = "%s/emoji" % (content_root,)
    output_path = "emoji_map"
    save_path = "%s/%s" % (content_root,output_path)
    pelican_object.settings['STATIC_PATHS'].append(output_path)
    prefix = pelican_object.settings.get('PELIMOJI_PREFIX',"")
    if prefix != "":
        prefix = prefix + "-"
    installed_emoji = subprocess.check_output(['find',search_path,'-iname',"*.png"]).split(b'\n')
    glue_exec = ['glue',search_path, save_path, \
        '--namespace',"cemoji", \
        '--sprite-namespace',"", \
        '--css-template=plugins/pelimoji/css.j2', \
        '--recursive', ]\
        #'--padding=0.5',] \
        #'--png8']
    subprocess.call(glue_exec)
    # Great! Now let's create a search-list
    emojis = [ os.path.basename(x.decode('utf-8'))[:-4] for x in installed_emoji ]

def emoji_html(emoji):
    html = '<i class="cemoji cemoji-%s" title=":%s:"><span>:%s:</span></i>' % (emoji,emoji,emoji)
    return html

def replace(content):
    try:
        for emoji in emojis:
            search = ':%s%s:' % (prefix,emoji)
            content._content = content._content.replace(search, emoji_html(emoji))
    except:
        print("Could not edit content of %s" % (content,))

def register():
    pelican.signals.initialized.connect(init)
    pelican.signals.content_object_init.connect(replace)