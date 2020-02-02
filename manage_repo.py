import subprocess
import requests
import sys


class ProcessGithub:
    def __init__(self, username=None, gen_token=None):
        self.USERNAME, self.GEN_TOKEN = username, gen_token

    def createRepo(self):
        if self.USERNAME == None or self.GEN_TOKEN == None:
            raise ValueError("Username or generated token is empty")
        r = requests.post(
            "https://api.github.com/users/{}/repos?access_token={}".format(
                self.USERNAME, self.GEN_TOKEN),
            data={
                "name": "Hello-World",
                "description": "This is your first repository",
                "homepage": "https://github.com",
                "private": false,
                "has_issues": true,
                "has_projects": true,
                "has_wiki": true
            })

        if r.status_code != 200:
            sys.exit()

        clone_url = r.text.clone_url
        subprocess.check_output(['git', 'clone', clone_url], cwd=repo_dir)
