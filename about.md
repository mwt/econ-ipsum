---
layout: page
title: About
permalink: /about/
---

Econ Ipsum is an Economics-themed Lorem Ipsum generator. It was built in Python using a dictionary of words and terms contained in the abstracts of all Econometrica papers since 1933. The generator shuffles the sentences from these abstracts while preserving word order.

The project was created by:
<ul>
{% for author in site.authors %}
<li class="p-name">
{%- if author.name -%}
<a class="u-name" href="{%- if author.domain -%}{{ author.domain }}{%- endif -%}">{{ author.name | escape }}</a>
{%- endif -%}
{%- if author.email -%}
<a href="mailto:{{ author.email }}" title="{{ author.email }}"><svg class="svg-icon"><use xlink:href="{{ '/assets/minima-social-icons.svg#mail' | relative_url }}"></use></svg></a>
{%- endif -%}
</li>
{% endfor %}
</ul>