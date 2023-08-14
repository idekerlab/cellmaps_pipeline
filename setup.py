#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
import os
import re
from setuptools import setup, find_packages


with open(os.path.join('cellmaps_pipeline', '__init__.py')) as ver_file:
    for line in ver_file:
        line = line.rstrip()
        if line.startswith('__version__'):
            version = re.sub("'", "", line[line.index("'"):])
        elif line.startswith('__description__'):
            desc = re.sub("'", "", line[line.index("'"):])
        elif line.startswith('__repo_url__'):
            repo_url = re.sub("'", "", line[line.index("'"):])
        elif line.startswith('__author__'):
            author = re.sub("'", "", line[line.index("'"):])
        elif line.startswith('__email__'):
            email = re.sub("'", "", line[line.index("'"):])

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['cellmaps_utils==0.1.0a16',
                'cellmaps_imagedownloader==0.1.0a10',
                'cellmaps_ppidownloader==0.1.0a3',
                'cellmaps_image_embedding==0.1.0a9',
                'cellmaps_ppi_embedding==0.1.0a5',
                'cellmaps_coembedding==0.1.0a5',
                'cellmaps_generate_hierarchy==0.1.0a8',
                'networkx>=2.8,<2.9',
                'tqdm']

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author=author,
    author_email=email,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    description=desc,
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_content_type = 'text/x-rst',
    include_package_data=True,
    keywords='cellmaps_pipeline',
    name='cellmaps_pipeline',
    packages=find_packages(include=['cellmaps_pipeline']),
    package_dir={'cellmaps_pipeline': 'cellmaps_pipeline'},
    scripts=[ 'cellmaps_pipeline/cellmaps_pipelinecmd.py'],
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url=repo_url,
    version=version,
    zip_safe=False)
