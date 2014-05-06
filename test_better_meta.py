import unittest
import better_meta
from better_meta import BetterMeta


class FakeGenerator(object):

    def __init__(self):
        self.settings = {
        }
        self.articles = []

        for i in range(10):
            article = FakeArticle()
            article.meta_description = 'should-be-description'
            self.articles.append(article)


class FakeArticle(object):

    def __init__(self):
        self.title = 'should-be-title'
        self.summary = 'should-be-summary'
        self.content = """<p>Lorem ipsum</p>
        <p><span><img src="test.jpg"></span></p>
        <p>Dolor sit amet</p>"""
        self.tags = [FakeTag('tag1'), FakeTag('tag2'), FakeTag('tag3')]
        self.url = 'should-be-the-article-url.html'


class FakeTag(object):

    def __init__(self, slug):
        self.slug = slug


class BetterMetaTestCase(unittest.TestCase):

    def setUp(self):
        BetterMeta.settings['SITEURL'] = 'http://localhost'
        BetterMeta.settings['DEFAULT_OG_IMAGE'] = 'should-be-default-og-image.jpg'
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

    def test_should_create_meta_canonical(self):
        BetterMeta.create_meta_attribute(self.article)

        self.assertEqual(self.article.meta['canonical'],
                            'http://localhost/should-be-the-article-url.html')

    def test_should_create_meta_ogtitle_on_article_when_it_has_og_title(self):
        self.article.meta_og_title = 'should-be-meta-og-title'

        BetterMeta.create_meta_attribute(self.article)

        self.assertEqual(self.article.meta['og_title'], 'should-be-meta-og-title')

    def test_should_create_meta_ogdescription_on_article_when_it_has_og_description(self):
        self.article.meta_og_description = 'should-be-meta-og-description'

        BetterMeta.create_meta_attribute(self.article)

        self.assertEqual(self.article.meta['og_description'], 'should-be-meta-og-description')

    def test_should_create_meta_ogurl_on_article_when_it_has_og_url(self):
        self.article.meta_og_url = 'http://mycustomdomain/should-be-article-url.html'

        BetterMeta.create_meta_attribute(self.article)

        self.assertEqual(self.article.meta['og_url'],
                         'http://mycustomdomain/should-be-article-url.html')

    def test_should_create_meta_ogimage_on_article_when_it_has_og_image(self):
        self.article.meta_og_image = 'http://mycustomdomain/og.jpg'

        BetterMeta.create_meta_attribute(self.article)

        self.assertEqual(self.article.meta['og_image'],
                         'http://mycustomdomain/og.jpg')


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

        self.assertEqual(self.article.meta['description'], 'This is a &#34;test&#34;! Just a test!')

    def test_should_limit_the_summary_content_when_using_it_as_description(self):
        self.article.summary = """<p>Do you see any "Teletubbies" in here? Do you
        see a slender plastic tag clipped to my shirt with my name printed on
        it? Do you see a little Asian child with a blank expression on his
        face sitting outside on a mechanical helicopter that shakes when you
        put quarters in it? No? Well, that's what you see at a toy store.
        And you must think you're in a toy store, because you're here shopping
        for an infant named Jeb.<p>"""
        BetterMeta.create_meta_attribute(self.article)

        self.assertEqual(self.article.meta['description'],
            'Do you see any &#34;Teletubbies&#34; in here? Do you see a slender plastic tag clipped to my shirt with my name printed on it? Do you see a little Asian child with...')


class BetterMetaUnfilledOGMetaTestCase(BetterMetaTestCase):

    def setUp(self):
        super(BetterMetaUnfilledOGMetaTestCase, self).setUp()
        BetterMeta.create_meta_attribute(self.article)

    def test_should_use_the_article_title_as_ogtitle(self):
        self.assertEqual(self.article.meta['og_title'], 'should-be-title')

    def test_should_use_the_article_url_as_ogurl(self):
        self.assertEqual(self.article.meta['og_url'],
                         'http://localhost/should-be-the-article-url.html')

    def test_should_use_the_article_description_as_ogdescription(self):
        self.assertEqual(self.article.meta['og_description'],
                         'should-be-summary')

    def test_should_use_the_article_image_as_ogimage(self):
        self.assertEqual(self.article.meta['og_image'], 'http://localhost/test.jpg')


class BetterMetaUnfilledOGMetaAlternativeImageTestCase(BetterMetaTestCase):

    def test_should_use_the_first_image_of_the_article(self):
        self.article.content = """<h1>hey!</h1><p><div><img src="http://myhost/1.jpg"></div>
        </p><br><img src="2.jpg">"""
        BetterMeta.create_meta_attribute(self.article)

        self.assertEqual(self.article.meta['og_image'], 'http://myhost/1.jpg')

    def test_should_use_the_default_image_as_ogimage_when_article_hasnt_one(self):
        self.article.content = '<p>Lorem ipsum</p>'
        BetterMeta.create_meta_attribute(self.article)

        self.assertEqual(self.article.meta['og_image'],
                         'should-be-default-og-image.jpg')


class BetterMetaPelicanIntegrationTestCase(unittest.TestCase):

    def setUp(self):
        self.generator = FakeGenerator()

    def test_module_should_have_register_method(self):
        self.assertTrue(hasattr(better_meta, 'register'))

    def test_should_create_meta_attribute_with_data_on_articles(self):
        BetterMeta.add_meta_to_articles(self.generator)

        for article in self.generator.articles:
            self.assertEqual(article.meta['description'], 'should-be-description')
