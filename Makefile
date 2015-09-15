# makefile for eNB Startup Analyzer
.PHONY: all clean test app
all: clean test

clean:
	@echo cleaning...
	rm -rf www/upload/*
	rm -rf www/session

test:
	@echo building test...
	python test/test_app.py

app:
	@echo start app...
	python src/app.py 15920
