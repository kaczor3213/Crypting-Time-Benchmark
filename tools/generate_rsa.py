import sys, getopt
import subprocess
import os

def generate_rsa(argv):
    algorithm = None
    silent = False
    password = None
    outputfile = None
    directory = None
    size = None
    opts = None
    try:
        opts, args = getopt.getopt(argv,"hsa:p:S:o:d:",["algorithm=","password=","key-size=","output-file=","directory="])
    except getopt.GetoptError:
        print('generate_rsa.py -s <silent> -a <algorithm> -p <password> -S <key-size> -o <output-file> -d <directory>')
        sys.exit(2)
    else:
        
        for opt, arg in opts:
            if opt in ("-h","--help"):
                print('generate_rsa.py -s <silent> -a <algorithm> -p <password> -S <key-size> -o <output-file> -d <directory>')
                sys.exit()
            elif opt in ("-s", "--silent"):
                silent = True
            elif opt in ("-a", "--algorithm"):
                if arg == None:
                    continue
                else:
                    if arg[0]!='-':
                        algorithm = '-'+arg
                    else:
                        algorithm = arg
            elif opt in ("-p", "--password"):
                password = arg
            elif opt in ("-S","--key-size"):
                size = arg
            elif opt in ("-o","--output-file"):
                outputfile = arg
            elif opt in ("-d", "--directory"):
                directory = arg
                if directory[-1] != '/':
                    directory = directory + '/'

        
        if directory == None:
            directory = './'

        if password == None or size == None:
            print("Provide sufficient arguments!")
            print('generate_rsa.py -s <silent> -a <algorithm> -p <password> -S <key-size> -o <output-file> -d <directory>')
            sys.exit(2)
        else:
            rsa_key = None

            if algorithm == None:
                if outputfile == None:
                    rsa_key = '-----BEGIN RSA PRIVATE KEY-----'+subprocess.Popen([f"openssl", "genrsa" ,"-passout", f"pass:{password}", f"{size}"],stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].decode('utf-8').split('-----BEGIN RSA PRIVATE KEY-----')[1]
                else:
                    subprocess.Popen([f"openssl", "genrsa", "-out", f"{directory+outputfile}", "-passout", f"pass:{password}", f"{size}"],stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].decode('utf-8').split('-----BEGIN RSA PRIVATE KEY-----')[0]
            else:
                if algorithm == None:
                    rsa_key = '-----BEGIN RSA PRIVATE KEY-----'+subprocess.Popen([f"openssl", "genrsa" ,f"{algorithm}","-passout", f"pass:{password}", f"{size}"],stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].decode('utf-8').split('-----BEGIN RSA PRIVATE KEY-----')[1]
                else:
                    rsa_key = '-----BEGIN RSA PRIVATE KEY-----'+subprocess.Popen([f"openssl", "genrsa", "-out", f"{directory+outputfile}", "-passout", f"pass:{password}",f"{algorithm}", f"{size}"],stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].decode('utf-8').split('-----BEGIN RSA PRIVATE KEY-----')[0]

            if not silent:
                if outputfile != None:
                    print("RSA key:")
                    os.system(f'cat {outputfile}')
                else:
                   print(f"RSA key:\n{rsa_key}")

if __name__ == '__main__':
    print(sys.argv[1:])
    generate_rsa(sys.argv[1:])