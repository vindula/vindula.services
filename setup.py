from setuptools import setup, find_packages
import os

version = '0.1'

long_description = open("README.txt").read() + "\n" +\
                   open(os.path.join("docs", "INSTALL.txt")).read() + "\n" +\
                   open(os.path.join("docs", "CREDITS.txt")).read() + "\n" +\
                   open(os.path.join("docs", "HISTORY.txt")).read()

setup(name='vindula.services',
      version=version,
      description="",
      long_description=long_description,
      classifiers=[
          "Development Status :: 1 - Alpha",
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Plone :: 4.2",
          "Intended Audience :: Developers",
          "Intended Audience :: System Administrators",
          "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
          "Operating System :: OS Independent",
          "Programming Language :: JavaScript",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
          "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary",
          "Topic :: Multimedia",
          "Topic :: Software Development :: Libraries :: Python Modules",
          ],
      keywords='vindula liberiun intranet plone archetypes',
      author='Gustavo Lepri',
      author_email='gustavolepri@liberiun.com',
      url='https://liberiun.codebasehq.com/projects/vindula/repositories/vindulaservices',
      license='GPLv2',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['vindula', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      extras_require={'test': ['plone.app.testing[robot]>=4.2.2']},
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["templer.localcommands"],
      )
