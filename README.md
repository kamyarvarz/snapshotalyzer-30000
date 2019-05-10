# snapshotalyzer-30000
project to manage AWS EC2 instance snapshots 

## About

This project is a demo, and uses boto3 to manange AWS EC2 instance snapshots

## Configuring

shotty uses the configuration file created by the AWS cli. e.g.

`aws configure --profile identity`

## Running in Windows

`pipenv run python shotty\shotty.py <command> <subcommand> <--purpose=PURPOSE>`

*command* is instances, volumes, or snapshots
*subcommand* - depends on command:
    instances has the following subcommands
        list, start, or stop

    volumes has the following subcommands
        list

    snapshots has the following subcommands
        list

*purpose* is optional and is your tag name