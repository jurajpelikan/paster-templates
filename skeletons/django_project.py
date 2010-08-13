"""
Paster template for django projects.
"""
import os
import subprocess
import glob
import shutil
import stat

from paste.script.templates import Template, var
from update_env import update_all


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

        update_all(variables, output_dir, variables['project'])
        os.chdir(_static)
        if not os.path.exists('admin-media'):
            os.symlink('../env/src/django/django/contrib/admin/media', 'admin-media')
        os.chdir(_project_root)
        subprocess.call([
            _django_admin, "startproject", "project"
            ])
    
        # rename dot files
        for dot_file in glob.glob(os.path.join(_project_root, 'dot.*')):
            os.rename(dot_file, dot_file.replace('/dot', '/')) 
                                  
        # copy update_env script
        _update_env = os.path.join(_bin, 'update_env')
        _update_env_py = os.path.join(os.path.dirname(__file__), 'update_env.py')
        shutil.copyfile(_update_env_py, _update_env)
        subprocess.call(['chmod', '755', _update_env])
