from algorithm_benchmark import benchmark
from datetime import datetime
import os

algorithms = ['-md5', '-sha1', '-sha256', '-sha512']
filesizes = ['0B', '800KB', '1MB', '100MB']
directory = f"bench_results_{datetime.now().isoformat(timespec='minutes').replace('T','_')}"
os.system(f"mkdir {directory}")
for a in algorithms:
    for f in filesizes:
        benchmark(['-s', '-a', a, '-f', f, '-c', '10', '-o', f"{directory}/{a[1:]+'_'+f}.csv"])
