'''
size-0{
   font-size: 11px;
}

size-1{
   font-size: 12px;
}
'''

CSS_SIZES = range(0, 6) # 1,2...6 for use in your css-file size-1, size-2, etc.

TAGS = {
    'python' : 28059,
    'html' : 19160,
    'tag-cloud' : 40,
}

MAX = max(TAGS.values()) # Needed to calculate the steps for the font-size

STEP = MAX / len(CSS_SIZES)


print '<html>'
print '  <head>'
print '    <title>OmniFocus</title>'
print '    <style type="text/css">'
print '        size-0{'
print '           font-size: 6px;'
print '        }'
print '        size-1{'
print '           font-size: 8px;'
print '        }'
print '        size-2{'
print '           font-size: 10px;'
print '        }'
print '        size-3{'
print '           font-size: 12px;'
print '        }'
print '        size-4{'
print '           font-size: 14px;'
print '        }'
print '        size-5{'
print '           font-size: 16px;'
print '        }'
print '        size-6{'
print '           font-size: 18px;'
print '        }'
print '    </style>'
print '  </head>'
print '  <body>'



for tag, count in TAGS.items():
    css = count / STEP        
    print '<font size="%s">%s</font>' % (css, tag)
    
print '  </body>'
print '</html>'