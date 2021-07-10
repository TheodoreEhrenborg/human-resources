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

    @staticmethod
    def login_or_register():
        response = ""
        while response not in ("y", "n"):
            response = input(
                "Have you already registered? (y/n) "
            ).lower()
        if response == "y":
            id_num = input("Your ID: ")
            c = Candidate.find_candidate_with_id(id_num)
            print("Hello, " + c.name)
            return c
        else:
            c = Candidate()
            c.register()
            return c

    @staticmethod
    def find_candidate_with_id(id_num):
        for c in Candidate.candidate_list:
            if c.id_num == id_num:
                return c
        else:
            raise Exception("ID not found")

    @staticmethod
    def print_candidates():
        any = False
        for c in Candidate.candidate_list:
            any = True
            print("ID: " + c.id_num)
            print("Name: " + c.name)
            print("Resume: " + c.resume)
            if len(c.applications) > 0:
                print("Applications made: ")
            for a in c.applications:
                print(a)
            print()
        if not any:
            raise Exception("No candidates")

    def __init__(self):
        self.name = ""
        self.id_num = ""
        self.resume = ""
        self.applications = []

    def register(self):
        if self.id_num != "":
            raise Exception("Already registered")
        self.name = input("Name: ")
        self.make_resume()
        Candidate.add(self)
        self.id_num = Candidate.generate_id()
        print("Your ID: " + self.id_num)

    def make_resume(self):
        self.resume = input("Your resume: ")

    def apply(self):
        a = Application()
        try:
            a.make_application(self)
        except Exception as e:
            print(e)

    def list_my_applications(self):
        Application.list_applications_of(self)

    def list_available_jobs(self):
        try:
            Job.print_available_jobs_long()
        except Exception as e:
            print(e)

    def interact(self):
        options = [
            "exit",
            "apply",
            "list",
            "check",
            "update",
            "see",
        ]
        while True:
            print(
                """Your options are:
    list --- see a list of available jobs
    see --- see your resume
    update --- update your resume
    check --- check the status of your job applications
    apply --- apply for a job
    exit"""
            )
            choice = ""
            while choice not in options:
                choice = input("Your choice: ").lower()
            if choice == "list":
                self.list_available_jobs()
            elif choice == "see":
                print(self.resume)
            elif choice == "update":
                self.make_resume()
            elif choice == "check":
                self.list_my_applications()
            elif choice == "apply":
                self.apply()
            else:
                break


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
    def print_available_jobs_long():
        any = False
        for job in Job.job_list:
            if job.available:
                any = True
                print("ID: " + job.id_num)
                print("Title: " + job.title)
                print("Description: " + job.description)
                print()
        if not any:
            raise Exception("No jobs available")

    @staticmethod
    def print_jobs_long():
        any = False
        for job in Job.job_list:
            any = True
            print("ID: " + job.id_num)
            print("Title: " + job.title)
            print("Description: " + job.description)
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

    @staticmethod
    def list_applications_of(candidate):
        for a in Application.application_list:
            print(a)
            print()

    @staticmethod
    def print_open_applications():
        any = False
        for a in Application.application_list:
            if a.status not in (
                Status.REJECTED,
                Status.ACCEPTED,
            ):
                any = True
                print(a)
                print()
        if not any:
            raise Exception("No open applications")

    @staticmethod
    def print_applications():
        any = False
        for a in Application.application_list:
            any = True
            print(a)
            print()
        if not any:
            raise Exception("No open applications")

    @staticmethod
    def get_application_with_id(id_num):
        for a in Application.application_list:
            if a.id_num == id_num:
                return a
        raise Exception("No such application found")

    def __init__(self):
        self.id_num = ""
        self.candidate = None
        self.job = None
        self.status = Status.APPLIED
        self.interview_transcript = ""

    def __str__(self):
        return (
            "ID: "
            + self.id_num
            + "\nJob: "
            + self.job.title
            + "\nStatus: "
            + self.status.name.title()
        )

    def get_details(self):
        output = str(self)
        output += "\nCandidate: " + a.candidate.id_num
        if self.status != Status.APPLIED:
            output += (
                "\nInterview transcript: "
                + a.interview_transcript
            )
        return output

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


def hr_interact():
    options = [
        "exit",
        "make",
        "close",
        "list cands",
        "list apps",
        "list open apps",
        "list jobs",
        "list open jobs",
        "details",
        "interview",
        "accept",
        "reject",
    ]
    while True:
        print(
            """Your options are:
        make --- make a job posting
        close --- manually close a job posting
        list cands --- list all candidates
        list apps --- list all job applications
        list open apps --- like previous, excluding accepted and rejected ones
        list jobs --- list all job postings
        list open jobs --- list all open job postings
        details --- print details of an application
        interview --- conduct an interview for an application
        accept --- accept an application
        reject --- reject an application
        exit"""
        )
        choice = ""
        while choice not in options:
            choice = input("Your choice: ").lower()
        if choice == "make":
            j = Job()
            j.describe()
        elif choice == "close":
            try:
                j = Job.get_job_with_id(input("Job ID: "))
                j.available = False
            except Exception as e:
                print(e)
        elif choice == "list cands":
            try:
                Candidate.print_candidates()
            except Exception as e:
                print(e)
        elif choice == "list apps":
            try:
                Application.print_applications()
            except Exception as e:
                print(e)
        elif choice == "list open apps":
            try:
                Application.print_open_applications()
            except Exception as e:
                print(e)
        elif choice == "list jobs":
            try:
                Job.print_jobs_long()
            except Exception as e:
                print(e)
        elif choice == "list open jobs":
            try:
                Job.print_available_jobs_long()
            except Exception as e:
                print(e)
        elif choice == "details":
            if True:
                # try:
                # I got an error when I selected details
                a = Application.get_application_with_id(
                    input("Application ID: ")
                )
                print(a.get_details())
        #    except Exception as e:
        #        print(e)
        elif choice == "interview":
            try:
                a = Application.get_application_with_id(
                    input("Application ID: ")
                )
                a.do_interview()
            except Exception as e:
                print(e)
        elif choice == "accept":
            try:
                a = Application.get_application_with_id(
                    input("Application ID: ")
                )
                a.accept()
            except Exception as e:
                print(e)
        elif choice == "reject":
            try:
                a = Application.get_application_with_id(
                    input("Application ID: ")
                )
                a.reject()
            except Exception as e:
                print(e)
        else:
            break
