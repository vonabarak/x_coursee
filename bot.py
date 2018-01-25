# -*- coding: utf-8 -*-

from telegram import Bot, error
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram.update import Update
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from telegram.replykeyboardremove import ReplyKeyboardRemove
from telegram.keyboardbutton import KeyboardButton

from zite import models

import logging
import pprint
from django.conf import settings
from django.core.cache import caches

logger = logging.getLogger('default')
pp = pprint.PrettyPrinter(indent=2, width=80)

cache = caches['commands']


class BotUpdater:
    def __init__(self):
        self.token = settings.TELEGRAM_BOT['token']
        self.webhook_url = settings.TELEGRAM_BOT['webhook_url']
        self.bot = Bot(token=self.token)
        self.dispatcher = Dispatcher(self.bot, None, workers=0)
        self.dispatcher.logger = logger

        self.dispatcher.add_handler(CommandHandler('start',     self.start, pass_args=True))
        # self.dispatcher.add_handler(CommandHandler('article',   self.article, pass_args=True))
        # self.dispatcher.add_handler(CommandHandler('menu',      self.menu, pass_args=True))
        self.dispatcher.add_handler(CommandHandler('test',      self.test))

        self.dispatcher.add_handler(CallbackQueryHandler(self.inlinekbdhandler))

        # self.dispatcher.add_handler(MessageHandler(
        #     filters=filters.Filters.status_update.new_chat_members,
        #     callback=self.greetings
        # ))

        userlist = [i. id for i in models.User.objects.all()]

        for user_id in userlist:
            cached_command = cache.get(user_id, None)
            if cached_command is not None:
                self.dispatcher.add_handler(MessageHandler(
                    filters=filters.Filters.user(user_id=user_id),
                    callback=getattr(self, cached_command)
                ))
        #         self.dispatcher.add_handler(
        #             MessageHandler(
        #                 filters=filters.Filters.user(user_id=user_id),
        #                 callback=callback
        #             )
        #         )

    def webhook(self, json):
        update = Update.de_json(json, self.bot)
        self.dispatcher.process_update(update)

    def set_webhook(self):
        self.bot.setWebhook(self.webhook_url)

    def msg(self, user, text):
        self.bot.send_message(chat_id=user.tgid, text=text)

    # CALLBACKS

    @staticmethod
    def greetings(bot, update):
        # models.ButtonSet.objects.first().callback(bot, update)
        article_buttons = [
            InlineKeyboardButton(i.title, callback_data=f'menu {i.pk}')
            for i in models.Category.objects.filter(main_menu=True)
        ]
        grouped_article_buttons = [article_buttons[i:i + 2] for i in range(0, len(article_buttons), 2)]
        inline_buttons = InlineKeyboardMarkup(
            grouped_article_buttons +
            [[InlineKeyboardButton('☘️ Старт ', url=f'https://t.me/{settings.TELEGRAM_BOT["name"]}?start')]]
        )
        for user in update.message.new_chat_members:
            bot.sendMessage(
                chat_id=update.message.chat_id,
                text=f'**Привет, {user.username}!**',
                reply_markup=inline_buttons,
                parse_mode='Markdown'
            )

    @staticmethod
    def article(bot, update, args):
        if not args:
            return bot.sendMessage(
                text='Укажите номер статьи через пробел: /article 1',
                chat_id=update.message.chat_id,
            )
        try:
            articles = models.Article.objects.filter(pk__in=args)
            if not articles:
                bot.sendMessage(
                    text=f'Нет такого',
                    chat_id=update.message.chat_id,
                )
            for a in articles:
                a.callback(bot, update)
        except models.Article.DoesNotExist:
            bot.sendMessage(
                text=f'Нет такого: {args}',
                chat_id=update.message.chat_id,
            )
        except ValueError:
            bot.sendMessage(
                text=f'Нужно указывать номер',
                chat_id=update.message.chat_id,
            )

    @staticmethod
    def menu(bot, update, args):
        if not args:
            return bot.sendMessage(
                text='Укажите номер меню через пробел: /menu 1',
                chat_id=update.message.chat_id,
            )
        try:
            articles = models.Category.objects.filter(pk__in=args)
            if not articles:
                _all = [str(i.pk) for i in models.Category.objects.all()]
                bot.sendMessage(
                    text=f'Нет такого. Есть {",".join(_all)}',
                    chat_id=update.message.chat_id,
                )
            for a in articles:
                a.callback(bot, update)
        except models.Category.DoesNotExist:
            bot.sendMessage(
                text=f'Нет такого: {args}',
                chat_id=update.message.chat_id,
            )
        except ValueError:
            bot.sendMessage(
                text=f'Нужно указывать номер',
                chat_id=update.message.chat_id,
            )

    @staticmethod
    def start(bot, update, args):
        logger.warning(str(args))
        if args and args[0]:
            args_tuple = args[0].split('-')
            command = args_tuple[0]
            parameters = args_tuple[1:]

        models.User.from_tg(update.message.from_user)

        article_buttons = [
            InlineKeyboardButton(i.title, callback_data=f'{i.get_callback_data()} send')
            for i in models.Category.objects.filter(main_menu=True)
        ]
        grouped_article_buttons = [article_buttons[i:i + 2] for i in range(0, len(article_buttons), 2)]
        inline_buttons = InlineKeyboardMarkup(grouped_article_buttons)

        bot.sendMessage(
            chat_id=update.message.chat_id,
            text='Привет!',
            reply_markup=inline_buttons,
        )


    def inlinekbdhandler(self, bot, update):
        tup = update.callback_query.data.split()

        model = getattr(models, tup[0]).objects.get(pk=tup[1])
        callback = getattr(model, tup[2])
        callback(bot, update)

        # bot.sendMessage(
        #     text=f'{pp.pformat(update.to_json())}\n\n{dir(update)}\n\n{update.effective_message}',
        #     chat_id=update.callback_query.from_user.id,
        #     # parse_mode='Markdown'
        # )
        bot.answerCallbackQuery(
            update.callback_query.id,
            text=update.callback_query.data
        )

    @staticmethod
    def test(bot, update):
        # buttons = ReplyKeyboardMarkup([
        #     [KeyboardButton('Телефон', request_contact=True), KeyboardButton('Локация', request_location=True)],
        # ])
        bot.sendMessage(
            text=pp.pformat(update.to_json()),
            chat_id=update.message.chat_id,
            reply_markup=ReplyKeyboardRemove(),
            # parse_mode='Markdown'
        )
