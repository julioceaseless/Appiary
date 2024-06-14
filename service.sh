#!/usr/bin/env bash
sudo systemctl daemon-reload
# start
sudo systemctl start appiary_web
sudo systemctl start appiary_api

# enable
sudo systemctl enable appiary_web
sudo systemctl enable appiary_api

# check status
sudo systemctl status appiary_web
sudo systemctl status appiary_api
