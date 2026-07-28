---
layout: page
title: Protocols
subtitle: Experimental protocols and methods
---

{% assign date_format = site.date_format | default: "%B %-d, %Y" %}

{% for post in site.tags.protocols %}
<div class="post-preview">
  <a href="{{ post.url | relative_url }}">
    <h3 class="post-title">{{ post.title | strip_html }}</h3>
    {% if post.subtitle %}
    <h4 class="post-subtitle">{{ post.subtitle | strip_html }}</h4>
    {% endif %}
  </a>
  <p class="post-meta">Posted on {{ post.date | date: date_format }}</p>
  {% if post.tags.size > 0 %}
  <div class="blog-tags">
    <span>Tags:</span>
    {% for tag in post.tags %}
    <a href="/tags#{{ tag }}">{{ tag }}</a>
    {% endfor %}
  </div>
  {% endif %}
</div>
{% endfor %}
