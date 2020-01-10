import boto3


def delete_s3_buckets(s3_client, predicate=lambda x: True, dry=True):
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


