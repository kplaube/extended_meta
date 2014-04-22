Better Meta
===========

[![Build Status](https://travis-ci.org/kplaube/better_meta.svg?branch=master)](https://travis-ci.org/kplaube/better_meta)

A Pelican plugin that provides better meta information for Pelican's article objects.

Installing
----------

*Better Meta* uses [BeautifulSoup][] and [Jinja2][] as dependencies. You need to install them to use operations like finding **og_image** and formatting the article's description.

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


  [BeautifulSoup]: http://www.crummy.com/software/BeautifulSoup/ "A Python library designed for quick turnaround projects like screen-scraping"
  [Jinja2]: http://jinja.pocoo.org/docs/ "Jinja2 is a modern and designer friendly templating language for Python"
