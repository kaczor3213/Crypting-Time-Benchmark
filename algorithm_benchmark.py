import sys, getopt
import subprocess
import os
import re 

def benchmark(argv):
    algorithm = None
    silent = False
    filesize = None
    count = None
    outputfile = None
    opts = None
    try:
        opts, args = getopt.getopt(argv,"hsa:f:c:o:",["algorithm=","file-size=","count=", "output-file="])
    except getopt.GetoptError:
        print('alghorithm_benchmark.py -s <silent> -a <algorithm> -f <filesize> -c <count> -o <outputfile>')
        sys.exit(2)
    else:
        
        for opt, arg in opts:
            if opt in ("-h","--help"):
                print('alghorithm_benchmark.py -s <silent> -a <algorithm> -f <filesize> -c <count> -o <outputfile>')
                sys.exit()
            elif opt in ("-s", "--silent"):
                silent = True
            elif opt in ("-a", "--algorithm"):
                if arg[0]!='-':
                    algorithm = '-'+arg
                else:
                    algorithm = arg
            elif opt in ("-f","--file-size"):
                filesize = arg
            elif opt in ("-c","--count"):
                count = arg
            elif opt in ("-o","--outputfile"):
                outputfile = arg

        if algorithm == None or filesize == None or count == None:
            print("Provide sufficient arguments!")
            print('alghorithm_benchmark.py -s <silent> -a <algorithm> -f <filesize> -c <count> -o <outputfile>')
            sys.exit(2)
        else:
            if  re.search(r"^0+[A-z]*$", filesize):
                os.system(f"touch {algorithm[1:]+'_'+filesize}.txt")
            else:
                if  not silent:
                    subprocess.call(["dd", "if=/dev/urandom",f"of={algorithm[1:]+'_'+filesize}.txt",f"bs={filesize}","count=1"])
                else:
                    subprocess.call(["dd","status=none", "if=/dev/urandom",f"of={algorithm[1:]+'_'+filesize}.txt",f"bs={filesize}","count=1"])
            average=0
            
            if outputfile != None:
                os.system(f"echo '{algorithm[1:]};id;time_[ms]'  > {outputfile}")
            if not silent:
                print(f"File size: {filesize}")
                print(f"Count of tests: {count}")

            for i in range(int(count)):
                times = subprocess.Popen([f"time", "openssl", "dgst" ,f"{algorithm}", f"{algorithm[1:]+'_'+filesize}.txt"],stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
                user_time = times[0].decode('utf-8').split()[2].replace('user','')
                sys_time = times[0].decode('utf-8').split()[3].replace('system','')
                total_time = float(user_time) +float(sys_time)
                average += total_time

                if outputfile != None:
                    os.system(f"echo ';{i};{str(total_time)};'  >> {outputfile}")
                if not silent:
                    print(f"Times: u: {user_time}, \t s: {sys_time}, \t t: {total_time}")    
            
            os.system(f"rm -f {algorithm[1:]+'_'+filesize}.txt")

            if not silent:
                print()
                print(f"Average time {average/float(count)}")

if __name__ == '__main__':
    print(sys.argv[1:])
    benchmark(sys.argv[1:])