#!/usr/bin/env python3

from enum import Enum, auto


class Status(Enum):
    APPLIED = auto()
    INTERVIEWED = auto()
    REJECTED = auto()
    ACCEPTED = auto()


class Candidate:
    candidate_list = []

    @staticmethod
    def add(candidate):
        Candidate.candidate_list.append(candidate)

    @staticmethod
    def generate_id():
        return "C" + str(len(Candidate.candidate_list))

    def __init__(self):
        self.name = ""
        self.id_num = ""
        self.resume = ""
        self.applications = []

    def register(self):
        if self.id_num != "":
            raise Exception("Already registered")
        self.name = input("Name: ")
        self.get_resume()
        Candidate.add(self)
        self.id_num = Candidate.generate_id()

    def get_resume(self):
        self.resume = input("Your resume: ")

    def apply(self):
        a = Application()
        a.make_application(self)


class Job:
    job_list = []

    @staticmethod
    def add(job):
        Job.job_list.append(job)

    @staticmethod
    def generate_id():
        return "J" + str(len(Job.job_list))

    @staticmethod
    def print_available_jobs_short():
        any = False
        for job in Job.job_list:
            if job.available:
                any = True
                print("ID: " + job.id_num)
                print("Title: " + job.title)
                print()
        if not any:
            raise Exception("No jobs available")

    @staticmethod
    def get_ids():
        return [job.id_num for job in Job.job_list]

    @staticmethod
    def get_job_with_id(id_num):
        for job in Job.job_list:
            if job.id_num == id_num:
                return job
        raise Exception("No such job found")

    def __init__(self):
        self.title = ""
        self.id_num = ""
        self.description = ""
        self.available = True

    def describe(self):
        if self.id_num != "":
            raise Exception(
                "This job already has a description"
            )
        self.title = input("Title: ")
        self.description = input("Describe the job: ")
        Job.add(self)
        self.id_num = Job.generate_id()

    def close_job(self):
        self.available = False


class Application:

    application_list = []

    @staticmethod
    def add(application):
        Application.application_list.append(application)

    @staticmethod
    def generate_id():
        return "A" + str(len(Application.application_list))

    def __init__(self):
        self.id_num = ""
        self.candidate = None
        self.job = None
        self.status = Status.APPLIED
        self.interview_transcript = ""

    def make_application(self, candidate):
        if self.id_num != "":
            raise Exception(
                "This application was already made"
            )
        Job.print_available_jobs_short()
        print(
            "Enter the ID of the job you wish to apply for."
        )
        job_id_num = ""
        while job_id_num not in Job.get_ids():
            job_id_num = input("ID: ")
        self.job = Job.get_job_with_id(job_id_num)
        if not self.job.available:
            raise Exception("This job was already filled")
        self.candidate = candidate
        self.candidate.applications.append(self)
        Application.add(self)
        self.id_num = Application.generate_id()

    def do_interview(self):
        if self.status != Status.APPLIED:
            raise Exception(
                "This candidate has already been interviewed"
            )
        self.interview_transcript = input(
            "Transcript of interview: "
        )
        self.status = Status.INTERVIEWED

    def reject(self):
        if self.status == Status.APPLIED:
            raise Exception(
                "Please do an interview before rejecting the candidate"
            )
        elif self.status in (
            Status.REJECTED,
            Status.ACCEPTED,
        ):
            raise Exception("Already accepted or rejected")
        elif self.status != Status.INTERVIEWED:
            raise Exception(
                "The status variable is corrupted"
            )
        self.status = Status.REJECTED

    def accept(self):
        if self.status == Status.APPLIED:
            raise Exception(
                "Please do an interview before accepting the candidate"
            )
        elif self.status in (
            Status.REJECTED,
            Status.ACCEPTED,
        ):
            raise Exception("Already accepted or rejected")
        elif self.status != Status.INTERVIEWED:
            raise Exception(
                "The status variable is corrupted"
            )
        self.status = Status.ACCEPTED
        self.job.close_job()
