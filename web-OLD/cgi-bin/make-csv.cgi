#!/usr/bin/python
import cgi
import cgitb; cgitb.enable() # Optional; for debugging only
from subprocess import call


print "Content-Type: text/html"
print ""

selected = cgi.FieldStorage()

selected[0] = current

for i in selected:
    type,sample = split('_')
    file = "analyses/abun/" + type + "/" + sample + "/" + sample + "_" + taxa + ".txt"
    call([sort -k1 file >tmp.txt])
    call([join -e 0 -o auto -a1 -a2 current i])


