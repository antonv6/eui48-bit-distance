# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

sys.path.insert(0, os.path.abspath('../src/'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'eui48-bit-distance'
copyright = '2026, Anton Shestakov'
author = 'Anton Shestakov'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
]

templates_path = ['_templates']
exclude_patterns = ['_build']

language = 'en'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_theme_options = {
    'top_of_page_buttons': ['view'],
    'source_repository': 'https://github.com/antonv6/eui48-bit-distance',
    'source_branch': 'main',
    'source_directory': 'docs/',
}

nitpick_ignore = {
    ('py:class', 'collections.abc.Iterable'),
}
