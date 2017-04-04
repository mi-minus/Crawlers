#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 chaoqiankeji.com, Inc. All Rights Reserved
#

"""
File: models.py
Author: minus(minus@stu.xjtu.edu.cn)
Date: 2016-12-26 12:36
Project: TestPy
"""
import mongoengine
from mongoengine import *
from mongoengine.context_managers import switch_db
import datetime

DATA_TYPE = (0, 1, 2, 3, 4, 5, 6)
IS_RUN = (0, 1)

# meta = {
#     'shard_key': ('machine', 'timestamp',)
# }

# class Page(Document):
#     title = StringField(max_length=200, required=True)
#     pt_time = DateTimeField(default=datetime.datetime.now)
#     html = FileField()
#     meta = {'collection': 'page'}

class PostQuerySet(QuerySet):

    def get_posts_by_topics(self):
        return self.order_by('topic_id', 'pt_time')

    def get_posts_by_sites(self):
        return self.order_by('site_id', 'pt_time')

    def get_posts_by_sites_topics(self):
        return self.order_by('site_id','topic_id', 'pt_time')

    def get_posts_by_datatype(self, datatype):
        return self(data_type=datatype)

class Datatype_name(Document):
    data_type = IntField(required=True, unique=True)
    datatype_name = StringField(required=True, max_length=16, unique=True)

class Poster(EmbeddedDocument):
    home_url = StringField(max_length=512)
    img_url = StringField(max_length=512)
    id = StringField(max_length=64)
    name = StringField(max_length=64)

class Post(Document):
    _id = ObjectIdField(primary_key=True)
    url = StringField(required=True, max_length=512, unique=True)
    site_id = IntField(required=True)
    site_name = StringField(max_length=64)
    topic_id = IntField(required=False, default=0)
    board = StringField(max_length=200)
    data_type = IntField(required=True, choices=DATA_TYPE)
    title = StringField(max_length=500)
    content = StringField(max_length=2048)
    html = FileField()
    pt_time = DateTimeField(required=True)
    st_time = DateTimeField(default=datetime.datetime.now)
    read_num = IntField(default=0)
    comm_num = IntField(default=0)
    img_url = StringField(max_length=512)
    repost_num = IntField(default=0)
    lan_type = IntField(default=0)
    is_read = IntField(default=0)
    repost_pt_id = StringField(required=False)
    text_type = IntField(required=False)
    poster = EmbeddedDocumentField(Poster)

    meta = {
        'ordering': ['pt_time'], # 默认的　objects()
        'collection': 'post',
        'shard_key': ('site_id', 'topic_id', 'pt_time'),
        'queryset_class': PostQuerySet,
        'indexes':[
            'topic_id',
            'pt_time',
            '$title',   # text index
            ('data_type', 'site_id'),  # 复合index
        ]
    }

class Topic(Document):
    _id = IntField(required=True, primary_key=True)
    topic_name = StringField(required=True, max_length=64)
    topic_kws = ListField(StringField(), default=list)
    user_id = IntField(required=True, unique_with='topic_name')
    user_name = StringField(required=True, max_length=32)

    meta = {
        'ordering': ['_id'],
        'collection': 'topic'
    }

class Site(Document):
    _id = IntField(required=True, primary_key=True)
    site_name = StringField(required=True, max_length=64, unique_with='_id')
    site_url = URLField(required=True)
    data_type = IntField(required=True, choices=DATA_TYPE)
    position = IntField(default=0)
    is_run = IntField(default=0, choices=IS_RUN)

    meta = {
        'ordering': ['_id'],
        'collection': 'site'
    }

class Site_topic(Document):
    site_id = IntField(required=True)
    topic_id = IntField(required=True)
    topic_name = StringField(required=True, max_length=64)
    topic_kws = ListField(StringField(), default=list)
    user_id = IntField(required=True, unique_with=['site_id', 'topic_id'])
    user_name = StringField(required=True, max_length=32)

    meta = {
        'ordering': ['site_id'],
        'collection': 'site_topic'
    }
