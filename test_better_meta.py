import unittest
import better_meta
from better_meta import init_better_meta, create_meta_attribute


class FakeGenerator(object):

    def __init__(self):
        self.articles = []

        for i in range(10):
            article = FakeArticle()
            article.meta_description = 'should-be-description'
            self.articles.append(article)


class FakeArticle(object):
    pass


class BetterMetaFilledMetaTestCase(unittest.TestCase):

    def setUp(self):
        self.article = FakeArticle()

    def test_should_create_meta_attribute_on_article_when_it_has_description(self):
        self.article.meta_description = 'should-be-meta-description'

        create_meta_attribute(self.article)

        self.assertEqual(self.article.meta['description'], 'should-be-meta-description')

    def test_should_create_meta_attribute_on_article_when_it_has_keywords(self):
        self.article.meta_keywords = 'should-be-meta-keywords'

        create_meta_attribute(self.article)

        self.assertEqual(self.article.meta['keywords'], 'should-be-meta-keywords')

    def test_should_create_meta_robots_on_article_when_it_has_robots(self):
        self.article.meta_robots = 'index,follow'

        create_meta_attribute(self.article)

        self.assertEqual(self.article.meta['robots'], 'index,follow')


class BetterMetaUnfilledMetaTestCase(unittest.TestCase):

    def setUp(self):
        self.article = FakeArticle()

    def test_should_create_meta_attribute_as_a_empty_dict(self):
        create_meta_attribute(self.article)
        self.assertEqual(self.article.meta, {})


class BetterMetaTestCase(unittest.TestCase):

    def setUp(self):
        self.generator = FakeGenerator()

    def test_module_should_have_register_method(self):
        self.assertTrue(hasattr(better_meta, 'register'))

    def test_should_create_meta_attribute_with_data_on_articles(self):
        init_better_meta(self.generator)

        for article in self.generator.articles:
            self.assertEqual(article.meta['description'], 'should-be-description')
