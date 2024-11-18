import requests

class Importer:
    def __init__(self, options, project):
        self.accesstoken = options.accesstoken
        self.account = options.account
        self.repo = options.repo
        self.project = project

    def import_milestones(self):
        # Simulating the milestone import process
        print(f"Simulating migration of milestones to repository {self.repo}")

    def import_labels(self, label_selector):
        # Simulating the label import process
        print(f"Simulating migration of labels to repository {self.repo}")

    def import_issues(self, start_from_issue):
        # Simulate importing the issues
        for issue in self.project._project['Issues'][start_from_issue:]:
            print(f"Simulating migration of issue {issue['key']} to repository {self.repo}")
            # Debug: Construct and print the API URL
            issue_url = f"https://api.github.com/repos/{self.account}/{self.repo}/issues"
            print(f"Debug: Issue API URL = {issue_url}")

            # Debug: Print headers
            headers = {
                "Authorization": f"token {self.accesstoken}",
                "Accept": "application/vnd.github+json",
            }
            print(f"Debug: Headers = {headers}")

            # Debug: Print payload
            payload = {
                "title": issue["summary"],
                "body": issue.get("description", "No description provided."),
                "labels": issue.get("labels", [])
            }
            print(f"Debug: Payload = {payload}")

            # Attempt to make the API call
            response = requests.post(issue_url, json=payload, headers=headers)
            print(f"Debug: Response Status Code = {response.status_code}")
            print(f"Debug: Response Content = {response.text}")

            if response.status_code != 201:
                print(f"Failed to create issue '{issue['key']}': {response.status_code} - {response.text}")
            else:
                print(f"Successfully created issue '{issue['key']}'")

    def post_process_comments(self):
        # Simulate post-processing comments
        print(f"Simulating post-processing of comments in repository {self.repo}")
