from django.test import TestCase
from django.core.urlresolvers import reverse

import django.contrib.auth.models as auth_models
import django.contrib.contenttypes as contenttypes

from toolkit.index.models import IndexLink, IndexCategory


class SecurityTests(TestCase):
    """Test that write permission is required"""

    def test_private_urls(self):
        """All URLs which should 302 redirect to the login page"""
        views_to_test = {
            'toolkit-index': {},
            'create-index-link': {},
            'update-index-link': {'pk': '1'},
            'delete-index-link': {'pk': '1'},
            'create-index-category': {},
            'update-index-category': {'pk': '1'},
        }
        for view_name, kwargs in views_to_test.iteritems():
            url = reverse(view_name, kwargs=kwargs)
            expected_redirect = "{0}?next={1}".format(reverse("django.contrib.auth.views.login"), url)

            # Test GET:
            response = self.client.get(url)
            self.assertRedirects(response, expected_redirect)

            # Test POST:
            response = self.client.post(url)
            self.assertRedirects(response, expected_redirect)


class TestViews(TestCase):
    # Fairly incomplete set of tests, but good enough

    def setUp(self):
        cat1 = IndexCategory(name="Category 1 Links!")
        cat1.save()

        cat2 = IndexCategory(name="Category 2 Links!")
        cat2.save()

        cat3 = IndexCategory(name="Sad, empty category")
        cat3.save()

        l1 = IndexLink(text="Link one", link="http://link1.test.com/")
        l1.category = cat1
        l1.save()

        l2 = IndexLink(text="Two Link", link="http://cubecinema.com/")
        l2.category = cat2
        l2.save()

        l3 = IndexLink(text="THIRD LINK", link="http://cubecinema.com/blah-de-blah")
        l3.category = cat2
        l3.save()

        # System user:
        user_rw = auth_models.User.objects.create_user('admin', 'toolkit_admin@localhost', 'T3stPassword!')
        # Create dummy ContentType:
        ct = contenttypes.models.ContentType.objects.get_or_create(
            model='',
            app_label='toolkit'
        )[0]
        # Create 'write' permission:
        write_permission = auth_models.Permission.objects.get_or_create(
            name='Write access to all toolkit content',
            content_type=ct,
            codename='write'
        )[0]
        # Give "admin" user the write permission:
        user_rw.user_permissions.add(write_permission)

        # And login:
        self.assertTrue(self.client.login(username="admin", password="T3stPassword!"))

    def tearDown(self):
        self.client.logout()

    def test_get_index(self):
        url = reverse("toolkit-index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('toolkit_index.html')

    def test_edit_link(self):
        url = reverse("update-index-link", kwargs={"pk": "1"})
        response = self.client.post(url, data={
            'text': 'All new link text!',
            'link': 'http://boring.com/',
            'category': '2',
        })
        self.assertRedirects(response, reverse("toolkit-index"))

        link = IndexLink.objects.get(id=1)
        self.assertEqual(link.text, 'All new link text!')
        self.assertEqual(link.link, 'http://boring.com/')
        self.assertEqual(link.category_id, 2)

    def test_edit_category(self):
        url = reverse("update-index-category", kwargs={"pk": "1"})
        response = self.client.post(url, data={
            'name': 'Category is called what, now?',
        })
        self.assertRedirects(response, reverse("toolkit-index"))

        cat = IndexCategory.objects.get(id=1)
        self.assertEqual(cat.name, 'Category is called what, now?')

    def test_edit_category_invalid_name_blank(self):
        url = reverse("update-index-category", kwargs={"pk": "1"})
        response = self.client.post(url, data={
            'name': '   ',
        })
        self.assertEqual(response.status_code, 200)
        # For whatever reason, this doesn't work correctly:
        # self.assertFormError(response, 'form', 'name', u'Name cannot be blank')
        self.assertContains(response, u'Name cannot be blank')

        cat = IndexCategory.objects.get(id=1)
        self.assertEqual(cat.name, 'Category 1 Links!')

    def test_edit_category_invalid_name_missing(self):
        url = reverse("update-index-category", kwargs={"pk": "1"})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', u'This field is required.')

        cat = IndexCategory.objects.get(id=1)
        self.assertEqual(cat.name, 'Category 1 Links!')
