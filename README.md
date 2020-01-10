## Description

AWS Tactical Nuke (`atn`) is a tool for selectively deleting AWS resources that are no longer needed. At this time, 
it supports deleting S3 resources only. 

### Installation
Recommended to run within a virtualenv.

```python setup.py install```

### Usage - S3
By default, running `atn s3` will run in dry-mode, which will simply list all the buckets in your account.

```bash
$ atn s3
atn s3
dry-mode -- would delete bucket=<bucket>, created=2019-12-09 19:55:38+00:00
dry-mode -- would delete bucket=<bucket>, created=2020-01-09 19:55:38+00:00
...
```

You can then use a number of filters to narrow down your search to a narrower subset of buckets before you delete.

```bash
$ atn s3 --contains=<substring> --earlier-than=2020 --later-than=2019-06-01
dry-mode -- would delete bucket=<bucket>, created=2019-12-09 19:55:38+00:00
...
```

Once you have the list narrowed down to the buckets you want cleared out, you pass in the `--delete` flag to empty
out the buckets and delete them.

 
```bash
$ atn s3 --contains=<substring> --earlier-than=2020 --later-than=2019-06-01 --delete
deleting bucket=<bucket>, created=2019-12-09 19:55:38+00:01
...
```


