Thumbor AWS (forked)
====================

Installation
------------

```bash
pip install git+git://github.com/voxmedia/aws@patched
```

Origin story REDUX
------------------

This is a fork of https://github.com/thumbor-community/aws ; which
wasn't working for our setup, when we tried replacing the PyPI version
of tc-aws (which *also* wasn't working) with this one.

That repo is itself a fork of https://github.com/willtrking/thumbor_aws ; as this
repository was not maintained anymore, we decided to maintain it under
the ``thumbor-community`` organisation.

The relevant branch (`patched`) is forked from the originally-tagged
v1.1.0 release, because there was a substantial refactoring after that,
which was causing the latest `master` version to not be usable (at
least without more work).

This currently interacts with S3 almost-perfectly (in terms of saving
files in the right place), but doesn't seem to actually be performing
the requested transformation on the image before it saves the
result. :/

Features
--------

 * tc_aws.loaders.s3_loader
 * tc_aws.result_storages.s3_storage
 * tc_aws.storages.s3_storage

Additional Configuration values used:

  # the Amazon Web Services access key to use
    AWS_ACCESS_KEY = ""
    # the Amazon Web Services secret of the used access key
    AWS_SECRET_KEY = ""



    # configuration settings specific for the s3_loader

    # list of allowed buckets for the s3_loader
    S3_ALLOWED_BUCKETS = []



    # configuration settings specific for the storages

    # put data into S3 using the Server Side Encryption functionality to
    # encrypt data at rest in S3
    # https://aws.amazon.com/about-aws/whats-new/2011/10/04/amazon-s3-announces-server-side-encryption-support/
    S3_STORAGE_SSE = True or False (Default: False)

    # put data into S3 with Reduced Redundancy
    # https://aws.amazon.com/about-aws/whats-new/2010/05/19/announcing-amazon-s3-reduced-redundancy-storage/
    S3_STORAGE_RRS = True or False (Default: False)

    # Use Role-based connection
    # http://docs.aws.amazon.com/IAM/latest/UserGuide/roles-assume-role.html
    AWS_ROLE_BASED_CONNECTION = True or False (Default: False)


    #Optional config value to enable the HTTP loader
    #This would allow you to load watermarks in over your images dynamically through a URI
    #E.g.
    #http://your-thumbor.com/unsafe/filters:watermark(http://example.com/watermark.png,0,0,50)/s3_bucket/photo.jpg
    AWS_ENABLE_HTTP_LOADER = True or False (Default: False)


    # Optional additional configuration for the Boto-Client used to access S3.
    # see http://boto.readthedocs.org/en/latest/ref/s3.html?highlight=boto.s3.connection.s3connection#boto.s3.connection.S3Connection
    # for all available config options
    BOTO_CONFIG = {
        'host': 'fakes3.local.dev',
        'is_secure': False
        }
