#!/bin/sh

#takes in port number as argument from command line to run the server code
args=("$@")
python3 server.py ${args[0]}
