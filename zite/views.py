
from logging import getLogger
import json

from django.views.generic import View, ListView, CreateView, FormView
from material.frontend.views import CreateModelView
from django.http import HttpResponse

from zite.forms import *
from zite.models import *
from bot import BotUpdater

# __all__ = ['BidView', 'BotWebHook', 'ButtonSetListView']

logger = getLogger('default')


# class ButtonSetListView(ListView):
#     model = ButtonSet


# class ItemsView(ListView):
#     model = Item
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         logger.info('Hello info')
#         logger.warning('Hello warn')
#         return super(ItemsView, self).get_context_data(object_list=object_list, **kwargs)


# class BidView(CreateModelView):
#     from material.base import Layout, Row, Fieldset
#     from material.widgets import SelectDateWidget
#
#     model = Bid
#     # form_class = BidForm
#     template_name = 'zite/bid_form.html'
#     title = 'Оформление заказа'
#     layout = Layout(
#         Row('item_url'),
#         Row('date'),
#         Row('phone')
#     )
#
#     def has_add_permission(self, request):
#         # allow all
#         return True


class BotWebHook(View):
    def post(self, request):
        json_request = json.loads(request.body.decode())
        # logger.info(f'Web-hook POST data: "{json_request}"')
        BotUpdater().webhook(json_request)
        return HttpResponse('POST OK')

    def get(self, request):
        # logger.info(f'Direct GET-request to web-hook URL. {self} {request}')
        return HttpResponse('GET OK')
