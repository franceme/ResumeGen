# ResumeGen

---

## ACKNOWLEDGMENTS

This project uses the template created by [Christopher Roger (Darwiin)](https://github.com/darwiin/yaac-another-awesome-cv), or it can also be found on [overleaf](https://www.overleaf.com/latex/templates/awesome-source-cv/wrdjtkkytqcw).
His project uses the [Latex Project Public License v1.3c](https://opensource.org/licenses/LPPL-1.3c), this project does not maintain the license since this work has only uses his latex project and doesn't claim ownership of the project.

Slight changes have been made to the cls class, including duplicating social hyperlinks for enabling or disabling hyperlinks.

---

## TLDR

This project can do the following:

1. Generate a latex Resume.tex file by using Mako to inject data into the HEAD file.
2. Create a "cut" of the resume, upgrading the minor version in the Info file and creating a folder of everything in the environment.
3. Populate the yaml files for a website template, (sample located [here](https://github.com/franceme/franceme.github.io/)).

## About

---

### Why not use Microsoft Word?

I had previously used Microsoft Word for my resume, however I have had various issues converting documents to pdf.
With several other project reports I have also had various issues converting to pdf; such as certain images not being displayed and formatting not transferring over.

Since then I've learned how to use [latex](https://www.latex-project.org/), and since then latex seems to have a more stable pdf conversion.

### But why make a project out of it?

This was created for personal necessity, curiosity, and to learn more about templating information via Python3.
Since I use Linux OS's more often than Windows, I also needed to be able to use some documentation system that was multi-os.
In the future if I switch from [Darwiin's](https://github.com/darwiin/yaac-another-awesome-cv) to another template, I only need to change the template files.

### Should I use this repo compared to any other?

That choice is completely up to you, though this helps if you want to have a dynamic resume.
From some of the few repos I have seen, the template file can loop through each section of the resume.
Therefor ideally you should only have to edit the Info file.
If you also use a dynamic website (like a Jekyll one), you can use this to generate the data files to ensure both the website and resume are in sync.

---

## Makefile useages

Command | Explanation
---: | :---
install | Installs all of the nessecary packages.
uninstall | Uninstalls all of the packages used, **NOTE** this uninstalls Python3 and texlive-full.
cycle | This will clean the environment and re-generate the resume. 
website | This will generate the website yaml files in the specified output folder.
clean | Removes everything unnessecary from the environment.
cut | This will generate the website yaml files, update the version in Info.json, make a folder of the version, and clean the environment.

Important variables

variable | What does it do
---: | :---
EXTTEX | Any extra commands used in generating files.
HEAD | The latex template file
PyGen | The Python3 file that generates the yaml/latex file.
Info | The json file with the main source of information
Class | The class file used within the latex generation.
PDFCycle | The location for the resume cuts.
Website | The location for the yaml website files to be created in.
tool | The latex flavor used for processing the template, ([Darwiin's](https://github.com/darwiin/yaac-another-awesome-cv) template uses [lualatex](http://luatex.org/)).

---

## TODO

1. Add more comments
2. Create a temp directory for all of the processing files to be stored in.
3. Create a way to upgrade the major version.