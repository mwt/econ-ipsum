---
layout: page
title: About
permalink: /about/
---

Econ Ipsum is an Economics-themed Lorem Ipsum generator. It was built in Python using a dictionary of words and terms contained in the abstracts of all papers published in Econometrica from 1933 to 2019. The generator shuffles the sentences from these abstracts while preserving word order.

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

The generator caches requests daily in blocks of 100 paragraphs. So, the first person who accesses the page each day causes 100 paragraphs to be generated. Everyone else who accesses the page within a 24 hour period will see the exact same paragraphs. After 24 hours, the cache will be refreshed with new content. You can generate as many paragraphs as you like.

The front-end of this project is hosted on [GitHub Pages](https://pages.github.com/) while the backend is hosted via [AWS Lambda](https://aws.amazon.com/lambda/). We would like to thank both for enabling this project to exist at no cost.