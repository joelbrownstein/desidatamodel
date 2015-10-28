# License information goes here
# -*- coding: utf-8 -*-
"""
Generate an DESI data model stub for a given FITS file.

You will still need to hand edit the file to add descriptions, etc. but
it gives you a good starting point in the correct format.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
# The line above will help with 2to3 support.
def main():
    """Program to run if called as an executable."""
    import xml.etree.ElementTree as ET
    import re
    from sys import argv, stderr
    from argparse import ArgumentParser
    from os import getenv
    from os.path import basename, join
    from . import file_size, get_uri, parse_header, rst
    try:
        import fitsio
    except ImportError:
        print("This script requires fitsio, available from https://github.com/esheldon/fitsio",file=stderr)
        return 1
    parser = ArgumentParser(description=__doc__,prog=basename(argv[0]))
    parser.add_argument('filename',help='A FITS file.',metavar='FILE',nargs='+')
    options = parser.parse_args()
    template = join(getenv('DESIDATAMODEL'),'etc','template.html')
    for f in options.filename:
        rstkeywords = dict()
        #
        # Create a title
        #
        basef = basename(f)
        try:
            modelname = basef[0:basef.index('-')]
        except ValueError:
            modelname = basef[0:basef.index('.')]
        rstkeywords['title'] = modelname
        rstkeywords['titlehighlight'] = '='*len(rstkeywords['title'])
        rstkeywords['filename'] = basef
        rstkeywords['filetype'] = 'FITS'
        rstkeywords['filesize'] = file_size(f)
        #
        #- Read the file and parse the headers
        #
        fx = fitsio.FITS(f)
        nhdr = len(fx)
        if nhdr > 99:
            hduname = 'HDU{0:03d}'
        elif nhdr > 9:
            hduname = 'HDU{0:02d}'
        else:
            hduname = 'HDU{0:1d}'
        contents_table = [('Number','EXTNAME','Type','Contents')]
        headers = list()
        hdu_sections = list()
        for k in range(nhdr):
            headers.append(fx[k].read_header())
            if k > 0 and 'EXTNAME' in headers[k]:
                extname = headers[k]['EXTNAME'].strip()
            else:
                extname = ''
            if k > 0:
                exttype = headers[k]['XTENSION'].strip()
            else:
                exttype = 'IMAGE'
            contents_table.append((hduname.format(k)+'_',extname,exttype,'*Brief Description*'))
            sec_title = hduname.format(k)
            hdu_sections.append(sec_title)
            hdu_sections.append('-'*len(sec_title))
            hdu_sections.append('')
            if extname != '':
                hdu_sections.append('EXTNAME = '+extname)
                hdu_sections.append('')
            hdu_sections.append('*Summarize the contents of this HDU.*')
            hdu_sections.append('')
            hdu_sections += parse_header(headers[k])
        #
        # Construct the contents table.
        #
        colsizes = [max(map(len,col)) for col in zip(*contents_table)]
        highlight = ' '.join(['='*k for k in colsizes])+"\n"
        colformat = ' '.join(['{{{0:d}:{1:d}}}'.format(i,s) for i,s in enumerate(colsizes)])+"\n"
        rstkeywords['contents_table'] = highlight
        for k in range(nhdr+1):
            rstkeywords['contents_table'] += colformat.format(*contents_table[k])
            if k == 0:
                rstkeywords['contents_table'] += highlight
        rstkeywords['contents_table'] += highlight
        rstkeywords['hdu_sections'] = '\n'.join(hdu_sections)
        #
        # Write the file
        #
        with open("{0}.rst".format(modelname),'w') as m:
            m.write(rst.format(**rstkeywords))
    return 0