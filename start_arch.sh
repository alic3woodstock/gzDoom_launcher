#!/bin/bash
if pacman -Qi python-kivy python-babel python-py7zr python-screeninfo fuse xsel > /dev/null; then
	echo "Starting..."
elif [ -e /usr/bin/paru ]; then
	paru -S python-kivy python-babel python-py7zr python-screeninfo fuse xsel --needed
elif [ -e /usr/bin/yay ]; then
	yay -S python-kivy python-babel python-py7zr python-screeninfo fuse xsel --needed
else
	sudo pacman -S python-kivy python-babel python-py7zr python-screeninfo fuse xsel --needed
fi
python main.py
