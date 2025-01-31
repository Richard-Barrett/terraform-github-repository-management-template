#!/usr/bin/env python3

from pathlib import Path
from diagrams import Cluster, Diagram
from diagrams.onprem.client import Users
from diagrams.aws.compute import Lambda
from diagrams.programming.language import Python
from diagrams.onprem.ci import GithubActions
from diagrams.custom import Custom

HOME_PATH = f"{Path(__file__).parent.resolve()}"

graph_attr = {
    "bgcolor": "transparent",
    "size": "15,15",  # Reduced size for balanced scaling
    "pad": "1.0",     # Padding to avoid overlapping text
    "dpi": "150",     # Keeps text sharp
    "fontname": "Arial",
    "fontsize": "18"
}

node_attr = {
    "fontsize": "14",
    "fontname": "Arial",
    "width": "2.5",       # Ensures all nodes have the same width
    "height": "2.5",      # Ensures consistent height
    "fixedsize": "true"   # Prevents nodes from auto-scaling
}

def main():
    with Diagram(
        "ServiceNow to GitHub PR Workflow",
        filename="images/servicenow_github_workflow",
        show=False,
        direction="LR",
        graph_attr=graph_attr,
        node_attr=node_attr
    ):
        
        # ✅ Wrap everything inside a "blue box"
        with Cluster("Workflow Diagram", graph_attr={"style": "filled", "fillcolor": "lightblue", "pencolor": "blue"}):
            
            with Cluster("User"):
                user = Users("User")

            with Cluster("ServiceNow"):
                servicenow = Custom("Form Submission", icon_path=f"{HOME_PATH}/images/servicenow.png")
                servicenow_script = Python("Transform & Send JSON")

            with Cluster("Automation Tool"):
                automation = Lambda("AWS Lambda")

            with Cluster("GitHub"):
                github_api = Custom("", icon_path=f"{HOME_PATH}/images/github.png")
                github_actions = GithubActions("")
                
                # ✅ Custom Git Repo icon (Scaled Properly)
                github_repo = Custom("", icon_path=f"{HOME_PATH}/images/git_repo.png")

                # ✅ Custom Merge icon (Scaled Properly)
                review_merge = Custom("", icon_path=f"{HOME_PATH}/images/merge_icon.png")

            # Define connections
            user >> servicenow >> servicenow_script >> automation >> github_api >> github_actions >> github_repo
            github_repo >> review_merge  # Now correctly using a custom merge icon

if __name__ == "__main__":
    main()
