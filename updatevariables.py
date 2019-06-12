from gitlab import Gitlab
import click


@click.command()
@click.argument('env_file', type=click.File('r'))
@click.argument('private_token')
@click.argument('project_name')
@click.argument('username')
def update_variables(env_file, private_token, project_name, username):
    """
    A command line app to create and update Gitlab environment variables. Will read an env_file in the following form.
    Variables will only be created or updated, NOT deleted.

        # Comments are ignored
        foo=bar
        spam=ham


    :param env_file: env file to read
    :param private_token: Gitlab private token. This can be created in Account Settings > Access Tokens (api scope)
    :param project_name: Gitlab Project to update
    :param username: Gitlab username
    :return:
    """

    valid_lines = [line.strip() for line in env_file.readlines() if not line.startswith('#')]
    new_env_vars = [{'key': pair[0], 'value': pair[1]} for pair in [line.split('=') for line in valid_lines]]
    url = "https://gitlab.com"
    g = Gitlab(url=url, private_token=private_token)

    user = g.users.list(username=username)[0]
    user_project = user.projects.list(search=project_name)[0]
    project_id = user_project.get_id()

    project = g.projects.get(project_id)
    existing_vars = {var.attributes['key']: var.attributes['value'] for var in project.variables.list()}
    existing_keys = existing_vars.keys()

    for env_var in new_env_vars:
        if env_var['key'] not in existing_keys:
            print(f"creating {env_var['key']} set to {env_var['value']}")
            project.variables.create(env_var)
        elif env_var['value'] != existing_vars[env_var['key']]:
            print(f"updating {env_var['key']} from {existing_vars[env_var['key']]} to {env_var['value']}")
            project.variables.update(env_var['key'], env_var)

    print("Done")


if __name__ == '__main__':
    update_variables()
