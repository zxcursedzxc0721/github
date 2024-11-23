## 🌟 GitHub Uploader

This script creates a github command that allows you to easily upload projects to GitHub. Just follow a few simple steps and you will be able to share your projects with the world!

### 📦 Installation

To install the command, run the following command in the terminal:

pip install .


After installation, you will have a github command that you can use to download your projects.

### 🛠️ Usage

To upload a project to GitHub, use the following command:

github -p <path_project folder> -r <repository name> --private --token <your_token>


### 📋 Arguments

- -p, --path: The required path to your project folder.
- -r, --repo: The name of the repository on GitHub. If not specified, the name of the project folder will be used.
- --private: Create a private repository.
- --token: Your GitHub access token.
- --reset-token: Reset the saved GitHub token.

### 🎉 Usage example

github -p "C:pathtoyourproject" -r "my-awesome-repo" --private --token "ghp
