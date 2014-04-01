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
        self.tags = ['tag1', 'tag2', 'tag3']


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

class BetterMetaPelicanIntegrationTestCase(unittest.TestCase):

    def setUp(self):
        self.generator = FakeGenerator()

    def test_module_should_have_register_method(self):
        self.assertTrue(hasattr(better_meta, 'register'))

    def test_should_create_meta_attribute_with_data_on_articles(self):
        BetterMeta.add_meta_to_articles(self.generator)

        for article in self.generator.articles:
            self.assertEqual(article.meta['description'], 'should-be-description')
