from generate_hk import generate_hk
from datetime import datetime
import os

algorithms = ['-md5', '-sha1', '-sha256']
keys = ['abcdef', 'okmnjiuhb', 'qazokmwsxijnedcijnrfvuhb']
directory = f"hk_results_{datetime.now().isoformat(timespec='minutes').replace('T','_')}"
os.system(f"mkdir {directory}")
os.system(f"echo 'Kocham przyrodę, uwielbiam drzewa, ptaszki. Gołębie są najlepsze, zwłaszcza jak srają.' > {directory}/test_input_file.txt")
os.system(f"echo 'algorithm;key;hashed_key' > {directory}/results.csv")
tmp = ""
for a in algorithms:
    for k in keys:
        data = generate_hk(['-s','-a', a, '-k', k, '-i', f'{directory}/test_input_file.txt'])
        tmp += f"{data[0]};{data[1]};{data[2]};\n"

os.system(f"echo '{tmp}' >> {directory}/results.csv")