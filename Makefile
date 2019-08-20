SRC=*.tex
NAME=Resume
EXTTEX=$(NAME)_Commands.tex
HEAD=$(NAME)_Overhead.tex
PyGen=Gentex.py
Pic=Headshot.png
Info=Info.json
Class=yaac-another-awesome-cv.cls
PDFCycle=../_archive/
Website=./_website/_data
tool=lualatex

MAKEFLAGS += --silent

default::compile

install:
	@echo Checking for sudo access
	@sudo -v

	@echo Installing the packages
	@sudo apt install texlive-full texlive-luatex python3 python3-pip python3-yaml -y

	@echo Making the directories
	@mkdir -p $(PDFCycle)
	@mkdir -p $(Website)

uninstall:
	@echo Checking for sudo access
	@sudo -v

	@echo Uninstalling the packages
	@sudo apt remove texlive-full texlive-luatex python3-yaml python3-pip python3 -y

	@echo Deleting the directories
	@rm -r $(PDFCycle)
	@rm -r $(Website)

rough: $(HEAD)
	@echo Rough
	@$(tool) $(NAME).tex

build: $(HEAD)
	@echo Build
	@$(tool) $(NAME).tex >> Resume_build.log

gen: $(PyGen)
	@echo Gen
	@./$(PyGen) $(Info) $(HEAD) $(NAME).tex

stage:
	@echo Stage
	@mkdir ../Stage
	@cp $(Info) ../Stage
	@cp $(Class) ../Stage
	@cp $(NAME).tex ../Stage
	@cp $(HEAD) ../Stage
	@cp $(EXTTEX) ../Stage
	@cp $(NAME).pdf ../Stage
	@cp Makefile ../Stage
	@cp -r fonts/ ../Stage
	@cp $(PyGen) ../Stage
	@mv ../Stage ../0.$(shell find ../ -maxdepth 1 -type d -name '0.*'|wc -l)
	@make clean

cycle:
	@echo Cycle
	@make clean
	@make

website: $(PyGen)
	@echo Website
	@./$(PyGen) $(Info) $(Website)

cut:
	@echo Cut
	@make clean
	@make website
	@make compile
	@make stage
	@sed -i -- 's/V0.$(shell find ../ -maxdepth 1 -type d -name '0.*'|wc -l)/V0.$(shell find ../ -maxdepth 1 -type d -name '0.*'|wc -l| awk '{print 1 + $$1}')/g' $(Info)
	@cp ../0.$(shell find ../ -maxdepth 1 -type d -name '0.*'|wc -l| awk '{print $$1}')/Resume.pdf $(PDFCycle)
	@make clean

test:
	@echo Test
	@make gen
	@make rough
	@make rough
	@make softclean

compile:
	@echo Compile
	@make gen
	@make build
	@make build
	@make softclean

softclean:
	@echo SoftClean
	@find . -maxdepth 1 \( ! -name 'Makefile' ! -name 'fonts' ! -name '$(Pic)' ! -name '$(PyGen)' ! -name '$(Info)'  ! -name '$(HEAD)' ! -name '$(Class)'  ! -name '$(EXTTEX)' ! -name '$(NAME).pdf' ! -name '$(NAME).tex' ! -name 'README.md' ! -name '.gitattributes' ! -name '.gitignore' ! -name 'LICENSE' \) -type f -exec rm {} +

clean:
	@echo Clean
	@make softclean
	@find . -maxdepth 1 -name $(NAME).pdf -type f -exec rm {} +
	@find . -maxdepth 1 -name $(NAME).tex -type f -exec rm {} +
