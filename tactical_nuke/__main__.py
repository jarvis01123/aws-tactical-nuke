#!/usr/bin/env python

import boto3
import click
import datetime
import sys

import tactical_nuke.utils.s3 as s3_utils
import tactical_nuke.utils.date as date_utils


def get_s3_bucket_predicate(**kwargs):
    predicates = []

    if kwargs.get('earlier_than'):
        earlier_date = date_utils.str2datetime(kwargs.get('earlier_than'))
        predicates.append(lambda bucket: bucket.get('CreationDate') < earlier_date)

    if kwargs.get('later_than'):
        later_date = date_utils.str2datetime(kwargs.get('later_than'))
        predicates.append(lambda bucket: bucket.get('CreationDate') > later_date)

    if kwargs.get('created_on'):

        def date_on(bucket):
            created_date = date_utils.str2datetime(kwargs.get('created_on'))
            next_date = created_date + datetime.timedelta(days=1)

            bucket_created = bucket.get('CreationDate')

            return created_date < bucket_created < next_date

        predicates.append(date_on)

    if kwargs.get('starts_with'):
        predicates.append(lambda bucket: bucket.get('Name').startswith(kwargs.get('starts_with')))

    if kwargs.get('ends_with'):
        predicates.append(lambda bucket: bucket.get('Name').endswith(kwargs.get('ends_with')))

    if kwargs.get('contains'):
        predicates.append(lambda bucket: kwargs.get('contains') in bucket.get('Name'))

    if kwargs.get('exclude'):
        predicates.append(lambda bucket: bucket.get('Name') not in kwargs.get('exclude'))

    return lambda x: all([p(x) for p in predicates])


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

    s3_utils.delete_s3_buckets(
        s3_client,
        get_s3_bucket_predicate(**kwargs),
        dry=dry)


if __name__ == '__main__':
    sys.exit(cli())
