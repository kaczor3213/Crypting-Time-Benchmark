from generate_hk import generate_hk
from datetime import datetime
from random import randint
import os
from sys  import getsizeof

algorithms = ['-md5', '-sha256']
key = 'okmnjiuhb'
filename = f"tmp_file_{datetime.now().isoformat(timespec='minutes').replace('T','_')}.txt";
filecontent = None

def corrupt_text(text):
    b_arr = bytearray(text, 'utf-8')
    index = randint(0,len(b_arr)-1)
    b = b_arr[index]
    b_arr[index]=b^0b00010000
    return  b_arr.decode('utf-8')

def overwrite_file(text, file):
    os.system(f"echo '{text}' > {file}")
    
def coherent_bits(hash_1='abxi', hash_2='zuhm'):
    b_arr_1 = bytearray(hash_1, 'utf-8')
    b_arr_2 = bytearray(hash_2, 'utf-8')
    counter = 0
    for i in range(len(b_arr_1)):
        tmp = b_arr_1[i] ^ b_arr_2[i]
        counter += 8-bin(tmp).count('1')
    return counter

for a in algorithms:
    filecontent = 'Kocham przyrodę, uwielbiam drzewa, ptaszki. Gołębie są najlepsze, zwłaszcza jak srają.'
  
    overwrite_file(filecontent, filename)
    data = generate_hk(['-s','-a', a, '-k', key, '-i', f'{filename}'])
    print(data[2])
    
    filecontent = corrupt_text(filecontent)
    overwrite_file(filecontent, filename)
    data_corrupted = generate_hk(['-s','-a', a, '-k', key, '-i', f'{filename}'])
    print(data_corrupted[2])
    
    print('Coherent bits:\t', coherent_bits(data[2], data_corrupted[2]), 'out of ', 8*len(bytearray(data_corrupted[2], 'utf-8')))
   
os.system(f"rm -f {filename}")
