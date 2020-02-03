import os
import shutil
import glob
source = os.getcwd()+"/DMN-subtree/Authorising-Rules/Designing-a-decision-service-using-DMN-models/Decision-Model-and-Notation-DMN"
dest = os.getcwd()+"/DMN"
shutil.rmtree(dest)
try:
    os.mkdir(dest)
except OSError:
    print("Creation of the directory %s failed" % dest)
else:
    print("Successfully created the directory %s " % dest)

files = [f for f in glob.glob(source+"/*.asciidoc", recursive=True)]

for f in files:
    with open(f, "r") as g:
        stri = g.read()
        for i, part in enumerate(stri.split("[id")):
            if not part.strip():
                continue  # make sure its not empty
            with open("file%d.asciidoc" % i, "w") as f:  # open a file to write to
                f.write("[id"+part)
    for file in os.listdir(os.getcwd()):
        if file.endswith(".asciidoc"):
            shutil.move(file, dest)
    with os.scandir(dest) as entries:
        for entry in entries:
            if entry.is_file():
                with open(entry, "r") as fi:
                    fline = fi.readline()
                    m=fline[fline.find("[id='")+5:fline.find("_{context}']")]
                    os.rename(entry,m+".asciidoc")
for file in os.listdir(os.getcwd()):
        if file.endswith(".asciidoc"):
            shutil.move(file, dest)
for file in glob.glob("DMN/*'].asciidoc"):
    os.rename(file,file.replace("']",""))
