import sys, getopt
import subprocess
import os

def sign_file_with_rsa(argv):
    silent = False
    inputfile = None
    outputfile = None
    rsa = None
    password = None
    opts = None
    try:
        opts, args = getopt.getopt(argv,"hsk:p:i:o:",["rsa=","pass=","input-file=","output-file="])
    except getopt.GetoptError:
        print('sign_file_with_rsa.py -s <silent> -k <rsa> -p <pass> -i <input-file> -o <output-file>')
        sys.exit(2)
    else:
        
        for opt, arg in opts:
            if opt in ("-h","--help"):
                print('sign_file_with_rsa.py -s <silent> -k <rsa> -p <pass> -i <input-file> -o <output-file>')
                sys.exit()
            elif opt in ("-s", "--silent"):
                silent = True
            elif opt in ("-k","--rsa"):
                rsa = arg
            elif opt in ("-p","--pass"):
                password = arg
            elif opt in ("-i","--input-file"):
                inputfile = arg
            elif opt in ("-o","--output-file"):
                outputfile = arg

        if  rsa == None or password == None or inputfile == None:
            print("Provide sufficient arguments!")
            print('sign_file_with_rsa.py -s <silent> -k <rsa> -p <pass> -i <input-file> -o <output-file>')
            sys.exit(2)
        else:
            total_time=0.0
            times = None
            user_time = None
            sys_time = None
            if outputfile == None:
                times = subprocess.Popen(["time", "openssl", "dgst","-hex","-sign", f"{rsa}", "-passin", f"pass:{password}",f"{inputfile}"],stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
                print(times[0].decode('utf-8','ignore').split()[1])
                user_time = times[0].decode('utf-8','ignore').split()[1].replace('user','')
                sys_time = times[0].decode('utf-8','ignore').split()[2].replace('system','')
            else:
                times = subprocess.Popen(["time", "openssl", "dgst","-sign", f"{rsa}", "-out", f"{outputfile}", "-passin", f"pass:{password}",f"{inputfile}"],stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
                user_time = times[0].decode('utf-8','ignore').split()[0].replace('user','')
                sys_time = times[0].decode('utf-8','ignore').split()[1].replace('system','')

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