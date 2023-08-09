# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import pathlib
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys
import platform
import os

project = 'empire-config'
copyright = 'Y\'en a pas de copyrite, Yann Tremblay'
author = 'Yann Tremblay'
release = '1.0'

root: str = str(pathlib.Path(__file__).parent.parent)

if platform.system().lower() == 'windows':
    sys.path.insert(0, os.path.join(root, 'winvenv', 'Lib', 'site-packages'))
else:
    for candidate in ['venv', 'uxvenv']:
        if os.path.isdir(candidate):
            sys.path.insert(0, os.path.join(root, candidate, 'lib', 'site-packages'))
            break

sys.path.insert(0, os.path.join(root, 'src'))

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo'
]
todo_include_todos = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '.pytest_cache']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

autodoc_type_aliases = {
    'JsonType': 'empire_commons.types_.JsonType'
}