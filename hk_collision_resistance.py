from generate_hk import generate_hk
from datetime import datetime
from random import randint, choice
import os
from sys  import getsizeof
import string

key = 'abc'
filename = f"tmp_file_{datetime.now().isoformat(timespec='minutes').replace('T','_')}.txt"
collisionfile =  f"tmp_collision_file_{datetime.now().isoformat(timespec='minutes').replace('T','_')}"
filecontent = 'kot'
os.system(f"echo '{filecontent}' > {filename}")
data = generate_hk(['-s','-a', '-md5', '-k', key, '-i', f'{filename}'])

letters =string.ascii_letters

def randomString(stringLength=3):
    return ''.join(choice(letters) for i in range(stringLength))

i=0
while True:
    i += 1
    s = randomString()
    os.system(f"echo '{s}' >{collisionfile}")

    collision = generate_hk(['-s','-a', '-md5', '-k', key, '-i', f'{collisionfile}'])
    if   collision[2][0:3] == data[2][0:3]:
        print('Attempts counter:',i)
        print('Collision str:',s,'\tOriginal str:',filecontent)
        print('Common bits:', '(coll_hk)',collision[2][0:3],collision[2][3:],'\t(orig_hk)',data[2][0:3],data[2][3:])
        break

os.system(f"rm -f {filename}")
os.system(f"rm -f {collisionfile}")
