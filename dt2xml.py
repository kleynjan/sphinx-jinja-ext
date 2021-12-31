#!/usr/bin/env python
# .doctree to .xml prettyprint
# usage: dt2xml <doctree_filename>
# 
import pickle, sys, os

fname, fin_ext = os.path.splitext( sys.argv[1] )

if fin_ext=='':
    fin_ext = '.doctree'

fin = fname + fin_ext
fout = fname + '.xml'
print( 'Reading %s, writing %s' % (fin,fout) )

doc = pickle.load( open( fin, "rb") )
xml = doc.asdom().toprettyxml()

text_file = open( fout, "w" )
n = text_file.write( xml )
text_file.close()
