cd /Library/Frameworks/Python.framework/Versions/3.6/bin
sudo ./pyinstaller --onefile --noconsole /Users/kiwi/Desktop/maze/main.py
cd dist
sudo mv main /Users/kiwi/Desktop/maze/main
cd ..
