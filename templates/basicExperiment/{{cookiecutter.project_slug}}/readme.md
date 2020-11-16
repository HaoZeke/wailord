# ORCA {{cookiecutter.project_name}}

A short description of this project is:

> {{cookiecutter.desc}}

## About

This is a project directory generated with `wailord` and facilitated by `cookiecutter`.

## License

{% if cookiecutter.license == 'MIT' %}
MIT License © {{cookiecutter.year}} {{cookiecutter.author}}

{% elif cookiecutter.license == 'MPLv2' %}
Mozilla Public License v2 © {{cookiecutter.year}} {{cookiecutter.author}}

{% elif cookiecutter.license == 'Private' %}
All rights reserved © {{cookiecutter.year}} {{cookiecutter.author}}.
{% endif %}
