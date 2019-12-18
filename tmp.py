from tools.generate_file import generate_file
from tools.generate_rsa import generate_rsa 
from benchmarks.signing_file_with_rsa_benchmark import sign_file_with_rsa
from datetime import datetime
import os

algorithms = ['', 'aes128', 'des3']
filesizes = ['16', '100KB', '5MB']
keysizes = ['1024', '2048', '4096']
directory = f"bench_results_{datetime.now().isoformat(timespec='minutes').replace('T','_')}/"
os.system(f"mkdir {directory}")

for a in algorithms:
    for f in filesizes:
        for k in keysizes:
            generate_rsa(['-s', '-a', a, '-p', 'dupa', '-S', k, '-o', 'key.rsa', '-d', {directory}])
            generate_file(['-s', '-f', f, '-n', 'test.txt', '-d', {directory}])
            filename= f"alg-{a}_fsize-{f}ksize-{k}.csv"
            os.system(f"echo 'id;time [s];\n'  >> {directory+filename}")
            total_time = 0
            for i in range(100):
                time = sign_file_with_rsa(['-k', 'key.rsa', '-p', 'dupa', '-i', 'test.txt'])
                total_time += time
                os.system(f"echo '{i};{time};\n'  >> {directory+filename}")
            print(filename, "avg_time:\t",total_time/100)

    
            
           
