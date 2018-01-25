# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from bot import BotUpdater


class Command(BaseCommand):
    help = 'Manage telegram bot'

    def add_arguments(self, parser):
        parser.add_argument('--set-webhook', action='store_true',
                            help='Set telegram bot to update its state wia web-hook')

    def handle(self, *args, **options):
        if options.get('set_webhook', None):
            bot = BotUpdater()
            bot.set_webhook()
            self.stderr.write(f'Setting web-hook URL to "{bot.webhook_url}"\n')
        else:
            self.stderr.write(self.help)
