import sys, getopt
import subprocess
import os

def verify_file_with_rsa(argv):
    silent = False
    key = None
    password = None
    hashedfile = None
    originalfile = None
    opts = None
    try:
        opts, args = getopt.getopt(argv,"hsk:p:f:g:",["key=","pass=","hashed-file=", "original-file="])
    except getopt.GetoptError:
        print('verify_file_with_rsa.py -s <silent> -k <key> -p <pass> -f <hashed-file> -g <original-file>')
        sys.exit(1)
    else:
        for opt, arg in opts:
            if opt in ("-h","--help"):
                print('verify_file_with_rsa.py -s <silent> -k <key> -p <pass> -f <hashed-file> -g <original-file>')
                sys.exit()
            elif opt in ("-s", "--silent"):
                silent = True
            elif opt in ("-k","--key"):
                key = arg
            elif opt in ("-p","--pass"):
                password = arg
            elif opt in ("-f","--hashed-file"):
                hashedfile = arg
            elif opt in ("-g","--original-file"):
                originalfile = arg
        if  key == None or password == None or hashedfile == None or originalfile == None:
            print("Provide sufficient arguments!")
            print('verify_file_with_rsa.py -s <silent> -a <algorithm> -k <key> -p <pass> -f <hashed-file> -g <original-file>')
            sys.exit(1)
        else:
            total_time=0.0
            times = subprocess.Popen(["time", "openssl", "dgst", "-prverify", f"{key}", "-passin", f"pass:{password}", "-signature", f"{hashedfile}",f"{originalfile}"],stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
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
    verify_file_with_rsa(sys.argv[1:])