import re

from django.test import TestCase, RequestFactory, Client

from helpdesk.models import Queue, QueueQuestion, make_secret


class HelpdeskTestCase(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.client = Client()

        # Queue
        self.queue_cnc = Queue.objects.create(title='Teste Router CNC')

        # Queue Questions and Problems
        self.queue_cnc_question_01 = QueueQuestion.objects.create(question='Máquina não liga',
                                                                  queue=self.queue_cnc)
        self.queue_cnc_question_02 = QueueQuestion.objects.create(question='A Máquina não se movimenta',
                                                                  queue=self.queue_cnc)
        self.queue_cnc_question_03 = QueueQuestion.objects.create(question='Alarme no Software',
                                                                  queue=self.queue_cnc)
        self.queue_cnc_question_04 = QueueQuestion.objects.create(question='Spindle não Gira',
                                                                  queue=self.queue_cnc)

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
