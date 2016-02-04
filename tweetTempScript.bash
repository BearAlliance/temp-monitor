#!/bin/bash  

echo Updating Repo
git pull

echo Taking Temperature reading and tweeting
python ~/dev/temp-monitor/tweetTemp.py

echo Finished!
