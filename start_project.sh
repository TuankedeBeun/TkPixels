#!/bin/bash

# set safe environment
export PATH=/usr/bin:/bin:/usr/local/bin

# navogate to project root
cd /home/tuanke/Programming/TkPixels || exit

# create logging directory and empty the run log file
mkdir -p logs
> logs/run.log

# pull latest changes from GitHub
echo "== Git Pull ==" >> logs/run.log
git config --global --add safe.directory /home/tuanke/Programming/TkPixels
git pull >> logs/run.log 2>&1

# start the led show
echo "== Start show ==" >> logs/run.log
python3 -u led_show.py >> logs/run.log 2>&1 &

# start I/O
echo "== Start I/O ==" >> logs/run.log
source /home/tuanke/myenv/bin/activate
python3 -u start_input.py >> logs/run.log 2>&1 &