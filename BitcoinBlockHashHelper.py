'''
 Sub-Module To Scan / Verify & Locate Last Block Stored Within btc-block-hashes.vnm
 Requires Pickle
 @User: Later Version Will Include Transaction Hash Tree.
'''
 

import pickle
FILE = 'btc-block-hashes.vnm'
ALLOWED = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
COUNTER = 43264
COUNTING = True
while COUNTING:
 OPEN = pickle.load(open(FILE,'rb'))
 while COUNTER < 500000 and COUNTING:
  if str(COUNTER) in OPEN:
   print('Hash [{}] Located For Block [{}]'.format(OPEN[str(COUNTER)],str(COUNTER)))
   if len(OPEN[str(COUNTER)]) == 64:
    for l in OPEN[str(COUNTER)]:
     if l not in ALLOWED:
      print('Invalid Character [{}] In Hash [{}] In Block [{}] Please Investigate'.format(l,OPEN[str(COUNTER)],str(COUNTER)))
      COUNTING = False
   else:
    print('Invalid Length [{}] For Hash [{}] In Block [{}] Please Investigate'.format(len(OPEN[str(COUNTER)]),OPEN[str(COUNTER)],str(COUNTER)))
    COUNTING = False
   if COUNTING:
    print('Block Hash Has Been Verified For Block [{}]'.format(str(COUNTER)))
    COUNTER += 1
  else:
   print('I Do Belive We Are On Block [{}]'.format(str(COUNTER)))
   COUNTING = False
