# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Pynani'
copyright = '2024, Jorge Juarez'
author = 'Jorge Juarez'
release = '1.3.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.autodoc',
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx_copybutton",
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'
html_logo = "_static/dark_logo_pynani.png"

html_static_path = ['_static']
html_theme_options = {
    "logo": {
        "image_dark": "_static/wite_logo_pynani.png",
    },
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/jorge-jrzz/Pynani",
            "icon": "fa-brands fa-github",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/pynani/",
            "icon": "https://img.shields.io/pypi/v/pynani",
            "type": "url",
        },
    ],
}

locale_dirs = ["locales/"]