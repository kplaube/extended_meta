Extended Meta
=============

[![Build Status](https://travis-ci.org/kplaube/extended_meta.svg?branch=master)](https://travis-ci.org/kplaube/extended_meta)

A Pelican plugin that provides better meta information for Pelican's article objects.

Installing
----------

*Extended Meta* uses [BeautifulSoup][] and [Jinja2][] as dependencies. You need to install them to use operations like finding **og_image** and formatting the article's description:

    $ pip install -r requirements.txt

Also, of course, you need to add the plugin to your ``PLUGINS`` list:

    PLUGINS = ['extended_meta', ]

How to use it
-------------

This plugins adds the ``meta`` variable to article's context, so you can use the following indexes to access the meta information:

    article.meta['description']
    article.meta['keywords']
    article.meta['robots']
    article.meta['canonical']
    article.meta['og_description']
    article.meta['og_title']
    article.meta['og_url']
    article.meta['og_image']

In your template, you can just print these guys:

    {% if article and article.meta %}
        <meta name="description" content="{{ article.meta.description }}">
        <meta name="keywords" content="{{ article.meta.keywords }}">
        <meta property="og:title" content="{{ article.meta.og_title }}">
        <meta property="og:description" content="{{ article.meta.og_description }}">
        <meta property="og:url" content="{{ article.meta.og_url }}">
        <meta property="og:image" content="{{ article.meta.og_image }}">
    {% endif %}

How it works
------------

You can use a set of post's meta data to define a specific meta information for your article:

    Title: How to use Extended Meta Pelican's plugin
    Date: 2014-04-22 13:00
    Category: development
    Tags: development, pelican, extended-meta, blog
    Slug: how-to-use-extended-meta-pelican-plugin
    meta_description: A brief description long enough to fit in search results
    meta_keywords: Some keywords that describes your article
    meta_robots: index,follow is the word
    meta_og_title: A cool Open Graph's title
    meta_og_description: A cool Open Graph's description
    meta_og_url: A different way to view your article through Open Graph?
    meta_og_image: The full address to an image

*Extended Meta* will verify all these "meta_" names, and group them as a dictionary in article's context. When the plugin doesn't find these names, it will use the following default values:

* **meta_description:** Will use a (formatted) piece of article's content
* **meta_keywords:** Will use article's tags
* **meta_robots:** Will use "index,follow"

The ``canonical`` key will always use the article URL.

The default values for all "meta_og_" are a little different:

* **meta_og_title:** Will use article's title
* **meta_og_description:** Will use ``meta_description`` key
* **meta_og_url:** Will use ``canonical`` key
* **meta_og_image:** Will use the first image of the article, if it doesn't find any, will use ``DEFAULT_OG_IMAGE`` of your Pelican's settings

You can see a live action example in my [blog][] repository, that uses the [Yapeme][] theme.

  [BeautifulSoup]: http://www.crummy.com/software/BeautifulSoup/ "A Python library designed for quick turnaround projects like screen-scraping"
  [Jinja2]: http://jinja.pocoo.org/docs/ "Jinja2 is a modern and designer friendly templating language for Python"
  [blog]: https://github.com/kplaube/blog "The implementation of my blog, using Pelican"
  [Yapeme]: https://github.com/kplaube/Yapeme "A responsive (and simple) theme for Pelican"
