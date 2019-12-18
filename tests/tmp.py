import sys
sys.path.append("..")
from tools.generate_file import generate_file
from tools.generate_rsa import generate_rsa 
from benchmarks.signing_file_with_rsa_benchmark import sign_file_with_rsa
from benchmarks.verifying_signed_file_benchmark import verify_file_with_rsa
from datetime import datetime
import os

algorithms = ['', 'aes128', 'des3']
filesizes = ['16', '100KB', '5MB']
keysizes = ['1024', '2048', '4096']
directory = f"bench_results_{datetime.now().isoformat(timespec='minutes').replace('T','_')}/"
os.system(f"mkdir {directory}")

for a in algorithms:
    if a == '':
        print(f"<=====================================DEFAULT_RSA======================================>\n")
    else:
        print(f"<======================================={a.upper()}=======================================>\n")

    for f in filesizes:
        for k in keysizes:
            if a=='':
                generate_rsa(['-s', '-p', 'dupa', '-S', k, '-o', 'key.rsa', '-d', directory])
            else:
                generate_rsa(['-s', '-a', a, '-p', 'dupa', '-S', k, '-o', 'key.rsa', '-d', directory])
            generate_file(['-s', '-f', f, '-n', 'test.txt', '-d', directory])
            filename= f"alg-{a}_fsize-{f}_ksize-{k}.csv"
            os.system(f"echo 'id;sign_time[s];verify_time[s]\n'  >> {directory+filename}")
            sign_total_time = 0
            verify_total_time = 0
            for i in range(100):
                sign_time = sign_file_with_rsa(['-s', '-k', directory+'key.rsa', '-p', 'dupa', '-i', directory+'test.txt','-o',directory+'hash.txt',])
                verify_time = verify_file_with_rsa(['-s','-k', directory+'key.rsa', '-p', 'dupa', '-f', directory+'hash.txt', '-g', directory+'test.txt'])
                os.system(f"echo '{i};{sign_time[1]};{verify_time[1]};\n'  >> {directory+filename}")
                sign_total_time += sign_time[1]
                verify_total_time += verify_time[1]
                
            print(filename, "avg_sign_time:\t\t",sign_total_time/100)
            print(filename, "avg_veri_time:\t\t",verify_total_time/100)
            print()

