@echo off
SET USERNAME=SECRET
SET PASSWORD=SECRET
@echo on

cat asciiArt.txt

@echo off
pipenv run python main.py
