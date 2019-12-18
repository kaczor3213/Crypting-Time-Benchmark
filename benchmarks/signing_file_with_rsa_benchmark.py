import sys, getopt
import subprocess
import os

def sign_file_with_rsa(argv):
    silent = False
    inputfile = None
    rsa = None
    password = None
    opts = None
    try:
        opts, args = getopt.getopt(argv,"hsa:k:p:i:",["algorithm=", "rsa=","pass=","input-file="])
    except getopt.GetoptError:
        print('sign_file_with_rsa.py -s <silent> -a <algorithm> -k <rsa> -p <pass> -i <inputfile>')
        sys.exit(2)
    else:
        
        for opt, arg in opts:
            if opt in ("-h","--help"):
                print('sign_file_with_rsa.py -s <silent> -a <algorithm> -k <rsa> -p <pass> -i <inputfile>')
                sys.exit()
            elif opt in ("-s", "--silent"):
                silent = True
            elif opt in ("-k","--rsa"):
                rsa = arg
            elif opt in ("-p","--pass"):
                password = arg
            elif opt in ("-i","--inputfile"):
                inputfile = arg

        if  rsa == None or password == None or inputfile == None:
            print("Provide sufficient arguments!")
            print('sign_file_with_rsa.py -s <silent> -a <algorithm> -k <rsa> -p <pass> -i <inputfile>')
            sys.exit(2)
        else:
            total_time=0.0
            times = subprocess.Popen(["time", "openssl", "dgst", "-hex","-sign", f"{rsa}", "-passin", f"pass:{password}",f"{inputfile}"],stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
            user_time = times[0].decode('utf-8','ignore').split()[2].replace('user','')
            sys_time = times[0].decode('utf-8','ignore').split()[3].replace('system','')
            try:
                total_time = float(user_time) +float(sys_time)
                if not silent:
                    print(f"Total time: {total_time}")
                return(0, total_time)
            except ValueError as e:
                return (1, e)

if __name__ == '__main__':
    print(sys.argv[1:])
    sign_file_with_rsa(sys.argv[1:])