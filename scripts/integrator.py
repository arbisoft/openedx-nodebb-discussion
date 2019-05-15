
import os

EDLY_APP_NAME = "'openedx.features.openedx_edly_discussion'"
TAB_ENTRY_POINT = '"openedx_edly_discussion = openedx.features.openedx_edly_discussion.plugins:EdlyTab"'
EDLY_DISCUSSION_FLAG = 'ENABLE_EDLY_DISCUSSION'


def append_in_file(file_path, line_to_append='', list_starting='', indent=1):
    """
    Appends the given line in the specified list.
    """
    output_file_content = []
    with open(file_path, "r+") as input:
        is_appended = False
        while True:
            line = input.readline()
            if not line:
                break
            stripped_line = line.strip()
            if not stripped_line.startswith('#') and stripped_line.startswith(list_starting) and '[' in stripped_line:
                while not is_appended:
                    output_file_content.append(line)
                    line = input.readline()
                    if not line:
                        break
                    stripped_line = line.strip()
                    if line_to_append in stripped_line and not stripped_line.startswith('#'):
                        is_appended = True
                        break
                        
                    if not stripped_line.startswith('#') and '#' in stripped_line:
                        line_tokens = line.split('#',1)
                        stripped_appname = line_tokens[0].strip()
                        if not stripped_appname.endswith(','):
                            new_appname = stripped_appname + ','
                            line_tokens[0] = line_tokens[0].replace(stripped_appname, new_appname)
                            line = '#'.join(line_tokens)
                    elif (not stripped_line.endswith(',') and not stripped_line.startswith(']')
                            and not stripped_line.startswith('#') and not stripped_line == ''):
                        line = line.rstrip() + ',\n'

                    if stripped_line.startswith(']'):
                        output_file_content.append("{}{},\n".format(" " * 4 * indent, line_to_append))
                        is_appended = True
            output_file_content.append(line)

    with open(file_path, "w") as output:
        for line in output_file_content:
            output.write(line)


def update_aws_production_file(file_path):
    """
    Appends lines at the end (production.py and aws.py) of file which are responsible to get env and auth tokens
    from the json files.
    """
    is_appended_auth = False
    is_appended_env = False
    with open(file_path, 'r') as aws_file:
        for line in aws_file:
            stripped_line = line.strip()
            if not stripped_line.startswith('#') and 'EDLY_DISCUSSION_SECRETS = AUTH_TOKENS.get' in stripped_line:
                is_appended_auth = True
            if not stripped_line.startswith('#') and 'EDLY_DISCUSSION_SETTINGS = ENV_TOKENS.get' in stripped_line:
                is_appended_env = True

    if not is_appended_auth or not is_appended_env:
        with open(file_path, 'a') as aws_file:
            aws_file.seek(0)
            aws_file.write('\n')
            aws_file.write('##################### Openedx Edly Discussion Secrets ###########\n')
            if not is_appended_auth:
                aws_file.write('\n')
                aws_file.write("EDLY_DISCUSSION_SECRETS = AUTH_TOKENS.get('EDLY_DISCUSSION_SECRETS', {")
                aws_file.write("})\n")
            if not is_appended_env:
                aws_file.write('\n')
                aws_file.write("EDLY_DISCUSSION_SETTINGS = ENV_TOKENS.get('EDLY_DISCUSSION_SETTINGS', None)\n")


def update_urls_file(file_path):
    """
    Appends discussion app urls at the end of the given file (urls.py).
    """
    is_appended = False
    with open(file_path, 'r') as urls_file:
        for line in urls_file:
            stripped_line = line.strip()
            if (not stripped_line.startswith('#') and
                    "if settings.FEATURES.get('{}'):".format(EDLY_DISCUSSION_FLAG) in stripped_line):
                is_appended = True

    if not is_appended:
        with open(file_path, 'a') as urls_file:
            urls_file.seek(0)
            urls_file.write('\n')
            urls_file.write("if settings.FEATURES.get('{}'):\n".format(EDLY_DISCUSSION_FLAG))
            urls_file.write("{}urlpatterns += [\n{}url(\n".format(' ' * 4, ' ' * 8))
            urls_file.write("{}".format(' ' * 12))
            urls_file.write("r'^courses/{}/edly'.format(settings.COURSE_ID_PATTERN),\n")
            urls_file.write("{}include('openedx.features.openedx_edly_discussion.urls'),\n".format(' ' * 12))
            urls_file.write("{}name='edly_discussion_endpoints',\n{}".format(' ' * 12, ' ' * 8))
            urls_file.write("),\n\t]")


if __name__ == "__main__":
    file_path = 'cms/envs/common.py'
    append_in_file(file_path, EDLY_APP_NAME, 'INSTALLED_APPS', indent=1)
    print('{} has been configured successfully !!!'.format(file_path))

    file_path = 'lms/envs/common.py'
    append_in_file(file_path, EDLY_APP_NAME, 'INSTALLED_APPS', indent=1)
    print('{} has been configured successfully !!!'.format(file_path))

    file_path = 'setup.py'
    append_in_file(file_path, TAB_ENTRY_POINT, '"openedx.course_tab"', indent=3)
    print('{} has been configured successfully !!!'.format(file_path))

    file_path = 'lms/envs/production.py'
    if os.path.isfile(file_path):
        update_aws_production_file(file_path)
        print('{} has been configured successfully !!!'.format(file_path))

        file_path = 'cms/envs/production.py'
        update_aws_production_file(file_path)
        print('{} has been configured successfully !!!'.format(file_path))
    else:
        file_path = 'lms/envs/aws.py'
        update_aws_production_file(file_path)
        print('{} has been configured successfully !!!'.format(file_path))

        file_path = 'cms/envs/aws.py'
        update_aws_production_file(file_path)
        print('{} has been configured successfully !!!'.format(file_path))

    file_path = 'lms/urls.py'
    update_urls_file(file_path)
    print('{} has been configured successfully !!!'.format(file_path))
