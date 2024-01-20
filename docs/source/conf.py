# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
from pathlib import Path
sys.path.insert(0, Path(__file__).parent.parent.parent.__str__())
import neonize

project = "neonize"
copyright = "2024, krypton-byte"
author = "krypton-byte"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.coverage",
    "sphinx.ext.napoleon", 
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
    "myst_parser",
    "sphinx_autodoc_typehints",
]

templates_path = ["_templates"]
autosummary_generate = True
autodoc_default_flags = ["members"]
exclude_patterns = ["gocode"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
# html_static_path = ["_static"]
