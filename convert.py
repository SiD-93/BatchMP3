#!/usr/bin/python
import os
import re
import multiprocessing

q = multiprocessing.Queue()

def encodeAudio ():
  while not q.empty():
    sourcefile = q.get()
    print sourcefile
    targetfile = sourcefile[:-3] + 'mp3'
    commandline = "ffmpeg -i \"" + sourcefile  +  "\" -acodec libmp3lame -ac 2 -ab 192k -vn -y \""+ targetfile + "\""
    os.popen (commandline) 

cores=multiprocessing.cpu_count()

extensions = ['avi','flv', 'mp4', 'wav', 'ogg', 'mpg', 'aac', 'flac', 'm4a' ]

pattern = ''

for n in extensions:
  if len(pattern) > 0: pattern += '|'
  pattern = pattern + n  + '|' + n.upper() 

expr = re.compile (".*\.(" + pattern  + ")$")

files = os.listdir('.')  

for n in files:
  if expr.match (n): 
    q.put(n)
    print (n)
for i in range (cores):
  process = multiprocessing.Process(target=encodeAudio, args=())
  process.start()

