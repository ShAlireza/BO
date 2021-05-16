import re
from typing import List, Union, Tuple

from crontab import CronTab, CronItem
from data import CronJob
from exceptions import MultipleJobsWithGivenId

from .event_push import parser as event_push_parser


class CronHandler:

    def __init__(self, user='alireza'):
        self.cron = CronTab(user=user)

    def add_job(self, cron_job: CronJob) -> CronJob:
        job = self.cron.new(
            command=cron_job.full_command,
            comment=cron_job.id
        )
        job.setall(
            cron_job.minute,
            cron_job.hour,
            cron_job.day_of_month,
            cron_job.month,
            cron_job.day_of_week
        )

        self.cron.write()

        return cron_job

    def delete_job(self, job_id=None, job_command=None, job_time=None):
        if job_id:
            return self.cron.remove_all(
                comment=job_id
            )
        elif job_command:
            return self.cron.remove_all(
                command=job_command
            )
        elif job_time:
            return self.cron.remove_all(
                time=job_time
            )

    def delete_all_jobs(self):
        return self.cron.remove_all()

    def edit_job(
            self,
            cron_job: CronJob
    ):
        _, cron_item = self.get_job_by_id(
            job_id=cron_job.id,
            return_cron_item=True
        )
        self._edit_job(
            job=cron_item
        )

    def edit_jobs(
            self,
            jobs_command
    ):
        jobs = self.get_jobs_by_command(
            job_command=jobs_command
        )

        for job in jobs:
            self._edit_job(
                job=job
            )

    def _edit_job(
            self,
            job
    ):
        pass

    def disable_job(
            self,
            cron_job: CronJob
    ) -> bool:

        _, cron_item = self.get_job_by_id(
            job_id=cron_job.id,
            return_cron_item=True
        )
        return self._disable_job(cron_item)

    def disable_jobs(
            self,
            job_command
    ) -> List[bool]:
        _, cron_items = self.get_jobs_by_command(
            job_command=job_command,
            return_cron_item=True
        )

        results: List[bool] = []

        for cron_item in cron_items:
            results.append(self._disable_job(cron_item))

        return results

    def _disable_job(
            self,
            job: CronItem
    ) -> bool:
        return job.enable(False)

    def get_job_by_id(
            self,
            job_id,
            return_cron_item=False
    ) -> Union[CronJob, Tuple[CronJob, CronItem]]:

        cron_items: List[CronItem] = list(self.cron.find_comment(
            comment=job_id
        ))

        if len(cron_items) > 1:
            raise MultipleJobsWithGivenId("multiple jobs found")

        cron_item = cron_items[0]
        cron_job = self.cron_job_from_cron_item(cron_item)

        if return_cron_item:
            return cron_job, cron_item
        return cron_job

    def get_jobs_by_command(
            self,
            job_command,
            return_cron_item=False
    ) -> Union[List[CronJob], Tuple[List[CronJob], List[CronItem]]]:
        cron_items = list(self.cron.find_command(
            command=job_command
        ))

        cron_jobs = list(map(self.cron_job_from_cron_item, cron_items))

        if return_cron_item:
            return cron_jobs, cron_items
        return cron_jobs

    def get_jobs_by_time(
            self,
            *time,
            return_cron_item=False
    ) -> Union[List[CronJob], Tuple[List[CronJob], List[CronItem]]]:
        cron_items = list(self.cron.find_time(
            *time
        ))

        cron_jobs = list(map(self.cron_job_from_cron_item, cron_items))

        if return_cron_item:
            return cron_jobs, cron_items
        return cron_jobs

    def get_all_jobs(
            self,
            return_cron_items=False
    ) -> Union[List[CronJob], Tuple[List[CronJob], List[CronItem]]]:
        cron_items = self.cron.crons

        cron_jobs = list(map(self.cron_job_from_cron_item, cron_items))

        if return_cron_items:
            return cron_jobs, cron_items
        return cron_jobs

    def get_jobs_with_unique_command(
            self,
            return_cron_items=False
    ) -> Union[List[CronJob], Tuple[List[CronJob], List[CronItem]]]:
        cron_items = self.cron.commands

        cron_jobs = list(map(self.cron_job_from_cron_item, cron_items))

        if return_cron_items:
            return cron_jobs, cron_items
        return cron_jobs

    def get_jobs_with_unique_id(
            self,
            return_cron_items=False
    ) -> Union[List[CronJob], Tuple[List[CronJob], List[CronItem]]]:

        cron_items = self.cron.comments
        cron_jobs = list(map(self.cron_job_from_cron_item, cron_items))

        if return_cron_items:
            return cron_jobs, cron_items
        return cron_jobs

    def print_cron_jobs(
            self
    ) -> None:

        for job in self.cron:
            print(job)

    @staticmethod
    def cron_job_from_cron_item(
            cron_item: CronItem
    ) -> CronJob:

        command_split = re.split("\\s+", cron_item.command)
        args = event_push_parser.parse_args(command_split[1:])

        return CronJob(
            id=cron_item.comment,
            enable=cron_item.is_enabled(),
            minute=cron_item.minute,
            technology=args.tech,
            host=args.host,
            port=args.port,
            hour=cron_item.hour,
            day_of_month=cron_item.dom,
            month=cron_item.month,
            day_of_week=cron_item.dow,
            full_command=cron_item.command,
        )
