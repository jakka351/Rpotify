#!/bin/bash
sudo apt-get install -y xdotool wget git 
wget -O rpotify.zip https://github.com/Madh93/Rpotify/archive/master.zip
unzip rpotify.zip && cd Rpotify-master
ln -s ./rpotify.sh /usr/local/bin/rpotify
echo "enter your client id:"
echo "enter your client secret:"
./rpotify.sh help
