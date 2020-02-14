import base64  # for decoding base64 image
import tempfile  # for setting up tempdir for media
from io import BytesIO

from django.contrib.auth.models import AnonymousUser, User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import RequestFactory, TestCase, Client, override_settings
from django.urls import reverse

from .admin import CompanyAdmin, CustomUserAdmin
from .models import UserProfile, Company
from .views import dashboard, profile_edit


class DashboardViewTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.client = Client()

        # User account
        self.user_admin = User.objects.create_user(username='jacob', email='jacob@…', password='top_secret')

        self.company = Company.objects.create(name='My Business',
                                              address='FooBar street, with no number',
                                              phone='(11) 1234-5678',
                                              website='https://www.foobar.com',
                                              facebook='https://www.foobar.com',
                                              instagram='https://www.foobar.com')

    def test_company_name_return_str(self):
        company = Company.objects.get(name=self.company.name)
        self.assertEqual(company.__str__(), self.company.name)

    def test_company_admin_add_company_return_false(self):
        request = reverse('admin:core_company_changelist')
        has_add_permission = CompanyAdmin.has_add_permission(self.company, request)
        self.assertEqual(has_add_permission, False)

    def test_returns_true_when_no_business_data_exists(self):
        self.company.delete()

        request = reverse('admin:core_company_changelist')
        has_add_permission = CompanyAdmin.has_add_permission(self.company, request)
        self.assertEqual(has_add_permission, True)

    def test_custom_user_profile_admin(self):
        request = reverse('admin:auth_user_change', args={self.user_admin})
        get_inline_instances = CustomUserAdmin.get_inline_instances(self.user_admin, request)
        self.assertEqual(get_inline_instances, [])

    def test_dashboard_anonimo(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()

        response = dashboard(request)
        self.assertEqual(response.status_code, 302)

    def test_dashboard_logado(self):
        request = self.factory.get('/')
        request.user = self.user_admin

        response = dashboard(request)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_content(self):
        request = self.factory.get('/')
        request.user = self.user_admin

        response = dashboard(request)
        self.assertContains(response, 'Total de prejuízo')

    def test_live_dashboard_anonimo(self):
        request = self.factory.get('live/')
        request.user = AnonymousUser()

        response = dashboard(request)
        self.assertEqual(response.status_code, 302)

    def test_live_dashboard_logado(self):
        request = self.factory.get('live/')
        request.user = self.user_admin

        response = dashboard(request)
        self.assertEqual(response.status_code, 200)

    def test_live_dashboard_content(self):
        request = self.factory.get('live/')
        request.user = self.user_admin

        response = dashboard(request)
        self.assertContains(response, 'Total de prejuízo')


class ProfileUpdateViewTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.client = Client()

        # User support
        self.user_support = User.objects.create_user(username='john', email='john@…', password='top_secret')

        # User Profile Staff
        image_thumb = '''
                R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7
                '''.strip()

        self.image = InMemoryUploadedFile(
            BytesIO(base64.b64decode(image_thumb)),  # use io.BytesIO
            field_name='tempfile',
            name='tempfile.png',
            content_type='image/png',
            size=len(image_thumb),
            charset='utf-8',
        )

        self.user_profile_support = UserProfile.objects.create(user=self.user_support, avatar=str(self.image))

    def test_profile_edit_anonimo(self):
        request = self.factory.get('/profile/')
        request.user = AnonymousUser()

        response = profile_edit(request)
        self.assertEqual(response.status_code, 302)

    def test_profile_edit_logado(self):
        request = self.factory.get('/profile/')
        request.user = self.user_support

        response = profile_edit(request)
        self.assertEqual(response.status_code, 200)

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_user_profile_edit_name(self):
        data = {
            'first_name': 'Joe',
            'last_name': 'Forest',
            'email': 'joe@foo.bar',
            'userprofile-TOTAL_FORMS': 1,
            'userprofile-INITIAL_FORMS': 1,
            'userprofile-MIN_NUM_FORMS': 0,
            'userprofile-MAX_NUM_FORMS': 1,
            'userprofile-0-id': self.user_profile_support.id,
            'userprofile-0-user': self.user_support.id,
        }

        self.client.force_login(self.user_support)
        request = self.client.get('/profile/')

        self.assertEqual(request.status_code, 200)

        response = self.client.post('/profile/', data=data, instance=self.user_support)

        self.user_support.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user_support.first_name, 'Joe')
