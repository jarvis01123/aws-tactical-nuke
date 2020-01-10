from setuptools import setup, find_packages
setup(
    name="AWS Tactical Nuke",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': ['atn=tactical_nuke.__main__:cli']
    },

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=['click', 'pytz', 'boto3'],

    # metadata to display on PyPI
    author="Travis McKee",
    author_email="travis.andrew.mckee@gmail.com",
    description="CLI tool for cleaning up old AWS resources that are no longer needed.",
    keywords="aws clean s3",
)
