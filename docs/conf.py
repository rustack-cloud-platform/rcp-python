# Configuration file for the Sphinx documentation builder.
# It also creates OpenAPI file

import os
import sys


# -- Fix pathes --------------------------------------------------------------
sys.path.insert(0, os.path.abspath('..'))


# -- Project information -----------------------------------------------------
project = 'rustack-esu'
copyright = '2021, SBCloud LLC'
author = 'Development Team'

# The full version, including alpha/beta/rc tags
version = '0.1.4'
# release = '0.1.4'
language = 'ru'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

exclude_patterns = ['_build']
pygments_style = 'sphinx'
todo_include_todos = False


exclude_patterns = []
html_theme = 'sphinx_rtd_theme'

htmlhelp_basename = 'examplecodedoc'


# -- Additional configuration ------------------------------------------------
autodoc_inherit_docstrings = True
autodoc_default_options = {
    'member-order': 'bysource',
    'members': True,
}

autoclass_content = 'both'
