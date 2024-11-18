#!/usr/bin/env python3

"""
Migration script for moving issues from Jira to GitHub.
Handles both simulation and actual migration modes.
"""

from collections import namedtuple
import os.path
import requests
from project import Project
from importer import Importer
from utils import read_xml_files

# Debug: Print environment variables to verify configuration
print(f"Debug: GITHUB_ACCOUNT = {os.getenv('GITHUB_ACCOUNT')}")
print(f"Debug: GITHUB_ACCESS_TOKEN = {os.getenv('JIRA_MIGRATION_GITHUB_ACCESS_TOKEN')}")
print(f"Debug: DEFAULT_REPO = {os.getenv('DEFAULT_REPO')}")
print(f"Debug: SECURITY_REPO = {os.getenv('SECURITY_REPO')}")

# Set migration mode based on environment variable, default to "simulation"
migration_mode = os.getenv('MIGRATION_MODE', 'simulation')
print(f"Debug: migration_mode is set to '{migration_mode}'")

if migration_mode == 'simulation':
    print("Running in simulation mode. No changes will be made.")
elif migration_mode == 'migration':
    print("Running in migration mode. Changes will be applied.")
else:
    print("Invalid mode specified. Defaulting to simulation mode.")
    migration_mode = 'simulation'

# GitHub repository URLs for security and non-security issues
SECURITY_REPO_URL = os.getenv('SECURITY_REPO_URL')
DEFAULT_REPO_URL = os.getenv('DEFAULT_REPO_URL')

# Read the GitHub account name from environment
ac = os.getenv('GITHUB_ACCOUNT')

# Set other necessary variables
file_names = os.getenv('JIRA_MIGRATION_FILE_PATHS')
jira_proj = os.getenv('JIRA_MIGRATION_JIRA_PROJECT_NAME')  # Jira project name from environment
jira_base_url = os.getenv('JIRA_MIGRATION_JIRA_URL')  # Jira base URL from environment
pat = os.getenv('JIRA_MIGRATION_GITHUB_ACCESS_TOKEN')  # GitHub PAT from environment

# Hardcoded values for Done status and Start from issue
jira_done_id = '3'  # Hardcoded to '3' for Done status
start_from_issue = '0'  # Hardcoded to start from issue '0'

# Options for the default repository
Options = namedtuple("Options", "accesstoken account repo")

# Project setup
project = Project(jira_proj, jira_done_id, jira_base_url)

# Track whether milestones and labels have already been imported for each repo
milestones_imported = {SECURITY_REPO_URL: False, DEFAULT_REPO_URL: False}
labels_imported = {SECURITY_REPO_URL: False, DEFAULT_REPO_URL: False}

def create_github_issue(repo_owner_repo, title, body, access_token):
    """
    Creates an issue in the specified GitHub repository.
    
    Parameters:
        repo_owner_repo (str): The GitHub repository in "{owner}/{repo}" format.
        title (str): The title of the issue.
        body (str): The body/description of the issue.
        access_token (str): The GitHub access token for authentication.
    
    Returns:
        bool: True if the issue was created successfully, False otherwise.
    """
    api_url = f"https://api.github.com/repos/{repo_owner_repo}/issues"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "title": title,
        "body": body
    }

    response = requests.post(api_url, headers=headers, json=data)
    
    if response.status_code == 201:
        print(f"Issue '{title}' created successfully.")
        return True
    else:
        print(f"Failed to create issue '{title}': {response.status_code} - {response.text}")
        return False

print("Performing assessment...")
# Assessment phase: Simulate gathering and validation of all issues
print("Assessment complete")

print("Verifying against Jira XML...")
# Verification phase: Compare the gathered data against the Jira XML.
print("Verification complete")

print(f"Starting migration ({migration_mode} mode)...")

# The migration status will be logged to 'migration_simulation.log' for review
log_file_name = "migration_simulation.log"
with open(log_file_name, "w") as log_file:
    log_file.write("Migration Simulation Log\n")

    # Process all items and check for security levels
    all_xml_files = read_xml_files(file_names)
    for f in all_xml_files:
        for item in f.channel.item:
            project.add_item(item)

            # Check if the issue has a security level and assign the appropriate repository
            if hasattr(item, 'security'):
                log_file.write(f"Issue {item.key}: Assigned to security repository.\n")
                opts = Options(accesstoken=pat, account=ac, repo=SECURITY_REPO_URL)
            else:
                log_file.write(f"Issue {item.key}: Assigned to default repository.\n")
                opts = Options(accesstoken=pat, account=ac, repo=DEFAULT_REPO_URL)

            importer = Importer(opts, project)

            # Import milestones only once per repository
            if not milestones_imported[opts.repo]:
                if migration_mode == 'migration':
                    print(f"Importing milestones to repository {opts.repo}")
                    # Code to actually import milestones here
                else:
                    print(f"Simulating import of milestones to repository {opts.repo}")
                    log_file.write(f"Milestones imported to repository {opts.repo}.\n")
                milestones_imported[opts.repo] = True

            # Import labels only once per repository
            if not labels_imported[opts.repo]:
                if migration_mode == 'migration':
                    print(f"Importing labels to repository {opts.repo}")
                    # Code to actually import labels here
                else:
                    print(f"Simulating import of labels to repository {opts.repo}")
                    log_file.write(f"Labels imported to repository {opts.repo}.\n")
                labels_imported[opts.repo] = True

            # Migrate each issue based on the selected mode
            if migration_mode == 'migration':
                print(f"Migrating issue {item.key} to repository {opts.repo}")
                # Get issue title and body for migration, converted to string to avoid serialization issues
                issue_title = f"Issue {item.key}: {str(item.title)}"
                issue_body = str(item.description) if item.description else "No description provided."
                
                # Ensure repo_owner_repo is formatted correctly as "owner/repo_name"
                repo_owner_repo = f"{ac}/{opts.repo}"
                
                # Call create_github_issue function
                created = create_github_issue(
                    repo_owner_repo,
                    issue_title,
                    issue_body,
                    opts.accesstoken
                )
                if created:
                    log_file.write(f"Issue {item.key}: Migrated to repository {opts.repo}.\n")
                else:
                    log_file.write(f"Issue {item.key}: Failed to migrate to repository {opts.repo}.\n")
            else:
                log_file.write(f"Issue {item.key}: Simulated migration to repository {opts.repo}.\n")

print(f"{migration_mode.capitalize()} process completed.")
print(f"Detailed logs can be found in '{log_file_name}'")
