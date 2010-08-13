from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='paster-templates',
      version=version,
      description="PasteScript templates.",
      long_description="PasteScript templates.",
      classifiers = [
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules"
          ],
      keywords='paste templates django',
      author='Juraj Pelikan',
      author_email='juraj.pelikan@gmail.com',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'PasteScript',
          'virtualenv'
      ],
      entry_points="""
      # -*- Entry points: -*-
      [paste.paster_create_template]
      django_project = skeletons:DjangoProjectTemplate
      """,
      )
