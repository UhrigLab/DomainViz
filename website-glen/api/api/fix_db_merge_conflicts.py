import glob, os
#This simple script just removes any files with <<<<<<< HEAD in them, be careful when calling it
#Since you may kill good dbs, this is only for emergency use, when files get corrupted by git conflicts and there 
#Is no easy way to fix them all.
for f in glob.glob("dbs/*"):
    file = open(f)
    if "<<<<<<< HEAD" in file.read():
        os.remove(f)
        print("removed" + f)