#!/usr/bin/env python3

from pathlib import Path
from diagrams import Cluster, Diagram
from diagrams.onprem.client import Users
from diagrams.saas.business import Servicenow
from diagrams.aws.compute import Lambda
from diagrams.programming.language import Python
from diagrams.onprem.ci import GithubActions
from diagrams.onprem.vcs import Github
from diagrams.custom import Custom

HOME_PATH = f"{Path(__file__).parent.resolve()}"

graph_attr = {
    "bgcolor": "transparent",
    "size": "13,13!"
}

def main():
    with Diagram("ServiceNow to GitHub PR Workflow", filename="images/servicenow_github_workflow", show=False, direction="LR", graph_attr=graph_attr):
        user = Users("User")
        
        with Cluster("ServiceNow"):
            servicenow = Servicenow("Form Submission")
            servicenow_script = Python("Transform & Send JSON")

        with Cluster("Automation Tool"):
            automation = Lambda("AWS Lambda / Zapier / API")

        with Cluster("GitHub"):
            github_api = Custom("GitHub API", icon_path=f"{HOME_PATH}/images/github.png")
            github_actions = GithubActions("GitHub Actions Workflow")
            github_repo = Github("GitHub Repository")

        # Define connections
        user >> servicenow >> servicenow_script >> automation >> github_api >> github_actions >> github_repo
        github_repo >> Custom("Review & Merge", icon_path=f"{HOME_PATH}/images/merge.png")

if __name__ == "__main__":
    main()
