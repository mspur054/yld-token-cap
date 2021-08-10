# yld-token-cap

This is a project that sends token information from Coingecko to a postgres instance hosted on AWS ec2. 


## Architecture

Pipeline: Python

Database: Postgres

Both are running in docker containers.

The pipeline is scheduled using crontab. 


## Setup 

Python is used to pull, transform, and load data. The Database is Postgres. Both are running as docker containers.

### Requirements

1. Docker and Docker Compose
2. git

<!---
Fill in rest later. Add in diagrams for Architecture. 

Great Expectations for testing data would be nice as well.
-->


