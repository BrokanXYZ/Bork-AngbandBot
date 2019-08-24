@echo off
SET USERNAME=SECRET
SET PASSWORD=SECRET
@echo on

type asciiArt.txt

@echo off
pipenv run python main.py
