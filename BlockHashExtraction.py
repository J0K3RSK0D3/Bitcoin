import urllib.request
import pprint
import time
import pickle
HASH_URL = 'Https://www.blockchain.com/btc/block-height/'
try:
 BTC_BLOCK_HASHES = pickle.load(open('btc-block-hashes.vnm','rb'))
except Exception as e:
 print('Block Hash File Needed')
 BTC_BLOCK_HASHES = dict()
 pickle.dump(BTC_BLOCK_HASHES,open('btc-block-hashes.vnm','wb'))

def Clone_System(target):
 try:
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  url = str(target)
  req = urllib.request.Request(url, headers = headers)
  x = urllib.request.urlopen(req)
  l = str(x.read())
  return l
 except Exception as e:
  print('Error Returning Url [{}]'.format(e))

def _grabFirst(string):
 position = 0
 for i in string:
  if str(i) == '>' and string[position+1] == '0':
   #print('i: [{}], Position: [{}]'.format(str(i),position))
   return position +1
  else:
   #print('i: [{}], Position: [{}]'.format(str(i),position))
   position += 1
def _grabSecond(string):
 allowed = ['a','b','c','d','e','f','0','1','2','3','4','5','6','7','8','9']
 position = 0
 for i in string:
  if i == '<' and string[position-1] in allowed:
   #print('i: [{}], Position: [{}]'.format(str(i),position))
   return position
  else:
   #print('i: [{}], Position: [{}]'.format(str(i),position))
   position += 1

def _main(block):
 global Block
 BTC_BLOCK_HASHES = pickle.load(open('btc-block-hashes.vnm','rb'))
 Hash = Clone_System(HASH_URL+str(block))
 XHash = Hash[6500:6959]
 #print('Sorting [{}]'.format(XHash))
 starting = _grabFirst(XHash)
 ending = _grabSecond(XHash)
 AHash = XHash[int(starting):int(ending)]
 print('Selected AHash: [{}]'.format(AHash))
 if len(AHash) == 64:
  if str(block) not in BTC_BLOCK_HASHES:
   print('Adding Data [{}] For Block [{}]'.format(XHash,str(block)))
   print('Real Hash: [{}]'.format(AHash))
   BTC_BLOCK_HASHES[str(block)] = AHash
   pickle.dump(BTC_BLOCK_HASHES,open('btc-block-hashes.vnm','wb'))
  elif str(block) in BTC_BLOCK_HASHES:
   if BTC_BLOCK_HASHES[str(block)] != AHash:
    print('We Have A Error, Different Hashes For Block: [{}].'.format(str(block)))
    print('Real Hash: [{}]'.format(AHash))
    BTC_BLOCK_HASHES[str(block)] = AHash
    pickle.dump(BTC_BLOCK_HASHES,open('btc-block-hashes.vnm','wb'))
   else:
    print('Hash Already Logged For Block [{}].'.format(str(block)))
 else:
  print('Length Is Off...[{}].'.format(len(AHash)))
  paused = input('>>: ')
 
_Started = False
while True:
 global Block
 if _Started == False:
  BTC_BLOCK_HASHES = pickle.load(open('btc-block-hashes.vnm','rb'))
  print('Which Block Are We Starting At?')
  Block = int(input('>>: '))
  _Started = True
 try:
   _main(Block)
   Block += 1
 except Exception as e:
  print('We Had A Error: [{}]'.format(e))
  try:
   print('Resetting Connection')
   mimic = Block - 5
   Block = mimic
   _main(Block)
  except Exception as e:
   print('Failed To Reset Connection. Error: [{}].'.format(e))
   exit()
  
  
 

