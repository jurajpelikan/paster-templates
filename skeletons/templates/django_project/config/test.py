from string import Template

_file = open('apache-conf.template')
template = Template(_file.read())
_file.close()

print template.substitute({
    'server_name': 'aaa',
    'project_root': '/home',
    'user': 'user',
    'group': 'group'

    })


