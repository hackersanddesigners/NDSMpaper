from colour import Color
from PIL import Image, ImageDraw, ImageFont
import os, random, pathlib, time, sys
fonts = []
W, H = (300, 300)

def generateImage():

    src_path =  pathlib.Path.cwd() / "fonts"
    global fonts
    fonts = getFiles( src_path, 'ttf' )

    cnt = int(sys.argv[1])
    i = 0
    while i<cnt:
        img = Image.new('RGBA', (W, H), color = (255, 255, 255, 0))
        d = ImageDraw.Draw(img)

        randomShape( img, d )
        randomText( 'NDSM', d, H / 2- 50 )
        randomText( 'OPEN', d, H / 2 + 10 )

        # d.rectangle((0,0,W-1,H-1),outline=(0,0,0))
        timestr = time.strftime( "%Y-%m%d-%H%M%S" )
        filename = "image-%s-%d.png" % ( timestr, i )
        i = i + 1
        img.save( filename )
    # img.show()

def randomText( txt, drw, y ):
    font = str( random.choice ( fonts ) )
    fnt = ImageFont.truetype( font, 50)
    w,h = fnt.getsize( txt )
    drw.text( ( ( W - w ) / 2 , y ), txt, font=fnt, fill=randomColor(), align="center")

def randomColor():
    # c = Color( "yellow" )
    # c.luminance = random.uniform( 0.5, 1 )
    # return ( int( c.red * 255 ), int( c.green * 255 ), int( c.blue * 255 ) )
    return ( random.randint( 0, 255 ), random.randint( 0, 255 ), random.randint( 0, 255 ) )

def randomShape( img, drw ):
    shapes = (circle, rect)
    shape = random.choice ( shapes )
    img2 = Image.new('RGBA', (W,H) )
    drw2 = ImageDraw.Draw( img2 )
    shape( drw2 )
    img2 = img2.rotate( random.randint(0,360) )
    img.paste( img2 )

def circle( drw ):
    drw.ellipse(randomBox(), fill=randomColor() )

def rect( drw ):
    drw.rectangle(randomBox(), fill=randomColor())

def randomBox():
    w = random.randint(20,W)
    h = random.randint(20,H)
    return( int(W/2 - w/2), int(H/2-h/2), int(W/2+w/2), int(H/2+h/2) )

def getFiles( path, ext ):
    files = []
    for i, file in enumerate( sorted( path.glob( '*' + ext ) ) ):
        # print( file )
        files.append( file )
    return files

generateImage()
