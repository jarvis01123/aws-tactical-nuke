import boto3

import tactical_nuke.utils.date as date_utils
import datetime


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


def delete_s3_buckets(s3_client, dry=True, **kwargs):
    predicate = get_s3_bucket_predicate(**kwargs)

    bucket_list = s3_client.list_buckets()['Buckets']

    filtered = [bucket for bucket in bucket_list if predicate(bucket)]

    for bucket in filtered:

        message = 'bucket={}, created={}'.format(
            bucket.get('Name'), bucket.get('CreationDate')
        )

        if dry:
            print('dry-mode -- would delete ' + message)

            continue
        else:

            print('deleting ' + message)

            try:
                bucket_resource = boto3.resource('s3').Bucket(bucket.get('Name'))
                bucket_resource.object_versions.delete()

                bucket_resource.delete()

            except Exception as e:

                print('Failed to delete bucket {}, ignoring'.format(bucket.get('Name')))


