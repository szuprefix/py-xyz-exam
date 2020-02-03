# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals

from xyz_restful.mixins import IDAndStrFieldSerializerMixin
from rest_framework import serializers
from . import models


class PaperSerializer(IDAndStrFieldSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Paper
        fields = '__all__'
        read_only_fields = ('user', 'questions_count')


class PaperListSerializer(PaperSerializer):
    class Meta(PaperSerializer.Meta):
        exclude = ('content_object', 'content')
        read_only_fields = ('user', 'questions_count')


class AnswerSerializer(IDAndStrFieldSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = '__all__'
        read_only_fields = ('user',)


class AnswerListSerializer(AnswerSerializer):
    class Meta(AnswerSerializer.Meta):
        fields = ['paper', 'user', 'std_score', 'seconds', 'create_time']


class StatSerializer(IDAndStrFieldSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Stat


class PerformanceSerializer(IDAndStrFieldSerializerMixin, serializers.ModelSerializer):
    paper_name = serializers.CharField(source="paper", label='试卷', read_only=True)
    user_name = serializers.CharField(source="user.get_full_name", label='学生', read_only=True)

    class Meta:
        model = models.Performance
        fields = '__all__'
        read_only_fields = ['paper', 'user']


class FaultSerializer(IDAndStrFieldSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Fault
        fields = '__all__'
