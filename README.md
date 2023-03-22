# DRO Project

This project allows the user to take an off the shelf [shahe DRO](https://www.amazon.com/Digital-Readout-0-150mm-Accurate-Machines/dp/B089ZSG84J/ref=sr_1_3?crid=NZHM6E6DVIOC&keywords=shahe+dro&qid=1679508608&sprefix=shahe+dro%2Caps%2C100&sr=8-3) and get the mm position of the DRO back on an arduino. 


The arduino sketch can be found in the dro_sketch folder. The main file is intended to be run on a computer listening to the arduino over a usb -> serial connection. 

parse_logs.py is specific to the use case I was using, but could be adapted to other uses.
