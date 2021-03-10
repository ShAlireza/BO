import argparse

import os
import sys

parser = argparse.ArgumentParser(
    description='push an event to queue',
    allow_abbrev=False
)

parser.add_argument(
    '-i',
    '--id',
    metavar='id',
    type=str,
    help='the cron job id',
    required=True,
    nargs=1
)

args = parser.parse_args()

cron_job_id = args.id[0]
