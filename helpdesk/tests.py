import base64  # for decoding base64 image
import re
from decimal import Decimal
from io import BytesIO

from django.contrib.auth.models import AnonymousUser, User, Group
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse

from core.views import dashboard, live_dashboard
from helpdesk.models import Queue, QueueQuestion, make_secret, Ticket, TicketUpdate
from .forms import TicketForm, TicketManageForm
from .views import ticket_crete, ticket_detail, ticket_add, ticket_edit, load_questions, ticket_list_all, ticket_feed, \
    ticket_list_todo, ticket_list_processing, ticket_list_done, ticket_comment, ticket_list_closed, ticket_list_resolved


class HelpdeskTestCase(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.client = Client()

        image_thumb = '''R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'''.strip()
        self.image = InMemoryUploadedFile(
            BytesIO(base64.b64decode(image_thumb)),  # use io.BytesIO
            field_name='tempfile',
            name='tempfile.png',
            content_type='image/png',
            size=len(image_thumb),
            charset='utf-8',
        )

        # Queue
        self.queue_cnc = Queue.objects.create(title='Teste Router CNC',
                                              description='Um fila de tickets para testes',
                                              image=str(self.image))

        # Queue Questions and Problems
        self.queue_cnc_question_01 = QueueQuestion.objects.create(question='Máquina não liga',
                                                                  queue=self.queue_cnc)
        self.queue_cnc_question_02 = QueueQuestion.objects.create(question='A Máquina não se movimenta',
                                                                  queue=self.queue_cnc)
        self.queue_cnc_question_03 = QueueQuestion.objects.create(question='Alarme no Software',
                                                                  queue=self.queue_cnc)
        self.queue_cnc_question_04 = QueueQuestion.objects.create(question='Spindle não Gira',
                                                                  queue=self.queue_cnc)

        # Ticket
        self.ticket_non_customer = Ticket.objects.create(queue=self.queue_cnc,
                                                         problems=[self.queue_cnc_question_03,
                                                                   self.queue_cnc_question_04],
                                                         submitter_name='Non Customer',
                                                         submitter_company='New Company',
                                                         submitter_phone='(11) 12213-0987',
                                                         submitter_email='non@foo.bar')

        # Staff user
        self.user_staff = User.objects.create_user(username='jacob', email='jacob@…', password='top_secret')
        self.group = Group.objects.create(name='Testes')
        self.group.user_set.add(self.user_staff)

    def test_retorno_queue_title(self):
        queue = Queue.objects.first()

        self.assertEquals(queue.__str__(), queue.title)
        self.assertEquals(queue.title, 'Teste Router CNC')

    def test_retorno_queue_question_title(self):
        questions = QueueQuestion.objects.filter(queue=self.queue_cnc)
        questions_expected = ['Máquina não liga', 'A Máquina não se movimenta',
                              'Alarme no Software', 'Spindle não Gira']

        self.assertEqual(len(questions), 4)
        self.assertIn(questions[0].__str__(), questions_expected)

    def test_make_secret_for_non_logged_user_view(self):
        secret = make_secret()

        uuid_valid_format = re.compile(r'^[a-z0-9\-]{36}$')

        self.assertIsNotNone(uuid_valid_format.match(secret))
        self.assertEqual(len(secret), 36)

    def test_public_view_ticket_create_step_one_status_code(self):
        request = self.factory.get('/ticket/create/')
        request.user = AnonymousUser()

        response = ticket_crete(request)
        self.assertEqual(response.status_code, 200)

    def test_public_view_ticket_create_step_one_content(self):
        request = self.factory.get('/ticket/create/')
        request.user = AnonymousUser()

        response = ticket_crete(request)
        self.assertContains(response, 'Teste Router CNC')

    def test_public_view_ticket_create_step_two_status_code(self):
        request = self.factory.get('/ticket/create/new/')
        request.user = AnonymousUser()

        response = self.client.post('/ticket/create/new/', data={'maquina': self.queue_cnc})
        self.assertEqual(response.status_code, 200)

    def test_public_view_ticket_create_step_two_content(self):
        request = self.factory.get('/ticket/create/new/')
        request.user = AnonymousUser()

        response = self.client.post('/ticket/create/new/', data={'maquina': self.queue_cnc})
        self.assertContains(response, 'Máquina não liga')

    def test_public_view_new_ticket_create_final_step(self):
        new_ticket_data = {
            'queue': self.queue_cnc,
            'name': 'Benjamin',
            'company': 'Dharma',
            'mobile': '(11) 12345-6789',
            'email': 'ben@dharma.org',
            'cliente': '',
            'problemas': [self.queue_cnc_question_01, self.queue_cnc_question_03, 'Outros'],
            'outros problemas': 'Mais um problema',
        }

        open_tickets = Ticket.objects.all()
        self.assertEqual(len(open_tickets), 1)

        response = self.client.post(reverse('public_ticket_create'), data=new_ticket_data)
        self.assertEqual(response.status_code, 200)

        open_tickets = Ticket.objects.all()
        self.assertEqual(len(open_tickets), 2)

        new_ticket_data_customer_default_problem = {
            'queue': self.queue_cnc,
            'name': 'Michel',
            'company': 'Opus',
            'mobile': '(12) 22342-6229',
            'email': 'michel@opus.net',
            'cliente': 'on',
            'problemas': [self.queue_cnc_question_02],
        }

        response = self.client.post(reverse('public_ticket_create'), data=new_ticket_data_customer_default_problem)
        self.assertEqual(response.status_code, 200)

        open_tickets = Ticket.objects.all()
        self.assertEqual(len(open_tickets), 3)

    def test_public_view_ticket_detail_status_code(self):
        email = self.ticket_non_customer.submitter_email
        secret = self.ticket_non_customer.secret_key
        request = self.factory.get(f'ticket/{email}/{secret}/')
        request.user = AnonymousUser()

        response = ticket_detail(request, email=email, secret=secret)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Non Customer')

    def test_view_for_ticket_create_by_staff_with_non_logged_user(self):
        self.client.logout()
        response = self.client.get(reverse('ticket_add'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             '/accounts/login/?next=/ticket/add/',
                             status_code=302,
                             target_status_code=200)

    def test_view_for_ticket_create_by_staff_user_logged_status_code(self):
        request = self.factory.get(reverse('ticket_add'))
        request.user = self.user_staff

        response = ticket_add(request)
        self.assertEqual(response.status_code, 200)

    def test_ticket_form_is_valid(self):
        form_data = {
            'queue': self.queue_cnc,
            'problems': [self.queue_cnc_question_01, self.queue_cnc_question_03, 'Outros'],
            'submitter_name': 'Nazir',
            'submitter_company': 'iwAtz',
            'submitter_phone': '(15) 4242-1337',
            'submitter_email': 'nazir@rizan.foo',
            'status': 1,
            'priority': 3,
            'tecnico_pre_diagnostico': self.user_staff,
            'tecnico_de_campo': self.user_staff,
            'is_customer': '',
            'customer_code': '',
            'need_paper': '',
            'resolution_report': '',
        }
        form = TicketForm(data=form_data)
        self.assertEqual(form.is_valid(), True)

    def test_ticket_form_invalid(self):
        invalid_form_data = {
            'queue': 'Errado',
            'problems': 'Inválido',
            'submitter_name': 'Nazir',
            'submitter_company': 'iwAtz',
            'submitter_phone': '(15) 4242-1337',
            'submitter_email': 'nazir@rizan.foo',
            'status': 'Inválido',
            'priority': 'ops',
            'tecnico_pre_diagnostico': self.user_staff,
            'tecnico_de_campo': self.user_staff,
            'is_customer': '',
            'customer_code': '',
            'need_paper': '',
            'resolution_report': '',
        }
        form = TicketForm(data=invalid_form_data)
        self.assertEqual(form.is_valid(), False)

    def test_ticket_manage_form(self):
        invalid_form_data = {
            'status': 'Errado',
            'priority': 'Inválido',
            'tecnico_pre_diagnostico': 'Nazir',
            'tecnico_de_campo': 'iwAtz',
            'is_customer': '(15) 4242-1337',
            'customer_code': 'nazir@rizan.foo',
            'order': 'Inválido',
            'losses': 'ops',
            'need_paper': '',
            'resolution_report': '',
        }
        form = TicketManageForm(data=invalid_form_data)
        self.assertEqual(form.is_valid(), False)

    def test_add_ticket_by_staff(self):
        tickets = Ticket.objects.all()
        self.assertEqual(len(tickets), 1)

        new_ticket_data_by_staff = {
            'queue': self.queue_cnc.pk,
            'problems': [self.queue_cnc_question_01, self.queue_cnc_question_03, 'Outros'],
            'outros problemas': 'Teste de outro',
            'submitter_name': 'Nazir',
            'submitter_company': 'iwAtz',
            'submitter_phone': '(15) 4242-1337',
            'submitter_email': 'nazir@rizan.foo',
            'status': 1,
            'priority': 3,
            'tecnico_pre_diagnostico': self.user_staff.pk,
            'tecnico_de_campo': self.user_staff.pk,
            'is_customer': '',
            'customer_code': '',
            'need_paper': '',
            'resolution_report': '',
        }

        self.client.force_login(self.user_staff)

        response = self.client.post(reverse('ticket_add'), data=new_ticket_data_by_staff)
        self.assertEqual(response.status_code, 302)

        tickets = Ticket.objects.all()
        self.assertEqual(len(tickets), 2)

        new_ticket_data_by_staff_no_extra_problem = {
            'queue': self.queue_cnc.pk,
            'problems': [self.queue_cnc_question_01, self.queue_cnc_question_03],
            'submitter_name': 'Rizan',
            'submitter_company': 'zTAwi',
            'submitter_phone': '(51) 3342-1337',
            'submitter_email': 'rizan@narin.foo',
            'status': 2,
            'priority': 4,
            'tecnico_pre_diagnostico': self.user_staff.pk,
            'tecnico_de_campo': self.user_staff.pk,
            'is_customer': '',
            'customer_code': '',
            'need_paper': '',
            'resolution_report': '',
        }

        response = self.client.post(reverse('ticket_add'), data=new_ticket_data_by_staff_no_extra_problem)
        self.assertEqual(response.status_code, 302)

        tickets = Ticket.objects.all()
        self.assertEqual(len(tickets), 3)

    def test_ticket_update_by_staff(self):
        ticket = self.ticket_non_customer
        self.assertEqual(ticket.submitter_name, 'Non Customer')
        self.assertEqual(ticket.is_customer, False)
        self.assertEqual(ticket.customer_code, None)
        self.assertEqual(ticket.order, None)
        self.assertEqual(ticket.losses, 0)

        new_ticket_data = {
            'submitter_name': ticket.submitter_name,
            'submitter_company': ticket.submitter_company,
            'submitter_phone': ticket.submitter_phone,
            'submitter_email': ticket.submitter_email,
            'status': 1,
            'priority': 4,
            'tecnico_pre_diagnostico': self.user_staff.pk,
            'tecnico_de_campo': self.user_staff.pk,
            'is_customer': True,
            'customer_code': 666,
            'order': 999,
            'losses': 1904.93,
            'resolution_report': '',
        }

        request = self.factory.post(reverse('ticket_edit', kwargs={'pk': ticket.pk}), new_ticket_data)
        request.user = self.user_staff

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = ticket_edit(request, pk=ticket.pk)
        ticket.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(ticket.submitter_name, 'Non Customer')
        self.assertEqual(ticket.is_customer, True)
        self.assertEqual(ticket.customer_code, '666')
        self.assertEqual(ticket.order, '999')
        self.assertEqual(ticket.losses, Decimal('1904.9300000000'))

        self.client.force_login(self.user_staff)
        response = self.client.get(reverse('ticket_edit', kwargs={'pk': self.ticket_non_customer.pk}))
        self.assertEqual(response.status_code, 200)

        form = TicketManageForm(instance=ticket)
        self.assertEqual(form.instance, self.ticket_non_customer)

        request = self.factory.get('/')
        request.user = self.user_staff

        response = dashboard(request)
        self.assertContains(response, 'R$ 1.904,93')

        request = self.factory.get('live/')
        request.user = self.user_staff

        response = live_dashboard(request)
        self.assertContains(response, 'R$ 1.904,93')

    def test_ticket_update_by_staff_with_erro_in_form(self):
        ticket = self.ticket_non_customer

        wrong_ticket_data = {
            'submitter_name': '',
            'submitter_company': '',
            'submitter_phone': '',
            'submitter_email': '',
            'status': 'Status errado',
            'priority': 'Aqui deve ser inteiro',
            'tecnico_pre_diagnostico': self.user_staff.pk,
            'tecnico_de_campo': self.user_staff.pk,
            'is_customer': True,
            'customer_code': 666,
            'order': 999,
            'losses': 0,
            'resolution_report': '',
        }

        wrong_request = self.factory.post(reverse('ticket_edit', kwargs={'pk': ticket.pk}), wrong_ticket_data)
        wrong_request.user = self.user_staff

        setattr(wrong_request, 'session', 'session')
        messages = FallbackStorage(wrong_request)
        setattr(wrong_request, '_messages', messages)

        response = ticket_edit(wrong_request, pk=ticket.pk)
        ticket.refresh_from_db()

        form = TicketManageForm(instance=ticket, data=wrong_ticket_data)
        self.assertFalse(form.is_valid())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<ul class="errorlist">')

    def test_load_questions_returns(self):
        request = self.factory.get(reverse('load_questions'), data={'queue': self.queue_cnc.pk})
        request.user = self.user_staff

        response = load_questions(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.queue_cnc_question_01)

    def test_ticket_list_all_view_non_logged_user(self):
        request = self.factory.get('/tickets/')
        request.user = AnonymousUser()

        response = ticket_list_all(request)
        self.assertEqual(response.status_code, 302)

    def test_ticket_list_all_view_staff_user(self):
        request = self.factory.get('/tickets/')
        request.user = self.user_staff

        response = ticket_list_all(request)
        self.assertEqual(response.status_code, 200)

    def test_ticket_list_todo_view_non_logged_user(self):
        request = self.factory.get('/tickets/todo/')
        request.user = AnonymousUser()

        response = ticket_list_todo(request)
        self.assertEqual(response.status_code, 302)

    def test_ticket_list_todo_view_staff_user(self):
        request = self.factory.get('/tickets/todo/')
        request.user = self.user_staff

        response = ticket_list_todo(request)
        self.assertEqual(response.status_code, 200)

    def test_ticket_list_processing_view_non_logged_user(self):
        request = self.factory.get('/tickets/processing/')
        request.user = AnonymousUser()

        response = ticket_list_processing(request)
        self.assertEqual(response.status_code, 302)

    def test_ticket_list_processing_view_staff_user(self):
        request = self.factory.get('/tickets/processing/')
        request.user = self.user_staff

        response = ticket_list_processing(request)
        self.assertEqual(response.status_code, 200)

    def test_ticket_list_done_view_non_logged_user(self):
        request = self.factory.get('/tickets/done/')
        request.user = AnonymousUser()

        response = ticket_list_done(request)
        self.assertEqual(response.status_code, 302)

    def test_ticket_list_done_view_staff_user(self):
        request = self.factory.get('/tickets/done/')
        request.user = self.user_staff

        response = ticket_list_done(request)
        self.assertEqual(response.status_code, 200)

    def test_ticket_list_closed_view_non_logged_user(self):
        request = self.factory.get('/tickets/closed/')
        request.user = AnonymousUser()

        response = ticket_list_closed(request)
        self.assertEqual(response.status_code, 302)

    def test_ticket_list_closed_view_staff_user(self):
        request = self.factory.get('/tickets/closed/')
        request.user = self.user_staff

        response = ticket_list_closed(request)
        self.assertEqual(response.status_code, 200)

    def test_ticket_list_resolved_view_non_logged_user(self):
        request = self.factory.get('/tickets/resolved/')
        request.user = AnonymousUser()

        response = ticket_list_resolved(request)
        self.assertEqual(response.status_code, 302)

    def test_ticket_list_resolved_view_staff_user(self):
        request = self.factory.get('/tickets/resolved/')
        request.user = self.user_staff

        response = ticket_list_resolved(request)
        self.assertEqual(response.status_code, 200)

    def test_ticket_list_feed_non_logged_user(self):
        request = self.factory.get('tickets/ajax/feed/')
        request.user = AnonymousUser()

        response = ticket_feed(request)
        self.assertEqual(response.status_code, 302)

    def test_ticket_list_feed_staff_user(self):
        request = self.factory.get('tickets/ajax/feed/')
        request.user = self.user_staff

        response = ticket_feed(request)
        self.assertEqual(response.status_code, 200)

    def test_ticket_comment_non_logged_user(self):
        request = self.factory.get('tickets/comment/<pk>/')
        request.user = AnonymousUser()

        response = ticket_comment(request)
        self.assertEqual(response.status_code, 302)

    def test_ticket_comment_staff_user(self):
        ticket = self.ticket_non_customer
        tickets_updates = TicketUpdate.objects.all()
        self.assertEqual(len(tickets_updates), 0)

        new_comment = {
            'update_ticket_pk': ticket.pk,
            'update_title': 'Test comment title',
            'update_comment': 'um comentário de teste'
        }

        request = self.factory.post(reverse('ticket_comment', kwargs={'pk': ticket.pk}), new_comment)
        request.user = self.user_staff

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = ticket_comment(request, pk=ticket.pk)
        self.assertEqual(response.status_code, 302)

        tickets_updates = TicketUpdate.objects.all()
        self.assertEqual(len(tickets_updates), 1)

    def test_view_ticket_json_dashboard_context_non_logged_user(self):
        request = self.client.get(reverse('json_dashboard_context'))
        self.assertEqual(request.status_code, 302)

    def test_view_ticket_json_dashboard_context_logged_user(self):
        self.client.force_login(self.user_staff)
        request = self.client.get(reverse('json_dashboard_context'))

        self.assertEqual(request.status_code, 200)

    def test_tickets_tables_builder_non_logged_user(self):
        request = self.client.get(reverse('tickets_tables_builder'))
        self.assertEqual(request.status_code, 302)

    def test_tickets_tables_builder_logged_user(self):
        self.client.force_login(self.user_staff)
        request = self.client.get(reverse('tickets_tables_builder'))
        self.assertEqual(request.status_code, 200)
