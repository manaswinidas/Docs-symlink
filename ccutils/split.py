import os, fnmatch
import shutil
import glob
import itertools
import logging
from configparser import ConfigParser
import re

def get_file_with_parents(filepath, levels):
    """function to get file with parents and return parents along with file upto level 2"""
    common = filepath
    for i in range(levels + 2):
        common = os.path.dirname(common)
    return os.path.relpath(filepath, common)

def find(name, path):
    """find the full file path starting from root"""
    for root, dirs, files in os.walk(path):
        for file in files:
            if name.strip() == file.strip():
                return os.path.join(root, name)
    return logging.error("Doesn't exist")

def get_file_name(part):
    """get file name using regex from fragment ID"""
    return re.findall(r"'(.*\-[a-z]+).*", part)[0]

def get_replaceid(fragment):
    """get replace id for shared content"""
    replaceid=re.findall(r":[A-z]+:\s(.+)", fragment)[0]
    return replaceid

all_files=[]
def split(meta_attribute, files, dest, search_dir):
    """split the subtree files into fragments"""
    for file in files:
        with open(file, "r") as fragment_content:
            content = fragment_content.read()
            for fragment in content.split("[id=")[1:]:
                if not fragment.strip():
                    continue  # make sure fragment not empty
                if meta_attribute not in fragment:
                    file_name = dest+"/"+str(get_file_name(fragment))+".asciidoc"
                else:
                    replaceid=get_replaceid(fragment)
                    file_name=str(find(replaceid, search_dir))
                all_files.append(file_name)
                if meta_attribute not in fragment:
                    with open(file_name, "w") as f:
                        f.write("[id="+fragment)

def assembly_list(file, output_lines, assembly_line, leveloffset, level):
    """function to generate assembly lines per file"""
    output_lines.append(
        str(assembly_line)+get_file_with_parents(file, 1)+str(leveloffset)+str(level)+"]\n")

def assembly_generate(assembly_file, search_dir, assembly_line, leveloffset, meta_attribute):
    """function to generate assembly"""
    output_lines = []
    with open(assembly_file) as fp:
        linesbegin = list(itertools.takewhile(lambda x: '// Modules -' not in x,
                                              itertools.dropwhile(lambda x: "[id='assembly_dmn-models']" not in x, fp)))
    with open(assembly_file) as fp:
        lines = list(itertools.takewhile(lambda x: '== Additional resources' not in x,
                                         itertools.dropwhile(lambda x: '// Modules -' not in x, fp)))
    with open(assembly_file) as fp:
        linesend = list(itertools.takewhile(lambda x: '// End of main.adoc' not in x,
                                            itertools.dropwhile(lambda x: '== Additional resources' not in x, fp)))

    for file in all_files:
        with open(file, "r") as file_content:
            level=re.findall(r":[A-z]+:\s(.+)", file_content.read())[0]
        assembly_list(file, output_lines, assembly_line, leveloffset, level)

    f = open(assembly_file, "w")
    final = linesbegin+output_lines+linesend
    f.write("\n".join(final))
    f.close()

def prepare_images_for_ccutils(split_source, images_dest):
    """copy all images from community directory to product directory and change paths accordingly"""
    for imgfile in glob.glob(split_source+"**/*.png", recursive=True):
        shutil.copy(imgfile, images_dest)
    
def findReplace(split_source, images_find, images_replace, filePattern):
    for path, dirs, files in os.walk(os.path.abspath(split_source)):
        for filename in fnmatch.filter(files, filePattern):
            filepath = os.path.join(path, filename)
            with open(filepath) as f:
                s = f.read()
            s = s.replace(images_find, images_replace)
            with open(filepath, "w") as f:
                f.write(s)

def main():
    config=ConfigParser()
    config.read(".config")
    # config.readfp(open(r'.config'))
    split_source = os.getcwd()+config.get('Split-config', 'split_source')
    split_dest = os.getcwd()+config.get('Split-config', 'split_dest')
    assembly_file = os.getcwd()+config.get('Split-config', 'assembly_file')
    search_dir = os.getcwd()+config.get('Split-config', 'search_dir')
    assembly_line=config.get('Split-config', 'assembly_line')
    leveloffset=config.get('Split-config', 'leveloffset')
    meta_attribute=config.get('Split-config', 'meta_attribute')
    images_dest=os.getcwd()+config.get('Split-config', 'images_dest')
    images_find=config.get('Split-config','images_find')
    images_replace=config.get('Split-config','images_replace')
    try:
        if(os.path.exists(split_dest)):
            shutil.rmtree(split_dest)
        os.mkdir(split_dest)
    except OSError:
        logging.error('The directory already exists')
    files = [f for f in glob.glob(split_source+"/*.asciidoc", recursive=True)]
    split(meta_attribute, files, split_dest, search_dir)
    assembly_generate(assembly_file, search_dir, assembly_line, leveloffset, meta_attribute)
    prepare_images_for_ccutils(split_source, images_dest)
    findReplace(split_source, images_find, images_replace, ".asciidoc")
    
if __name__ == "__main__":
    main()
