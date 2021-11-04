#!/bin/sh

#takes in host name and port number as arguments from command line to run the client code
args=("$@")
python3 client.py ${args[0]} ${args[1]}
