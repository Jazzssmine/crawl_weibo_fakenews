#!/bin/bash

*/10 * * * * python3 /home/share/spider/main.py > "/home/share/spider/$(date +"%Y-%m-%d").log" 2>&1