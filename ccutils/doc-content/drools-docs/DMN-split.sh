#!/bin/bash
sudo chmod -R 777 ../asciidoc
rm -rf DMN
mkdir DMN
for files in DMN-subtree/Authorising-Rules/Designing-a-decision-service-using-DMN-models/Decision-Model-and-Notation-DMN/*.asciidoc
do
    csplit --quiet --prefix=DMN/ $files "/\[id/" "{*}"
    find DMN/ -size 0 -delete
    cd DMN
    for file in *
    do
        # sed -n "s/^.*'\(.*\)_{context}'.$/\1/ p" $file <<< ${bigname}
        bigname=$(sed -n "s/^.*'\(.*\)_{context}'.$/\1/ p" $file)
        sudo mv -v "$file" "$bigname.asciidoc"
        # "s/^.*'\(.*\)'.*$/\1/ p"
    done
    cd ..
    sudo chmod -R 777 DMN
done
csplit --quiet --prefix=DMN/ DMN-subtree/Authorising-Rules/Designing-a-decision-service-using-DMN-models/Decision-Model-and-Notation-DMN/DMN-model-execution.asciidoc "/\[id/" "{*}"
find DMN/ -size 0 -delete
sudo chmod -R 777 DMN
cd DMN
for file in {01..04}
do 
    # sed -n "s/^.*'\(.*\)'.$/\1/ p" $file <<< ${name} 
    name=$(sed -n "s/^.*'\(.*\)'.$/\1/ p" $file)
    sudo mv -v "$file" "$name.asciidoc"
done