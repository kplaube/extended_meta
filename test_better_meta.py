import unittest
import better_meta
from better_meta import BetterMeta


class FakeGenerator(object):

    def __init__(self):
        self.articles = []

        for i in range(10):
            article = FakeArticle()
            article.meta_description = 'should-be-description'
            self.articles.append(article)


class FakeArticle(object):

    def __init__(self):
        self.summary = 'should-be-summary'
        self.tags = [FakeTag('tag1'), FakeTag('tag2'), FakeTag('tag3')]


class FakeTag(object):

    def __init__(self, slug):
        self.slug = slug


class BetterMetaTestCase(unittest.TestCase):

    def setUp(self):
        self.article = FakeArticle()


class BetterMetaFilledMetaTestCase(BetterMetaTestCase):

    def test_should_create_meta_attribute_on_article_when_it_has_description(self):
        self.article.meta_description = 'should-be-meta-description'

        BetterMeta.create_meta_attribute(self.article)

        self.assertEqual(self.article.meta['description'], 'should-be-meta-description')

    def test_should_create_meta_attribute_on_article_when_it_has_keywords(self):
        self.article.meta_keywords = 'should-be-meta-keywords'

        BetterMeta.create_meta_attribute(self.article)

        self.assertEqual(self.article.meta['keywords'], 'should-be-meta-keywords')

    def test_should_create_meta_robots_on_article_when_it_has_robots(self):
        self.article.meta_robots = 'index,follow'

        BetterMeta.create_meta_attribute(self.article)

        self.assertEqual(self.article.meta['robots'], 'index,follow')


class BetterMetaUnfilledMetaTestCase(BetterMetaTestCase):

    def setUp(self):
        super(BetterMetaUnfilledMetaTestCase, self).setUp()
        BetterMeta.create_meta_attribute(self.article)

    def test_should_use_the_summary_as_description_when_it_hasnt_meta_description(self):
        self.assertEqual(self.article.meta['description'], 'should-be-summary')

    def test_should_use_tags_as_keywords_when_it_hasnt_meta_keywords(self):
        self.assertEqual(self.article.meta['keywords'], 'tag1, tag2, tag3')

    def test_should_use_index_follow_as_default_robots_data(self):
        self.assertEqual(self.article.meta['robots'], 'index,follow')

    def test_should_format_the_summary_to_use_as_description(self):
        self.article.summary = '<p>This is a "test"! <strong>Just a test!</strong></p>'
        BetterMeta.create_meta_attribute(self.article)

        self.assertEqual(self.article.meta['description'], 'This is a \"test\"! Just a test!')

    def test_should_limit_the_summary_content_when_using_it_as_description(self):
        self.article.summary = """<p>Do you see any Teletubbies in here? Do you
        see a slender plastic tag clipped to my shirt with my name printed on
        it? Do you see a little Asian child with a blank expression on his
        face sitting outside on a mechanical helicopter that shakes when you
        put quarters in it? No? Well, that's what you see at a toy store.
        And you must think you're in a toy store, because you're here shopping
        for an infant named Jeb.<p>"""
        BetterMeta.create_meta_attribute(self.article)

        self.assertEqual(self.article.meta['description'],
            'Do you see any Teletubbies in here? Do you see a slender plastic tag clipped to my shirt with my name printed on it? Do you see a little Asian child with a ...')


class BetterMetaPelicanIntegrationTestCase(unittest.TestCase):

    def setUp(self):
        self.generator = FakeGenerator()

    def test_module_should_have_register_method(self):
        self.assertTrue(hasattr(better_meta, 'register'))

    def test_should_create_meta_attribute_with_data_on_articles(self):
        BetterMeta.add_meta_to_articles(self.generator)

        for article in self.generator.articles:
            self.assertEqual(article.meta['description'], 'should-be-description')
