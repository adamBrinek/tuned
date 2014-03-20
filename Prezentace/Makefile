#	Prvni pokus o makefile pro LaTex
#	Nejspis potrebuje jeste dost upravit ale zatim zvlada to co se po nem chce

NAME = Draft
BROWSER = evince 

pdf:
	pdflatex $(NAME)
run:
	make pdf && make clean && $(BROWSER) $(NAME).pdf

clean:
	rm $(NAME).log $(NAME).aux

tarball: 
	tar $(NAME).tar.gz
