#!/bin/bash
if [ -e /usr/bin/paru ]; then
	paru -Sy python-kivy python-babel python-py7zr python-screeninfo fuse --needed
elif [ -e /usr/bin/yay ]; then
	yay -Sy python-kivy python-babel python-py7zr python-screeninfo fuse --needed
else
	sudo pacman -Sy python-kivy python-babel python-py7zr python-screeninfo fuse --needed
fi

python main.py
