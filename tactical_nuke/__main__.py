#!/usr/bin/env python

import boto3
import click
import sys

import tactical_nuke.utils.s3 as s3_utils

@click.group()
def cli():
    pass


@cli.command()
@click.option('--prefix')
@click.option('--earlier-than')
@click.option('--later-than')
@click.option('--created-on')
@click.option('--starts-with')
@click.option('--ends-with')
@click.option('--contains')
@click.option('--created-on')
@click.option('-e', '--exclude', multiple=True)
@click.option('--delete', is_flag=True, default=False)
def s3(**kwargs):
    s3_client = boto3.client('s3')

    dry = not kwargs.get('delete')

    s3_utils.delete_s3_buckets(s3_client, dry=dry, **kwargs)


if __name__ == '__main__':
    sys.exit(cli())
