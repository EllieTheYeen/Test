---
layout: default
---
<div id="top_links">
    <a href="/" title="Main page">Home</a>
</div>

{%- if page.title -%}
    <h1 class="page-heading">{{ page.title }}</h1>
{%- endif -%}

{{ content }}

{%- if page.author != nil -%}
By {{ page.author }}
{%- else if site.author != nil -%}
By {{ site.author | escape }}
{%- else -%}
{%- endif -%}

<div id="bottom_links">
    <a href="#a-title" title="Go to the top of the page">Top</a>
    <a href="/" title="Go to the main page">Home</a>
    <a href="/feed.xml" title="The RSS feed">RSS</a>
    <a href="{{ page.path | prepend: 'https://github.com/EllieTheYeen/Test/blob/main/' }}" title="Source of this page">Source</a>
</div>
