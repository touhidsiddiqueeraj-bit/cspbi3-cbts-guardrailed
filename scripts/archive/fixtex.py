import re
p = '/home/touhid/Documents/texflowmcp/workspace/document.tex'
t = open(p).read()
BS = chr(92)
t2 = re.sub(BS * 4 + r'(?=[A-Za-z%])', lambda m: BS, t)
open(p, 'w').write(t2)
print('done')
