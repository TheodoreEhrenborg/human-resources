#!/usr/bin/env python3

import lib


j = lib.Job()


j.describe()


c = lib.Candidate()


c.register()


c.apply()


a = lib.Application.application_list[0]
