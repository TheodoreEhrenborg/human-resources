#!/usr/bin/env python3

from lib import Application, Candidate, Job, hr_interact
import pickle

try:
    with open("data.pickle", "rb") as f:
        (a_list, c_list, j_list) = pickle.load(f)
except FileNotFoundError:
    pass
else:
    Application.application_list = a_list
    Candidate.candidate_list = c_list
    Job.job_list = j_list

print("Make sure only one can run at a time")

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


with open("data.pickle", "wb") as f:
    pickle.dump(
        (
            Application.application_list,
            Candidate.candidate_list,
            Job.job_list,
        ),
        f,
    )
