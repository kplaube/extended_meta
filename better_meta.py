from pelican import signals

META_ATTRIBUTES = ('description', 'keywords', 'robots')


def register():
    signals.article_generator_finalized.connect(init_better_meta)


def init_better_meta(generator):
    for article in generator.articles:
        create_meta_attribute(article)


def create_meta_attribute(article):
    article.meta = {}

    for key in META_ATTRIBUTES:
        article_attrib = "meta_%s" % key

        if not hasattr(article, article_attrib):
            continue

        article.meta[key] = getattr(article, article_attrib)
