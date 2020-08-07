import pelican, sys, subprocess, os.path, glob, re

def init(pelican_object):
    #global emojis, prefix
    global pelimoji_prog, pelimoji_replace
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
    # Now using 'glue' to make the sprite sheet itself
    glue_exec = ['glue',search_path, save_path, \
        '--namespace',"cemoji", \
        '--sprite-namespace',"", \
        '--css-template=plugins/pelimoji/css.j2', \
        '--recursive', ]\
        #'--padding=0.5',] \
        #'--png8']
    subprocess.call(glue_exec)
    # Now let's create a search-list of emoji names
    emojis = [ os.path.basename(x.decode('utf-8'))[:-4] for x in installed_emoji ]
    # And a regex pattern to find to avoid iterating
    pattern = ":" + prefix + "(?P<emoji>(" + ")|(".join(emojis) + ")):"
    # compile the pattern to global for speed given how massive it'll (potentially) be
    pelimoji_prog = re.compile(pattern)
    # And the pattern to replace it with!
    pelimoji_replace = "<i class=\"cemoji cemoji-\g<emoji>\" title=\":\g<emoji>:\"><span>:\g<emoji>:</span></i>"

def replace(content):
    fileext = str(content).split('.')[-1].lower()
    if fileext in ['md','html','rst','txt']:
        try:
            content._content = pelimoji_prog.sub(pelimoji_replace,content._content)
        except:
            print("Something went wrong editing {} for pelimoji, sorry".format(str(content)))

def register():
    pelican.signals.initialized.connect(init)
    pelican.signals.content_object_init.connect(replace)