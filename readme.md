# NDSM newspaper 2019 generator

## Description
Script to auto-generate a book from a bunch of documents downloaded from Google
docs as HTML files. The script will remove most of the CSS and combine all
the documents in one file: build/book.html. Then Weasyprint converts the
HTML to PDF.
The fonts used are all open source fonts.

## Installation

Make sure you have weasyprint installed as per instructions :
https://weasyprint.readthedocs.io/en/stable/install.html

### Mac
On mac you'll have to install some stuff with Homebrew, so read the guide.
We had a problem with a Cairo version, so we had to force a version with
```pip install cairocf==0.9.0```

Then:

``` pip install WeasyPrint ```

And install the other dependencies

``` pip install pathlib beautifulsoup4 ```

We had locale errors on some machines. Set locale with:
```
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```
or add those to the shells .rc file

## Usage

Export the documents as HTML (File &gt; Download &gt; HTML page...) from Google docs and place in ./srcdocs

Run clean command
---
Google docs places a lot of representational css inline in the document.
This command cleans most of that up. We only leave the font-weight and font-style
rules because we actually need those.
The cleaned documents will be placed in ./build/clean. Adjust those as needed.
By default is searches for files in the .srcdocs folder

``` python generate.py --clean ```

Or specify source folder:
```python generate.sh --clean --input ./srcdocs_en```

Run build command
---
This will combine all the files in ./build/clean by getting the contents of the
document body and wrapping that in an &lt;article&gt; tag.
The combined document will be saved as  ./build/book.html and this file is used
by Weasyprint to generate ./build/book-&lt;date&gt;.html and ./build/book-&lt;date&gt;.pdf

``` python generate.py --build ```


*optionally*
Set the output filename by adding --output [filename]

``` python generate.py --build --output ndsm_papger.pdf ```

Create PDF from preexisting html
---
This option allow for small text changes. To do that edit the generated
/build/book-&lt;date&gt;.html and pass that to the --html flag

```python generate.sh --html book-2019-0920-143629.html```

Examples
---
Clean the input html and generate a Pdf

```python generate.sh --clean --input ./srcdocs_en && python generate.sh --build```


## Resources
https://www.w3.org/TR/css-page-3/#cascading-and-page-context
https://www.smashingmagazine.com/2015/01/designing-for-print-with-css/

## Fonts
- Todo. Add links to font authors
