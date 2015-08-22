#!/usr/bin/env python3

import requests


domain = 'http://dakis.gimbutas.lt/api/'
exp_data = {
    "description": "First successful post through API",
    "algorithm": "TestTasks",
    "neighbours": "Nearest",
    "stopping_criteria": "x_dist",
    "stopping_accuracy": "0.01",
    "subregion": "simplex",
    "inner_problem_accuracy": None,
    "inner_problem_iters": 10,
    "inner_problem_division": "LongesEdge",
    "lipschitz_estimation": "min_allowed",
    "simplex_division": "LongestEdge",
    "valid": True,
    "mistakes": "",
}

resp = requests.post(domain + 'experiments/', data=exp_data)
exp_url = resp.json()['url']

task_data = {
    "func_name": "GKLS",
    "func_cls": 1,
    "func_id": 1,
    "calls": 123,
    "subregions": 1041,
    "duration": "0.12",
    "f_min": None,
    "x_min": None,
    "experiment": exp_url,
}
requests.post(domain + 'tasks/', data=task_data)

task_data['func_id'] = 2
task_data['calls'] = 213
requests.post(domain + 'tasks/', data=task_data)
