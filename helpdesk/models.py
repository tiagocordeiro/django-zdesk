import uuid

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.text import slugify

from core.models import Active, TimeStampedModel


class Queue(Active, TimeStampedModel):
    """
    Uma fila é uma coleção de tickets para o que geralmente seriam áreas ou
    departamentos de negócios.
    Por exemplo, uma empresa pode ter uma fila para cada Produto fornecido,
    ou uma fila para cada uma das Contas, Pré-Vendas e Suporte.

    A queue is a collection of tickets into what would generally be business
    areas or departments.
    For example, a company may have a queue for each Product they provide, or
    a queue for each of Accounts, Pre-Sales, and Support.
    """

    title = models.CharField('Title', max_length=100)

    description = models.TextField('Description')

    slug = models.SlugField('Slug', max_length=50, unique=True, blank=True, null=True,
                            help_text='This slug is used when building ticket IDs.'
                                      'Once set, try not to change it or e-mailing may get messy.')

    image = models.ImageField(upload_to='queue/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)

        super(Queue, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = 'Queue'
        verbose_name_plural = 'Queues'


class QueueQuestion(Active, TimeStampedModel):
    """
    Um item na base de conhecimento, problemas e perguntas frequentes.
    As perguntas vinculadas a uma Queue são usadas para gerar o fomulário de novo ticket.
    """
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE, verbose_name='Queue')
    order = models.PositiveIntegerField('ordem', default=0)
    question = models.CharField('Question', max_length=256,
                                help_text='Pergunta para formulário de abertura de tickets')

    def __str__(self):
        return self.question

    class Meta:
        ordering = ('queue', 'order')
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


def make_secret():
    return str(uuid.uuid4())


class Ticket(Active, TimeStampedModel):
    """
    Para permitir a entrada de um ticket o mais rápido possível, apenas o
    campos mínimos simples são obrigatórios. Isso basicamente nos permite
    classifique e gerencie o ticket. O usuário sempre pode voltar e
    insira mais informações posteriormente.

    Um bom exemplo disso é quando um cliente está ao telefone e
    você deseja fornecer a eles um ID do ticket o mais rápido possível. Você pode
    insira algumas informações básicas, salve o ticket, forneça o ID ao cliente
    desligue o telefone e adicione mais detalhes posteriormente
    (quando o cliente não estiver na linha).

    Observe que assign_to é opcional - tickets não atribuídos são exibidos em
    o painel para solicitar aos usuários que se apropriem deles.

    To allow a ticket to be entered as quickly as possible, only the
    bare minimum fields are required. These basically allow us to
    sort and manage the ticket. The user can always go back and
    enter more information later.

    A good example of this is when a customer is on the phone, and
    you want to give them a ticket ID as quickly as possible. You can
    enter some basic info, save the ticket, give the customer the ID
    and get off the phone, then add in further detail at a later time
    (once the customer is not on the line).

    Note that assigned_to is optional - unassigned tickets are displayed on
    the dashboard to prompt users to take ownership of them.
    """
    OPEN_STATUS = 1
    REOPENED_STATUS = 2
    RESOLVED_STATUS = 3
    CLOSED_STATUS = 4
    DUPLICATE_STATUS = 5

    STATUS_CHOICES = (
        (OPEN_STATUS, 'Open'),
        (REOPENED_STATUS, 'Reopened'),
        (RESOLVED_STATUS, 'Resolved'),
        (CLOSED_STATUS, 'Closed'),
        (DUPLICATE_STATUS, 'Duplicate'),
    )

    PRIORITY_CHOICES = (
        (1, '1. Critical'),
        (2, '2. High'),
        (3, '3. Normal'),
        (4, '4. Low'),
        (5, '5. Very Low'),
    )

    queue = models.ForeignKey(Queue, on_delete=models.CASCADE, verbose_name='Queue')

    problems = ArrayField(models.CharField(max_length=200), blank=True)

    submitter_name = models.CharField('Contact name', max_length=50, blank=True, null=True)

    submitter_company = models.CharField('Company', max_length=50, blank=True, null=True)

    submitter_phone = models.CharField('Phone number', max_length=16, blank=True, null=True)

    submitter_email = models.EmailField('Submitter E-Mail', blank=True, null=True,
                                        help_text='The submitter will receive an email for all public '
                                                  'follow-ups left for this task.')

    status = models.IntegerField('Status', choices=STATUS_CHOICES, default=OPEN_STATUS)

    priority = models.IntegerField('Priority', choices=PRIORITY_CHOICES, default=3, blank=3,
                                   help_text='1 = Highest Priority, 5 = Low Priority')

    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_to',
                                    blank=True, null=True, verbose_name='Assigned to')

    tecnico_pre_diagnostico = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                                related_name='tecnico_pre_diagnostico', blank=True, null=True,
                                                verbose_name='Técnico pré diagnóstico')

    tecnico_de_campo = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                         related_name='tecnico_de_campo', blank=True, null=True,
                                         verbose_name='Técnico de campo')

    is_customer = models.BooleanField('É cliente', default=False)

    customer_code = models.CharField('Código do cliente', max_length=6, blank=True, null=True)

    order = models.CharField('Código do pedido', max_length=10, blank=True, null=True)

    need_paper = models.BooleanField('Tem papel', default=False)

    resolution_report = models.TextField('Relatório final', blank=True, null=True,
                                         help_text='The resolution provided to the customer by our staff.')

    secret_key = models.CharField("Secret key needed for viewing/editing ticket by non-logged in users",
                                  max_length=36,
                                  default=make_secret)


class TicketUpdate(Active, TimeStampedModel):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name='Ticket')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='user', blank=True, null=True,
                             verbose_name='Usuário')
    title = models.CharField('Título', max_length=100, blank=True, null=True)
    comment = models.TextField('Comentário', blank=True, null=True)
    public = models.BooleanField('Público', blank=True, null=True, default=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Update'
        verbose_name_plural = 'Updates'
