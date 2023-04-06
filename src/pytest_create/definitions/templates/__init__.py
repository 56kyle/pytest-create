"""Contains default Jinja2 templates for use as ObjectDef templates."""
from pathlib import Path

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import Template


TEMPLATES_FOLDER: Path = Path(__file__).parent
ENV: Environment = Environment(
    loader=FileSystemLoader(str(TEMPLATES_FOLDER)), autoescape=True
)

CLASS_TEMPLATE: Template = ENV.get_template("class.jinja2")
FUNCTION_TEMPLATE: Template = ENV.get_template("function.jinja2")
MODULE_TEMPLATE: Template = ENV.get_template("module.jinja2")
