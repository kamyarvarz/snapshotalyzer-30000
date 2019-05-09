# snapshotalyzer-30000
project to manage AWS EC2 instance snapshots 

## About

This project is a demo, and uses boto3 to manange AWS EC2 instance snapshots

## Configuring

shotty uses the configuration file created by the AWS cli. e.g.

`aws configure --profile identity`

## Running

`pipenv run "python shotty/shotty.py <command> <--purpose=PURPOSE"`

*command* is list, start, or stop
*project* is optional