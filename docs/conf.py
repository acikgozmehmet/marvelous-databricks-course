import sphinx_rtd_theme  # noqa
import os
import sys

[sys.path.insert(0, x[0]) for x in os.walk("../src")]

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "house_prices"
copyright = "2025, Marvelous MLOps"
author = "Mehmet Acikgoz"

version = "0.1.1"
release = "0.1.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autodoc", "sphinx.ext.viewcode", "sphinx.ext.napoleon", "sphinxcontrib.video"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "logo only": True,
    "collapse_navigation": True,
    "sticky_navigation": True,
    "includehiden": True,
    "navigation_depth": 4,
    "titles_only": False,
}

html_static_path = ["_static"]


def setup(app):
    app.add_css_file("css/customWidth.css")
