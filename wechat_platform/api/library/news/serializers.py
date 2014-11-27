# -*- coding: utf-8 -*-

import time

from django.core.urlresolvers import reverse
from rest_framework import serializers

from system.library.news.models import LibraryNews


class LibraryNewsListSeriailzer(serializers.ModelSerializer):
    """
    系统素材库 - 图文库 序列化类 (仅限获取列表信息[GET])
    """
    show_cover_pic = serializers.SerializerMethodField('get_show_cover_pic')
    content_url = serializers.SerializerMethodField('get_content_url')
    storage_location = serializers.SerializerMethodField('get_storage_location')
    multi_item = serializers.SerializerMethodField('get_multi_item')
    datetime = serializers.SerializerMethodField('get_datetime')

    def get_show_cover_pic(self, obj):
        if obj.picture:
            return True
        else:
            return False

    def get_content_url(self, obj):
        """
        获取文章访问的绝对路径
        """
        if obj.is_simulated():
            return self.context['view'].request.build_absolute_uri(reverse('news:detail', kwargs={'pk': obj.pk}))
        else:
            return obj.url

    def get_storage_location(self, obj):
        if obj.is_simulated():  # 如果可以以模拟登陆方式发送, 说明图文信息已经存储在本地
            return 'local'
        else:  # 否则图文是存储在远程(无法以模拟登陆方式发送)
            return 'remote'

    def get_multi_item(self, obj):
        multi_item = LibraryNews.manager.get(
            official_account=obj.official_account,
            plugin_iden=obj.plugin_iden,
            root=obj
        )
        multi_item_expander = []
        for item in multi_item:
            multi_item_expander.append({
                'id': item.pk,
                'title': item.title,
                'description': item.description,
                'author': item.author,
                'show_cover_pic': self.get_show_cover_pic(item),
                'picurl': item.picurl,
                'content_url': self.get_content_url(item),
                'from_url': item.from_url,
            })
        multi_item_expander = sorted(multi_item_expander, key=lambda k: k.get('id'))
        return multi_item_expander

    def get_datetime(self, obj):
        return time.strftime('%Y-%m-%d %H:%M', obj.datetime.timetuple())

    class Meta:
        model = LibraryNews
        fields = (
            'id', 'title', 'description', 'author', 'show_cover_pic', 'picurl', 'content_url',
            'from_url', 'storage_location', 'multi_item', 'datetime'
        )
        read_only_fields = ('id', 'title', 'description', 'author', 'picurl', 'from_url')