
import telegram
from telegram.update import Update
from telegram.error import TelegramError
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup

from django.conf import settings
from django.db import models

__all__ = ['Button', 'Photo', 'Article', 'Category', 'User', 'Service', 'ArticleMark']


class User(models.Model):
    id = models.BigIntegerField(primary_key=True)
    is_bot = models.BooleanField(default=False)
    first_name = models.CharField(max_length=512)
    last_name = models.CharField(max_length=512, null=True, blank=True)
    username = models.CharField(max_length=512, null=True, blank=True)
    language_code = models.CharField(max_length=512, null=True, blank=True)

    @classmethod
    def from_tg(cls, user: telegram.User):
        u, _ = cls.objects.get_or_create(id=user.id)
        for field in cls._meta.fields:
            setattr(u, field.name, getattr(user, field.name))
        u.save()
        return u

    def __str__(self):
        return self.first_name


class Button(models.Model):
    text = models.CharField(max_length=128)
    command = models.SlugField(max_length=32)
    # callback_data = models.CharField(max_length=128, null=True, blank=True)
    # switch_inline_query = models.CharField(max_length=128, null=True, blank=True)
    # switch_inline_query_current_chat = models.CharField(max_length=128, null=True, blank=True)
    # callback_game =
    # pay = models.NullBooleanField(null=True, blank=True)

    @property
    def url(self):
        return f'https://t.me/{settings.TELEGRAM_BOT["name"]}?{self.command}'

    def __str__(self):
        return self.text


class Photo(models.Model):
    title = models.CharField(max_length=128)
    image = models.ImageField()

    def __str__(self):
        return self.title


class Sendable:
    pk = 'stub'

    def get_markup(self) -> InlineKeyboardMarkup:
        raise NotImplemented()

    def get_text(self) -> str:
        raise NotImplemented()

    def callback(self, bot: telegram.Bot, update: Update):
        from logging import getLogger
        logger = getLogger('default')

        try:
            chat_id = update.message.chat_id
        except (AttributeError, KeyError):
            chat_id = update.effective_user.id

        try:
            bot.sendMessage(
                chat_id=chat_id,
                text=self.get_text(),
                reply_markup=self.get_markup(),
                parse_mode='Markdown'
            )
        except TelegramError as e:
            logger.exception(
                f'An exception occured in dynamically generated callback for sendable #{self.pk}: {e}')


class Article(models.Model, Sendable):
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    menu = models.ForeignKey('Category',
                             related_name='articles', null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=256)
    text = models.TextField(null=True, blank=True)
    photos = models.ManyToManyField(Photo, related_name='articles', blank=True)
    main_menu = models.BooleanField(default=False)

    def get_text(self):
        photo_links = '\n'.join([f'[{i.title}](https://x-coursee.com{i.image.url})' for i in self.photos.all()])
        return f'**{self.title}**\n{self.text}\n{photo_links}'

    def get_markup(self):
        likes = ArticleMark.objects.filter(article=self, mark=1).count()
        dislikes = ArticleMark.objects.filter(article=self, mark=-1).count()
        return InlineKeyboardMarkup([[
            InlineKeyboardButton(text=f'👍{likes}',    callback_data=f'{self.get_callback_data()} like'),
            InlineKeyboardButton(text=f'👎{dislikes}', callback_data=f'{self.get_callback_data()} dislike'),
        ]])

    def like(self, bot, update):
        ArticleMark.objects.create(
            user=User.from_tg(update.callback_query.from_user),
            article=self,
            mark=1
        )
        bot.editMessageReplyMarkup(
            chat_id=update.effective_message.chat_id,
            message_id=update.effective_message.message_id,
            reply_markup=self.get_markup(),
        )

    def dislike(self, bot, update):
        ArticleMark.objects.create(
            user=User.from_tg(update.callback_query.from_user),
            article=self,
            mark=-1
        )
        bot.editMessageReplyMarkup(
            chat_id=update.effective_message.chat_id,
            message_id=update.effective_message.message_id,
            reply_markup=self.get_markup(),
        )

    def get_callback_data(self):
        return f'{self.__class__.__name__} {self.pk}'

    def send(self, bot, update):
        bot.editMessageText(
            text=self.get_text(),
            chat_id=update.effective_message.chat_id,
            message_id=update.effective_message.message_id,
            reply_markup=self.get_markup(),
            parse_mode='Markdown'
        )
        # bot.sendMessage(
        #     text=self.get_text(),
        #     chat_id=update.callback_query.from_user.id,
        #     reply_markup=self.get_markup(),
        #     parse_mode='Markdown'
        # )

    def __str__(self):
        return self.title


class ArticleMark(models.Model):
    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
    #     unique_together = (('user', 'article'), )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    mark = models.SmallIntegerField(choices=(
        (1, 'like'),
        (-1, 'dislike'),
    ))

    def __str__(self):
        return f'{self.user.first_name} {self.get_mark_display()} "{self.article}"'


class Service(Article):
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    # def get_markup(self):
    #     return InlineKeyboardMarkup([[
    #         InlineKeyboardButton(text='Назад', callback_data=f'menu {self.menu_id}'),
    #         InlineKeyboardButton(text='Начало', callback_data='start'),
    #     ]])


class ServiceReview(models.Model):
    class Meta:
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзыв'

    ctime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Article, on_delete=models.CASCADE)
    mark = models.PositiveSmallIntegerField(choices=(
        (1, '⭐️'),
        (2, '⭐⭐️'),
        (3, '⭐️⭐⭐'),
        (4, '⭐⭐️⭐⭐️'),
        (5, '⭐⭐️⭐⭐⭐️'),
    ))
    review = models.TextField()


class Category(Article):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_markup(self):

        article = [InlineKeyboardButton(
                    text=i.title,
                    callback_data=f'{i.get_callback_data()} send'
                ) for i in self.articles.all()]
        grouped_article = [article[i:i + 2] for i in range(0, len(article), 2)]
        return InlineKeyboardMarkup(grouped_article)
