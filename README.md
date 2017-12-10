MCS(MIFARE Classic Shield)
============================
> This script runs only in raspberry pi

> mcs.py is a small class to interface with the NFC reader Module MFRC522 on the Raspberry Pi.

> This code requires you to have MFRC522 installed from the following repository:
https://github.com/mxgxw/MFRC522-python


## What is this script for?

> This script is written for the first two bytes of block number 9 are based on a card in which the amount information is stored in 
> little endian format.
> MIFARE Classic is a card with a fatal vulnerability, but it can be applied to a certain level of security by running the above script.
> The operation procedure is as follows.
> 1. Balance encoding
> 2. 5 left or right bit shift
> 3. Calculate CRC32
> 4. MD5 Hash using UID, balnaceBLK

## Examples

> This repository includes a couple of examples showing how to protect MIFARE Classic(bit shift,XOR,CRC32,MD5)

## Usage

> Import the class by importing mcs.py top of your script.
> For more info see the examples.


## Pins

| name | pin   | usage      |
|------|-------|------------|
| SDA  | 24    | GPIO8      |
| SCK  | 23    | GPIO11     |
| MOSI | 19    | GPIO10     |
| MISO | 21    | GPIO9      |
| GND  | Any   | Any GND    |
| RST  | 22    | GPIO25     |
| 3.3V | 1     | 3V3        |

