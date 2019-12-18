import sys, getopt
import subprocess
import os

def generate_hk(argv):
    algorithm = None
    silent = False
    inputfile = None
    key = None
    hk = None
    opts = None
    try:
        opts, args = getopt.getopt(argv,"hsa:k:i:",["algorithm=","key=","input-file="])
    except getopt.GetoptError:
        print('generate_hk.py -s <silent> -a <algorithm> -k <key> -i <inputfile>')
        sys.exit(2)
    else:
        
        for opt, arg in opts:
            if opt in ("-h","--help"):
                print('generate_hk.py -s <silent> -a <algorithm> -k <key> -i <inputfile>')
                sys.exit()
            elif opt in ("-s", "--silent"):
                silent = True
            elif opt in ("-a", "--algorithm"):
                if arg[0]!='-':
                    algorithm = '-'+arg
                else:
                    algorithm = arg
            elif opt in ("-k","--key"):
                key = arg
            elif opt in ("-i","--inputfile"):
                inputfile = arg

        if algorithm == None or key == None or inputfile == None:
            print("Provide sufficient arguments!")
            print('generate_hk.py -s <silent> -a <algorithm> -k <key> -i <inputfile>')
            sys.exit(2)
        else:
            hk = subprocess.Popen([f"openssl", "dgst" ,f"{algorithm}","-hmac", f"{key}", f"{inputfile}"],stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].decode('utf-8').split('=')[1].strip()
            if not silent:
                print(f"Key: {key}")
                print(f"Hashed key: {hk}")
            return(algorithm, key, hk)

if __name__ == '__main__':
    generate_hk(sys.argv[1:])