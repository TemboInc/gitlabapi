# Gitlabapi

A command line app to create and update Gitlab environment variables. Will read an env_file in the following form.
Variables will only be created or updated, NOT deleted.
  
    # Comments are ignored
    foo=bar
    spam=ham



[See the open Gitlab issue](https://gitlab.com/gitlab-org/gitlab-ce/issues/55460)

## Usage

`python createvariables.py env_file_path private_token project_name username`

A private token can be created in Gitlab Account Settings > Access Tokens. (The token must have has api scope)

