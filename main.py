#!/usr/bin/env python3

import pickle
from lib import Application, Candidate, Job, hr_interact


try:
    with open("is_running.txt", "r") as f:
        if "running" in f.read():
            raise Exception(
                "This program is already running"
            )
except FileNotFoundError:
    pass

with open("is_running.txt", "w") as f:
    f.write("program running")

try:
    with open("data.pickle", "rb") as data:
        (a_list, c_list, j_list) = pickle.load(data)
except FileNotFoundError:
    pass
else:
    Application.application_list = a_list
    Candidate.candidate_list = c_list
    Job.job_list = j_list

answer = 0
while answer not in (1, 2):
    answer = int(
        input(
            "Type 1 if you're in HR, 2 if you want to apply for a job: "
        )
    )
if answer == 1:
    hr_interact()
else:
    c = Candidate.login_or_register()
    c.interact()


with open("data.pickle", "wb") as data:
    pickle.dump(
        (
            Application.application_list,
            Candidate.candidate_list,
            Job.job_list,
        ),
        data,
    )

with open("is_running.txt", "w") as f:
    f.write("program done")
