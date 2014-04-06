from jinja2 import Markup
from pelican import signals
import textwrap

META_ATTRIBUTES = ('description', 'keywords', 'robots')
DEFAULT_ROBOTS = 'index,follow'
META_DESCRIPTION_LENGTH = 155


def register():
    signals.article_generator_finalized.connect(BetterMeta.add_meta_to_articles)


class BetterMeta:
    settings = {}

    @classmethod
    def add_meta_to_articles(cls, generator):
        cls.settings = generator.settings

        for article in generator.articles:
            cls.create_meta_attribute(article)

    @classmethod
    def create_meta_attribute(cls, article):
        article.meta = {
            'canonical': cls.get_canonical(article),
        }

        for key in META_ATTRIBUTES:
            article_attrib = "meta_%s" % key

            if hasattr(article, article_attrib):
                meta_value = getattr(article, article_attrib)
            else:
                meta_value = getattr(cls, "get_default_%s" % article_attrib)(article)

            article.meta[key] = meta_value

    @classmethod
    def get_canonical(cls, article):
        return "{0}/{1}".format(cls.settings.get('SITEURL', ''), article.url)

    @classmethod
    def get_default_meta_description(cls, article):
        summary = Markup(article.summary).striptags()
        description = textwrap.wrap(summary, META_DESCRIPTION_LENGTH)[0]
        description = Markup.escape(description)

        if len(summary) > META_DESCRIPTION_LENGTH:
            return description + '...'
        else:
            return description

    @classmethod
    def get_default_meta_keywords(cls, article):
        return ', '.join([tag.slug for tag in article.tags])

    @classmethod
    def get_default_meta_robots(cls, article):
        return DEFAULT_ROBOTS
