#!/usr/bin/env bash
tmux kill-server
# cd mlh-portfolio
git fetch && git reset origin/main --hard
source python3-virtualenv/bin/activate
pip install -r requirements.txt
tmux new-session -d -s flaskapp
tmux send-keys 'source python3-virtualenv/bin/activate && flask run --host=0.0.0.0' C-m
