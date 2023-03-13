import os
import sys
import subprocess
# Keep UTF-8 environment
environ = os.environ.copy()
environ['PYTHONIOENCODING'] = 'utf-8'

directory = sys.argv[1]
extension = sys.argv[2]

def write_log(fpath, mode = 'w'):
    with open("result.txt", mode) as f:
        if fpath != "":
            f.write(fpath + "\n")
        pass

def filter_accept(root, file):
    input_file = os.path.join(root, file)
    write_log(input_file, "a")
    

write_log("")
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith("." + extension):
            filter_accept(root, file)