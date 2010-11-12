"""
Paster template for django projects.
"""
import os
import subprocess
import glob

from paste.script.templates import Template


class DjangoProjectTemplate(Template):
    """
    Paster temlate class for django projects. This creates directory structure,
    sets up virtualenv and installs packages in this environment. Next it creates
    django project a prepares apache config file.
    """

    summary = "Django project template."
    _template_dir = "templates/django_project"
    vars = []
    
    def post(self, command, output_dir, variables): # pylint: disable-msg=R0201,W0613
        """
        - create virtualenv
        - install pip
        - install pip_requirements
        - generate apache config
        """
        _bin = os.path.abspath(os.path.join(output_dir, "env", "bin"))
        _admin_media_root = os.path.abspath(os.path.join(
            output_dir, "env", 'src', 'django', 'django', 'contrib', 'admin', 'media'))
        _static = os.path.abspath(os.path.join(output_dir, 'static'))
        _django_admin = os.path.abspath(os.path.join(_bin, 'django-admin.py'))
        _project_root = os.path.abspath(output_dir)

        # update_all(variables, output_dir, variables['project'])
        os.chdir(_static)
        if not os.path.exists('admin-media'):
            os.symlink('../env/src/django/django/contrib/admin/media', 'admin-media')
        os.chdir(_project_root)

        subprocess.call([
            "virtualenv", "--no-site-packages",
            os.path.join(_project_root, "env")
            ])

        # if not os.path.exists('project'):
        #     subprocess.call([
        #         _django_admin, "startproject", "project"
        #         ])
    
        # rename dot files
        for dot_file in glob.glob(os.path.join(_project_root, 'dot.*')):
            if not os.path.exists(dot_file.replace('/dot', '/')):
                os.rename(dot_file, dot_file.replace('/dot', '/')) 
                                  
