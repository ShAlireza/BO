from crontab import CronTab
from exceptions import MultipleJobsWithGivenId


class CronHandler:

    def __init__(self, user='alireza'):
        self.cron = CronTab(user=user)

    def add_job(self, job):

        pass

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

    def edit_job(self, job_id=None, job_command=None):
        job = self.get_job_by_id(
            job_id=job_id
        )
        self._edit_job(
            job=job
        )

    def edit_jobs(self, jobs_command):
        jobs = self.get_jobs_by_command(
            job_command=jobs_command
        )

        for job in jobs:
            self._edit_job(
                job=job
            )

    def _edit_job(self, job):
        pass

    def disable_job(self, job_id):
        job = self.get_job_by_id(
            job_id=job_id
        )
        self._disable_job(job)

    def disable_jobs(self, job_command):
        jobs = self.get_jobs_by_command(
            job_command=job_command
        )
        for job in jobs:
            self._disable_job(job)

    def _disable_job(self, job):
        pass

    def get_job_by_id(self, job_id):
        command = list(self.cron.find_comment(
            comment=job_id
        ))
        if len(command) > 1:
            raise MultipleJobsWithGivenId("multiple jobs found")
        return command[0] if command else None

    def get_jobs_by_command(self, job_command):
        return list(self.cron.find_command(
            command=job_command
        ))

    def get_jobs_by_time(self, *time):
        return list(self.cron.find_time(
            time
        ))

    def get_all_jobs(self):
        return self.cron.crons

    def get_jobs_with_unique_command(self):
        return self.cron.commands

    def get_jobs_with_unique_id(self):
        return self.cron.comments

    def print_cron_jobs(self):
        for job in self.cron:
            print(job)
