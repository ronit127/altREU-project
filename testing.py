import subprocess

for i in range(0, 100, 1):
    print(subprocess.getstatusoutput('python dataset.py'))