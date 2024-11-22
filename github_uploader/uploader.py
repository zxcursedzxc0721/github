import os
import sys
import argparse
import configparser
from github import Github
from github.GithubException import GithubException

def get_config_file_path():
    """
    Returns the path to the configuration file in the user's home directory.
    """
    home = os.path.expanduser("~")
    config_file = os.path.join(home, ".github_uploader_config")
    return config_file

def get_token():
    """
    Retrieves the GitHub token from the configuration file.
    Returns None if the token is not found.
    """
    config_file = get_config_file_path()
    config = configparser.ConfigParser()
    if os.path.exists(config_file):
        config.read(config_file)
        if 'GitHub' in config and 'token' in config['GitHub']:
            return config['GitHub']['token']
    return None

def set_token(token):
    """
    Saves the GitHub token to the configuration file.
    """
    config_file = get_config_file_path()
    config = configparser.ConfigParser()
    config['GitHub'] = {'token': token}
    with open(config_file, 'w') as configfile:
        config.write(configfile)

def validate_token(token):
    """
    Validates the GitHub token.
    Returns True if the token is valid, otherwise False.
    """
    try:
        g = Github(token)
        user = g.get_user()
        user.login  # Attempt to get the user's login to validate the token
        return True
    except GithubException:
        return False

def upload_project(token, project_path, repo_name=None, private=False):
    """
    Uploads the project at the specified path to GitHub using the provided token.
    Creates a new repository if it does not exist.
    """
    g = Github(token)
    user = g.get_user()
    if not repo_name:
        repo_name = os.path.basename(os.path.abspath(project_path))
    try:
        repo = user.get_repo(repo_name)
        print(f"Repository '{repo_name}' already exists.")
    except GithubException as e:
        if e.status == 404:
            # Repository does not exist, create it
            repo = user.create_repo(name=repo_name, private=private)
            print(f"Created repository '{repo_name}'.")
        else:
            print(f"Error accessing repository: {e}")
            sys.exit(1)
    # Upload files
    for root, dirs, files in os.walk(project_path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, project_path)
            # Convert path to POSIX format for GitHub
            relative_path = relative_path.replace(os.path.sep, '/')
            with open(file_path, 'rb') as f:
                content = f.read()
            try:
                # Check if the file exists in the repository
                repo_contents = repo.get_contents(relative_path)
                # Update file
                repo.update_file(relative_path, f"Update {relative_path}", content, repo_contents.sha)
                print(f"Updated file '{relative_path}'.")
            except GithubException as e:
                if e.status == 404:
                    # File does not exist, create it
                    repo.create_file(relative_path, f"Add {relative_path}", content)
                    print(f"Created file '{relative_path}'.")
                else:
                    print(f"Error uploading file '{relative_path}': {e}")
    print("Upload completed.")

def main():
    """
    Main function that processes command-line arguments and starts the upload process.
    """
    parser = argparse.ArgumentParser(description="Upload a project to GitHub.")
    parser.add_argument('-p', '--path', required=True, help='Path to the project folder.')
    parser.add_argument('-r', '--repo', help='Name of the repository on GitHub. Defaults to the project folder name.')
    parser.add_argument('--private', action='store_true', help='Create a private repository.')
    parser.add_argument('--token', help='GitHub access token.')
    parser.add_argument('--reset-token', action='store_true', help='Reset the saved GitHub token.')
    args = parser.parse_args()

    if args.reset_token:
        set_token('')
        print("Saved GitHub token has been reset.")
        sys.exit(0)

    token = args.token or get_token()
    while not token or not validate_token(token):
        print("GitHub access token is missing or invalid.")
        token = input("Please enter your GitHub access token: ")
        if validate_token(token):
            set_token(token)
            break
        else:
            print("Invalid token, please try again.")

    project_path = args.path
    if not os.path.isdir(project_path):
        print(f"Project path '{project_path}' does not exist or is not a directory.")
        sys.exit(1)

    repo_name = args.repo
    upload_project(token, project_path, repo_name, private=args.private)

if __name__ == '__main__':
    main()