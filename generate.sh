#! /usr/bin/env python

import os, sys, getopt, random, subprocess
import pathlib
from bs4 import BeautifulSoup
import argparse
import shutil
from shutil import copyfile

cwd =  pathlib.Path.cwd()
pathlib.Path( cwd / 'srcdocs' ).mkdir( parents=True, exist_ok=True )
src_path = cwd / 'srcdocs'
pathlib.Path( cwd / 'build' / 'clean' ).mkdir( parents=True, exist_ok=True )
dest_path = cwd / 'build' / 'clean'

def main(argv):
    parser = argparse.ArgumentParser(description='Generate H&D Book')
    parser.add_argument('-c','--clean', help='Cleanup input HTML files. Removes unwanted html & css. Saves files in srcdocs/clean', action='store_true' )
    parser.add_argument('-b','--build', help='Combines the files in build/clean (created by running this script with -c option) and creates a PDF', action='store_true' )
    parser.add_argument('-o','--output', help='Output pdf filename. Default: book.pdf', default="book.pdf" )
    args = parser.parse_args()

    if args.build:
        build( args.output )
    elif args.clean:
        cleanFiles()

def cleanFiles():
    shutil.rmtree(dest_path)
    pathlib.Path( cwd / 'build' / 'clean' ).mkdir( parents=True, exist_ok=True )
    for i, file in enumerate( sorted( src_path.rglob( '*.html' ) ) ):
        with open( file, 'r' ) as src_file:
            content = src_file.read()
            soup = BeautifulSoup( content, 'html.parser' )
            print( os.path.dirname( file ) )
            # move linked images to build and adjust src attr
            for img in soup.select( 'img' ):
                name = os.path.basename( img['src'] )
                filepath =  pathlib.Path( os.path.dirname( file ) )
                imgpath =  pathlib.Path(  img['src'] )
                pathlib.Path( cwd / 'build' / 'clean' / 'images' / str( i )  ).mkdir( parents=True, exist_ok=True )
                dest = pathlib.Path( cwd / 'build' / 'clean' / 'images' / str( i ) / name )
                copyfile( filepath / imgpath, dest  )
                # pathlib.Path( cwd / 'build' / 'clean' / str( i ) /  ).mkdir( parents=True, exist_ok=True )
                img[ 'src' ] = ('images/%s/' % i ) + name

            # del soup.body[ 'class' ]
            # for style in soup.head.find_all( 'style' ):
            #     style.decompose()

            # for class_el in soup.select( '[class],[id]' ):
            #     del class_el[ 'class' ]
            #     del class_el[ 'id' ]

            for inline_styles in soup.select( '[style]' ):
                del inline_styles[ 'style' ]


            # for p_span in soup.select( 'p > span, h1 > span' ):
            #     p_span.unwrap()

            for empty_el in soup.select( 'p:empty, span:empty' ):
                empty_el.decompose()

            clean = soup.prettify()

            with open( dest_path / file.name, 'w' ) as dest_file:
                dest_file.write( clean )
                print( "Wrote build/clean/%s " % os.path.basename( dest_file.name ) )


def build( output_filename ):
    template = pathlib.Path.cwd() / 'lib' / 'template.html'
    with open( template, 'r' ) as book:
        content = book.read()
    book_html = BeautifulSoup( content, 'html.parser' )
    container = book_html.body.div

    for idx, file in enumerate( sorted( dest_path.rglob( '*.html' ) ) ):
        with open( file, 'r' ) as src_file:
            content = src_file.read()
            body = formatDocument( content, idx )
            container.append( body )

    dest_file = pathlib.Path.cwd() / 'build' / 'book.html'
    with open( dest_file, 'w' ) as output:
        output.write( book_html.prettify() )

    pdf_path = pathlib.Path.cwd() / 'build' / output_filename
    print( str( pdf_path ) )

    subprocess.Popen( [ 'weasyprint %s %s' % ( dest_file, pdf_path ) ], shell = True ) # add to suppress output: , stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL )


import re

def formatDocument( content, idx ):
    soup = BeautifulSoup( content, 'html.parser' )
    body = soup.body

    wrapper = soup.new_tag("article")
    body.wrap( wrapper )
    # transform the body to an article tag and copy it to the output doc
    body.name = 'div'
    body[ 'class' ] = 'columns cols-' + str( random.randint( 2, 4 ) ) + ' bodyfont-' + str( random.randint( 1, 5 ) )
    # scoped does work in Weasyprint regrettably so we add an id to the article and suffix the css
    body[ 'id' ] = 'article-' + str( idx )
    for header in body.select( 'h1, h2' ):
        rndHeadingFont( header )
    for h1 in body.select( 'h1' ):
        wrapper.insert( 0, h1 ) # place the h1 outside of the article so it can be fullwidth
    for img in soup.select( 'img' ):
        img[ 'src' ] = 'clean/' + img[ 'src' ] # adjust image path

    # get the style tag from head and turn it into a style scoped to the article
    # this isnt going to be pretty...

    for style in soup.head.find_all( 'style' ):
        replaced = re.sub("{", "{\n", style.string) # force everything on a own line.
        replaced = re.sub("(?!;)}", ";}\n", replaced) # sometimes the semicolon is missing
        replaced = re.sub("([;|}])", "\g<1>\n", replaced) # more new lines
        lines = re.split("\n+", replaced)
        output = ''
        for line in lines:
            if( line.endswith( ';' ) ):
                # remove all css attributes that are not italic/bold
                statement = line.strip()
                if ( statement.startswith( 'font-weight' ) or statement.startswith( 'font-style' ) ):
                    output += "\n" + line
            else:
                if "{" in line:
                    line = '#article-' + str( idx ) + " " + line # prefix with article id
                output += "\n" + line
        style.string = output
        style[ 'scoped' ] = 'scoped' # scoped does work in Weasyprint regrettably
        wrapper.insert( 0, style )

    return wrapper

def rndHeadingFont( header ):
    header[ 'class' ] = "headingfont-" + str( random.randint( 1, 17 ) )
    return header

if __name__ == "__main__":
   main( sys.argv[ 1: ] )
