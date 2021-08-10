#!/bin/bash

# Make environment values available to crontab
printenv | grep -v "no_proxy" >> /etc/environment 

# Run cron
cron && tail -f /var/log/cron.log
