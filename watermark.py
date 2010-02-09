#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Modified by Eric on 2010-02-09.
Copyright (c) 2010 __lxneng@gmail.com__. All rights reserved.
"""
import optparse
import os
import Image
import ImageEnhance
#------------------------global variables------------------------
logo = None
POSITION = ('LEFTTOP','RIGHTTOP','CENTER','LEFTBOTTOM','RIGHTBOTTOM')
PADDING = 10
MARKIMAGE = 'watermark_logo.png'

#---------------------------------------------------------------
def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def watermark(imagefile, markfile, position=POSITION[4], opacity=1):
    """Adds a watermark to an image."""    
    im = Image.open(imagefile)
    mark = Image.open(markfile)    
    if opacity < 1:
        mark = reduce_opacity(mark, opacity)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    # create a transparent layer the size of the image and draw the
    # watermark in that layer.
    layer = Image.new('RGBA', im.size, (0,0,0,0))
    if position == 'title':
        for y in range(0, im.size[1], mark.size[1]):
            for x in range(0, im.size[0], mark.size[0]):
                layer.paste(mark, (x, y))
    elif position == 'scale':
        # scale, but preserve the aspect ratio
        ratio = min(
            float(im.size[0]) / mark.size[0], float(im.size[1]) / mark.size[1])
        w = int(mark.size[0] * ratio)
        h = int(mark.size[1] * ratio)
        mark = mark.resize((w, h))
        layer.paste(mark, ((im.size[0] - w) / 2, (im.size[1] - h) / 2))
    elif position == POSITION[0]:
        #lefttop
        position = (PADDING,PADDING)
        layer.paste(mark, position)
    elif position == POSITION[1]:
        #righttop
        position = (im.size[0] - mark.size[0]-PADDING, PADDING)
        layer.paste(mark, position)
    elif position == POSITION[2]:
        #center
        position = ((im.size[0] - mark.size[0])/2,(im.size[1] - mark.size[1])/2)
        layer.paste(mark, position)
    elif position == POSITION[3]:
        #left bottom
        position = (PADDING,im.size[1] - mark.size[1]-PADDING,)
        layer.paste(mark, position)
    else:
        #right bottom (default)
        position = (im.size[0] - mark.size[0]-PADDING, im.size[1] - mark.size[1]-PADDING,)
        layer.paste(mark, position)
        
    # composite the watermark with the layer
    return Image.composite(layer, im, layer)



def list_dir(srcdir = None,prefix = ''):
    
    if srcdir == None:
        return
    for filename in os.listdir(srcdir):
        srcfilepath = os.path.join(srcdir, filename)
        if os.path.isfile(srcfilepath):
            if srcfilepath[-3:] in ('bmp','jpg','gif','png'):
                #addlogo(srcfilepath)
                try:
                    watermark(srcfilepath,MARKIMAGE,POSITION[3],opacity=0.7).save(srcfilepath,quality=90)
                except:
                    continue
                print srcfilepath
        elif os.path.isdir(srcfilepath):
            list_dir(srcfilepath, prefix)
    return
def main():
    usage = 'usage: %prog -d datadir'
    parser = optparse.OptionParser(usage)
    parser.add_option(
        '-d',
        '--datadir',
        dest='datadir',
        help='dir used to which folder pics do you want watermark',
        type='string'
    )

    (options, args) = parser.parse_args()

    if options.datadir == None:
        parser.error('must has -d option!')
    elif not os.path.isdir(options.datadir):
        parser.error('source directory do not exist!')
    print options.datadir
    
    list_dir(options.datadir, options.datadir)
    
if __name__ == '__main__':
    main()
