from pelican import signals

META_ATTRIBUTES = ('description', 'keywords', 'robots')
DEFAULT_ROBOTS = 'index,follow'


def register():
    signals.article_generator_finalized.connect(BetterMeta.add_meta_to_articles)


class BetterMeta:

    @classmethod
    def add_meta_to_articles(cls, generator):
        for article in generator.articles:
            cls.create_meta_attribute(article)

    @classmethod
    def create_meta_attribute(cls, article):
        article.meta = {}

        for key in META_ATTRIBUTES:
            article_attrib = "meta_%s" % key

            if hasattr(article, article_attrib):
                meta_value = getattr(article, article_attrib)
            else:
                meta_value = getattr(cls, "get_default_%s" % article_attrib)(article)

            article.meta[key] = meta_value

    @classmethod
    def get_default_meta_description(cls, article):
        return article.summary

    @classmethod
    def get_default_meta_keywords(cls, article):
        return ', '.join([tag.slug for tag in article.tags])

    @classmethod
    def get_default_meta_robots(cls, article):
        return DEFAULT_ROBOTS
