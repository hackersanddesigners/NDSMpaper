from PIL import Image, ImageDraw
import os, random, pathlib, time, sys

width = 44 #mm
height = 320 #mm
dpi = 300
W = int( width / 2.54 * dpi )
H = int( height / 2.54 * dpi )
contain_images = True

def generateImage():
    print( "Generating image. W: %d H: %d DPI: %d" % ( W, H, dpi ) )
    canvas = Image.new( 'RGB', ( W, H ), color = ( 255, 255, 255 ) )

    src_path =  pathlib.Path.cwd() / "images" # source folder to get images from
    images = getFiles( src_path, 'jpg' ) # get the images
    num_picked = random.randint( 3, 5 ) # how many should we place?
    picked = random.choices ( images, k = num_picked ) # pick a few
    for image_path in picked:
        print( image_path )
        randomImage( image_path, canvas ) # place them on the canvas

    timestr = time.strftime( "%Y-%m%d-%H%M%S" )
    filename = "image-%s.jpg" % ( timestr )

    canvas.save( filename )
    # img.show()
    print( "Done. Generated %s " %  filename )

# Place image randomly on the canvas
def randomImage( image_path, canvas ):
    Image.MAX_IMAGE_PIXELS = 933120000 # Sets the maximum file size higher.

    img = Image.open( image_path )
    print( img.width, img.height )

    if img.width > W: # the image does not fit on the canvas
        nw = W
        nh = int( W / img.width * img.height )
        print( "Resizing. Org: %d, %d New: %d, %d" % ( img.width, img.height, nw, nh ) )
        img = img.resize( ( nw, nh ), PIL.Image.BICUBIC )

    if not contain_images: # possibly out of the image
        x = random.randint( 0, W )
        y = random.randint( 0, H )
    else: # make sure we can see it completely
        x = random.randint( 0, W - img.width )
        y = random.randint( 0, H - img.height )
    canvas.paste( img , (x, y) )

# gets all files with .ext from a directory
def getFiles( path, ext ):
    files = []
    for i, file in enumerate( sorted( path.glob( '*' + ext ) ) ):
        files.append( file )
    return files

generateImage()
