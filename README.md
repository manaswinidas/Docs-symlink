# Docs-symlink

This repository explores the use of symbolic links for achieving single-sourced documentation for Kogito.

## Run 

In order to run the product docs, you need to install [ccutil](https://pantheon.cee.redhat.com/#/help/ccutil-install) and follow the instructions in [proposal-d](https://gitlab.cee.redhat.com/red-hat-jboss-bxms-documentation/proposal-d/tree/master).

In order to run the community docs, you need to have Maven installed. If yes, goto `doc-content/drools-docs`, run `mvn clean install` and view the `index.html` in `target/generated-docs/html_single`.

In order to run the PROD docs in gitbook, run the Python script named `split.py` to split and rename the documentation blocks and rewrite the assembly. Go to `assemblies/assembly_dmn-models/dm` and run `ba-build` to see the documentation at `index.html` inside `assemblies/assembly_dmn-models/dm/build/tmp/en-US/html-single`. In order to see the gitbook version, go to the `assemblies/assembly_dmn-models/dm/build/tmp/en-US/html-single` folder and run `gitbook serve`. You can see the documentation at `localhost:4000`. It may ask you to run `gitbook install`. You also may need to install gitbook CLI, if you don't have it already. Just run `npm install gitbook-cli -g` and run the commands again.

In order to fetch from all subtrees in the root repository, run `git subtree pull-all`. 
In order to push all changes in subtrees to the original projects from the root repository, run `git subtree push-all`.

## Steps to reproduce

If you go to the `.gitignore` file, you can see a path to DMN folder, which is the transient output folder. The DMN-source folder is similar to structure at [https://github.com/manaswinidas/DMN/wiki](https://github.com/manaswinidas/DMN/wiki). It has been added as a peer folder in the root itself, which is symlinked to the DMN folder in `maven/doc-content/drools-docs/src/main/asciidoc`. The command to add a symbolic link is as follows:

`ln -s /path/to/test_docs/DMN-source/ /path/to/asciidoc/DMN` inside the required folder.

For adding gitbook, just go to the folder where you want your gitbook to be built. Run `gitbook init` followed by `gitbook serve` and see the gitbook documentation running on `localhost:4000`. Since, I have included a plugin called `include-html`, after running `gitbook serve`, you may get a prompt to run `gitbook install`. Run the same followed by `gitbook serve` to get the documentation running on the browser.
