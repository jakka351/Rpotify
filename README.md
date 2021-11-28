# Rpotify controlling Raspotify with Steering Wheel Controls via CANBus.

Rpotify is a tool for managing Spotify remotely without GUI, only by CLI.  

### Combining [`Raspotify`](https://github.com/dtcooper/raspotify) and [`can0swc`](https://github.com/jakka351/can0swc) and [`Rpotify`](https://github.com/Madh93/Rpotify) gives me wireless audio playing from my phone to my auxillary port, controlled by the steering wheel controls in my car.

## Features

**Current features:**

- Play/Pause/Stop
- Next/Previous
- Shuffle/Repeat
- Volume up/down
- Now Playing
- Information track
- Search song/album/artist

### Vehicle Set Up
This is setup for an MKI FG Falcon, edit the can data in the script to use with different vehicles, likely most mazdas and fords that have 11 bit ids and 8 bytes of message data will be fairly easy to do.

### Install

Download, extract and launch:
```
    wget -O rpotify.zip https://github.com/Madh93/Rpotify/archive/master.zip
    unzip rpotify.zip && cd Rpotify-master
    ./rpotify.sh
```
### How to use
To run steering wheel controls program:
     `python3 can0spoti.py`
     
To list all commands:

    `./rpotify.sh help`
