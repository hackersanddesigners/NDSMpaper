from PIL import Image, ImageDraw
import os, random, pathlib, time, sys
import argparse

width = 44 #mm
height = 320 #mm
dpi = 300
W = int( width / 2.54 * dpi )
H = int( height / 2.54 * dpi )
contain_images = True
args = None

def main(argv):
    global args, width, height, dpi
    parser = argparse.ArgumentParser(description='Generate sidebar image for the NDSM newspaper')
    parser.add_argument('--input', help='name of input file directory', default="images" )
    parser.add_argument('--output', help='Output jpg filename. Defaults to input dir name + timestamp' )
    parser.add_argument('--width', help='Width of the output image in mm', type=int )
    parser.add_argument('--height', help='Height of the output image in mm',type=int )
    parser.add_argument('--dpi', help='DPI of the output image',type=int )
    args = parser.parse_args()
    recalc = False
    if args.width:
        width = args.width
        recalc = True
    if args.height:
        height = args.height
        recalc = True
    if args.dpi:
        dpi = args.dpi
        recalc = True
    if recalc:
        calcDimensions
    generateImage()

def calcDimensions():
    global W, H
    W = int( width / 2.54 * dpi )
    H = int( height / 2.54 * dpi )

def generateImage():
    print( "Generating image. W: %d H: %d DPI: %d" % ( W, H, dpi ) )
    canvas = Image.new( 'RGB', ( W, H ), color = ( 255, 255, 255 ) )

    src_path =  pathlib.Path.cwd() / args.input # source folder to get images from
    images = getFiles( src_path, 'jpg' ) # get the images
    num_picked = random.randint( 3, 5 ) # how many should we place?
    picked = random.choices ( images, k = num_picked ) # pick a few
    for image_path in picked:
        print( image_path )
        randomImage( image_path, canvas ) # place them on the canvas

    if args.output == None:
        timestr = time.strftime( "%Y-%m%d-%H%M%S" )
        args.output = "build/" + args.input + "-" + timestr + ".jpg"
    else:
        args.output = "build/" + args.output + ".jpg"
    canvas.save( args.output )
    # img.show()
    print( "Done. Generated %s " %  args.output )

# Place image randomly on the canvas
def randomImage( image_path, canvas ):
    Image.MAX_IMAGE_PIXELS = 933120000 # Sets the maximum file size higher.

    img = Image.open( image_path )
    print( img.width, img.height )

    if img.width > W: # the image does not fit on the canvas
        nw = W
        nh = int( W / img.width * img.height )
        print( "Resizing. Org: %d, %d New: %d, %d" % ( img.width, img.height, nw, nh ) )
        img = img.resize( ( nw, nh ), Image.BICUBIC )

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

if __name__ == "__main__":
   main( sys.argv[ 1: ] )
