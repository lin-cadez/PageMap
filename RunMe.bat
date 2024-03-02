@echo off
echo Installing dependencies...
pip install pyvis beautifulsoup4 tldextract requests
echo Dependencies installed successfully.

echo Running main.py...
cls
python main.py
