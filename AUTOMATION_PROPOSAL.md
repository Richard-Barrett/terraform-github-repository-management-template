# Automating GitHub Pull Requests from a ServiceNow Form

To automate the process of creating a GitHub pull request (PR) based on a ServiceNow form, you need to integrate ServiceNow with an automation tool or middleware that can handle the logic of transforming the form data into a payload, triggering a GitHub Actions workflow, and creating the PR. Below is a step-by-step guide to achieve this:

## Step 1: Build the ServiceNow Form

### Create a ServiceNow Form:
In ServiceNow, create a custom form with fields for:

- **Target Organization**: Dropdown to select the GitHub organization.
- **Repository Name**: Text field for the repository name.
- **Description**: Text field for the repository description.
- **Language**: Dropdown to select the programming language (e.g., Python, Java, Go).
- **Visibility**: Dropdown to select public or private.
- **Additional Options**: Checkboxes for enabling issues, wiki, etc.

### Add a Script to the Form:
Use a **Business Rule, Script Include, or Flow Designer** in ServiceNow to:

1. Collect the form data.
2. Transform it into a JSON payload.
3. Send the payload to an external automation tool (e.g., AWS Lambda, Zapier, or a custom API).

---

## Step 2: Set Up an Automation Tool

You need a middleware or automation tool to handle the logic between ServiceNow and GitHub. Here are some options:

### **Option 1: AWS Lambda**
#### Create a Lambda Function:
Write a Python or Node.js function to:
- Receive the JSON payload from ServiceNow.
- Validate the payload.
- Trigger a GitHub Actions workflow using the GitHub API.

#### Expose the Lambda Function:
Use **API Gateway** to expose the Lambda function as an HTTP endpoint.  
ServiceNow will send the payload to this endpoint.

---

### **Option 2: Zapier or Make (formerly Integromat)**
#### Create a Zap/Scenario:
- Set up a **trigger** for when a new ServiceNow form is submitted.
- Use an **action** to transform the form data into a JSON payload.
- Use another **action** to call the GitHub API or trigger a GitHub Actions workflow.

---

### **Option 3: Custom API**
#### Build a Custom API:
Use a framework like **Flask (Python)** or **Express (Node.js)** to create an API.  
The API will:
1. Receive the payload from ServiceNow.
2. Trigger a GitHub Actions workflow or directly create a PR using the GitHub API.

---

## Step 3: Trigger GitHub Actions Workflow

### **GitHub Actions Workflow**
Create a GitHub Actions workflow (e.g., `.github/workflows/create-repo-pr.yml`) that:
- Listens for a **repository_dispatch** event or a custom webhook.
- Updates the **locals.tf** file in the appropriate organization directory.
- Creates a pull request with the changes.

#### **Example Workflow:**

```yaml
name: Create Repository PR

on:
  repository_dispatch:
    types: [create-repo]

jobs:
  update-locals:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Update locals.tf
        run: |
          echo '${{ github.event.client_payload }}' > payload.json
          python update_locals.py --payload payload.json

      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v4
        with:
          title: "Add new repository: ${{ fromJson(github.event.client_payload).repository_name }}"
          branch: "new-repo-${{ fromJson(github.event.client_payload).repository_name }}"
          commit-message: "Add new repository configuration"
```

### Trigger the Workflow

Use the GitHub API to trigger the workflow with the payload:

```bash
curl -X POST \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/OWNER/REPO/dispatches \
  -d '{"event_type":"create-repo","client_payload":{PAYLOAD_JSON}}'
```

## Step 4: Integrate ServiceNow with the Automation Tool

### ServiceNow Outbound REST API

Use ServiceNow's REST Message or Flow Designer to send the JSON payload to the automation tool (e.g., AWS Lambda, Zapier, or your custom API).

#### Example REST Message in ServiceNow

Create a REST Message in ServiceNow with:

- Endpoint: The URL of your automation tool (e.g., AWS API Gateway endpoint).
- HTTP Method: POST
- Authentication: If required, add authentication headers (e.g., API key).

#### Script to Send Payload

```javascript
var restMessage = new RESTMessage();
restMessage.setEndpoint("https://your-automation-tool-endpoint.com");
restMessage.setHttpMethod("POST");
restMessage.setRequestHeader("Content-Type", "application/json");

var payload = {
  organization: current.getValue("organization"),
  repository_name: current.getValue("repository_name"),
  description: current.getValue("description"),
  language: current.getValue("language"),
  visibility: current.getValue("visibility"),
  enable_issues: current.getValue("enable_issues"),
  enable_wiki: current.getValue("enable_wiki")
};

restMessage.setRequestBody(JSON.stringify(payload));
var response = restMessage.execute();
``` 

## Step 5: Test the End-to-End Process

1. Submit the ServiceNow Form
Fill out the form in ServiceNow and submit it.

2. Verify the Payload
Ensure the payload is correctly sent to the automation tool.

3. Check GitHub Actions
Verify that the GitHub Actions workflow is triggered and creates a PR.

4. Review and Merge
Review the PR and merge it to create the repository.

---

## Summary of Tools and Technologies

| **Tool**           | **Purpose** |
|-------------------|----------------------------------------------|
| **ServiceNow**    | Form creation and payload generation        |
| **Automation Tool** | AWS Lambda, Zapier, or a custom API to handle the payload and trigger GitHub Actions |
| **GitHub Actions** | Workflow to update `locals.tf` and create a PR |
| **GitHub API**    | To trigger workflows or create PRs programmatically |
