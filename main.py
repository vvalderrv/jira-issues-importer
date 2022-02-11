import getpass
from collections import namedtuple
from lxml import objectify
from project import Project
from importer import Importer
from labelcolourselector import LabelColourSelector


def read_xml_sourcefile(file_names):
    files = list()
    for file_name in file_names.split(';'):
        all_text = open(file_name).read()
        files.append(objectify.fromstring(all_text))

    return files


file_names = input(
    'Path to JIRA XML query file (semi-colon separate for multiple files): ')
all_xml_files = read_xml_sourcefile(file_names)

jira_proj = input('JIRA project name: ') or 'INFRA'
jira_done_id = input('JIRA Done statusCategory ID [default "3"]: ') or '3'
jira_base_url = input('JIRA base url [default "https://issues.jenkins.io"]: ') or 'https://issues.jenkins.io'
ac = input('GitHub account name (user/org): ') or 'jenkins-infra'
repo = input('GitHub repository name: ') or 'helpdesk'
pat = input('Github Personal Access Token: ') # or '<your-github-pat>'
start_from_issue = input('Start from [default "0" (beginning)]: ') or '0'

Options = namedtuple("Options", "accesstoken account repo")
opts = Options(accesstoken=pat, account=ac, repo=repo)

project = Project(jira_proj, jira_done_id, jira_base_url)

for f in all_xml_files:
    for item in f.channel.item:
        project.add_item(item)

project.prettify()

input('Press any key to begin...')

'''
Steps:
  1. Create any milestones
  2. Create any labels
  3. Create each issue with comments, linking them to milestones and labels
  4: Post-process all comments to replace issue id placeholders with the real ones
'''
importer = Importer(opts, project)
colourSelector = LabelColourSelector(project)

importer.import_milestones()

if int(start_from_issue) == 0:
    importer.import_labels(colourSelector)

importer.import_issues(int(start_from_issue))
# importer.post_process_comments()
