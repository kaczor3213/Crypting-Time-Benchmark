import sys, getopt
import subprocess
import os
import re 

def generate_file(argv):
    silent = False
    filesize = None
    filename = None
    directory = None
    opts = None
    try:
        opts, args = getopt.getopt(argv,"hsf:n:d:",["file-size=","file-name=", "directory="])
    except getopt.GetoptError:
        print('generate_file.py -s <silent> -f <filesize> -n <filename> -d <directory:default("./")>')
        sys.exit(1)
    else:
        
        for opt, arg in opts:
            if opt in ("-h","--help"):
                print('generate_file.py -s <silent> -f <filesize> -n <filename> -d <directory:default("./")>')
                sys.exit()
            elif opt in ("-s", "--silent"):
                silent = True
            elif opt in ("-f","--file-size"):
                filesize = arg
            elif opt in ("-n","--file-name"):
                filename = arg
            elif opt in ("-d", "--directory"):
                directory = arg
                if directory[-1] != '/':
                    directory = directory + '/'
        
        if directory == None:
            directory = './'

        if filesize == None or filename == None:
            print("Provide sufficient arguments!")
            print('generate_file.py -s <silent> -f <filesize> -n <filename> -d <directory:default("./")>')
            sys.exit(1)
        else:
            if  re.search(r"^0+[A-z]*$", filesize):
                os.system(f"touch {filename}.txt")
            else:
                if  not silent:
                    subprocess.call(["dd", "if=/dev/urandom",f"of={directory+filename}",f"bs={filesize}","count=1"])
                else:
                    subprocess.call(["dd","status=none", "if=/dev/urandom",f"of={directory+filename}",f"bs={filesize}","count=1"])

if __name__ == '__main__':
    print(sys.argv[1:])
    generate_file(sys.argv[1:])