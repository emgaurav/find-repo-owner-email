import requests
import json

github_token = "github-token-here"

headers = {
    "Authorization": f"token {github_token}",
    "Accept": "application/vnd.github.v3+json"
}

def get_top_contributor_email(repo_name):
    contributor_url = f"https://api.github.com/repos/{repo_name}/contributors"
    response = requests.get(contributor_url, headers=headers)
    if response.status_code == 200:
        contributors = json.loads(response.text)
        if contributors:
            top_contributor = contributors[0]['login']
            commits_url = f"https://api.github.com/repos/{repo_name}/commits?author={top_contributor}"
            response = requests.get(commits_url, headers=headers)
            if response.status_code == 200:
                commits = json.loads(response.text)
                if commits:
                    return commits[0]['commit']['author']['email']
    return None

if __name__ == "__main__":
    with open('repo-list-goes-here.txt', 'r') as f:
        repo_list = [line.strip() for line in f.readlines()]

    for repo_name in repo_list:
        top_contributor_email = get_top_contributor_email(repo_name)
        if top_contributor_email:
            print(f"The email of the top contributor for the repository {repo_name} is {top_contributor_email}.")
        else:
            print(f"Could not find email information for the repository {repo_name}.")
