# -*- coding:utf-8 -*-
from __future__ import division
from xyz_util.statutils import do_rest_stat_action, using_stats_db
from xyz_restful.mixins import UserApiMixin, BatchActionMixin
from . import models, serializers, stats
from rest_framework import viewsets, decorators, response
from xyz_restful.decorators import register


@register()
class PaperViewSet(UserApiMixin, BatchActionMixin, viewsets.ModelViewSet):
    queryset = models.Paper.objects.all()
    serializer_class = serializers.PaperSerializer
    search_fields = ('title',)
    filter_fields = {
        'id': ['in', 'exact'],
        'owner_id': ['exact', 'in'],
        'is_active': ['exact'],
        'title': ['exact'],
        # 'is_break_through': ['exact'],
        'owner_type': ['exact'],
        'tags': ['exact'],
        'content': ['contains'],
        'create_time': ['range']
    }
    ordering_fields = ('is_active', 'title', 'create_time', 'questions_count')

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PaperListSerializer
        return super(PaperViewSet, self).get_serializer_class()

    @decorators.list_route(['POST'])
    def batch_active(self, request):
        return self.do_batch_action('is_active', True)

    @decorators.list_route(['get'])
    def stat(self, request):
        return do_rest_stat_action(self, stats.stats_paper)

    @decorators.detail_route(['GET', 'POST'])
    def image_signature(self, request, pk):
        from xyz_qcloud.cos import gen_signature
        return response.Response(gen_signature(allow_prefix='/exam/paper/%s/images/*' % self.get_object().id))

    @decorators.list_route(['GET'])
    def ids(self, request):
        qset = self.filter_queryset(self.get_queryset()).values_list('id', flat=True)
        return response.Response({'ids': list(qset)})


@register()
class AnswerViewSet(UserApiMixin, viewsets.ModelViewSet):
    queryset = models.Answer.objects.all()
    serializer_class = serializers.AnswerSerializer
    filter_fields = ('paper', 'user')

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.AnswerListSerializer
        return super(AnswerViewSet, self).get_serializer_class()

    @decorators.list_route(['get'])
    def stat(self, request):
        return do_rest_stat_action(self, stats.stats_answer)


@register()
class StatViewSet(UserApiMixin, viewsets.ReadOnlyModelViewSet):
    queryset = models.Stat.objects.all()
    serializer_class = serializers.StatSerializer
    filter_fields = ('paper',)


@register()
class PerformanceViewSet(UserApiMixin, viewsets.ReadOnlyModelViewSet):
    queryset = using_stats_db(models.Performance.objects.all())
    serializer_class = serializers.PerformanceSerializer
    filter_fields = {
        'paper': ['exact', 'in'],
        'user': ['exact']
    }
    search_fields = ('paper__title', 'user__first_name')
    ordering_fields = ('score', 'update_time')


@register()
class FaultViewSet(UserApiMixin, BatchActionMixin, viewsets.ModelViewSet):
    queryset = models.Fault.objects.all()
    serializer_class = serializers.FaultSerializer
    filter_fields = {
        'paper': ['exact', 'in'],
        'question_id': ['exact'],
        'question_type': ['exact'],
        'corrected': ['exact'],
        'is_active': ['exact'],
        'user': ['exact'],
        'paper__owner_type': ['exact'],
        'paper__owner_id': ['exact'],
        'create_time': ['range']
    }
    ordering_fields = ['times', 'update_time']

    @decorators.list_route(['get'])
    def stat(self, request):
        return do_rest_stat_action(self, stats.stats_fault)

    @decorators.detail_route(['patch'])
    def redo(self, request, pk):
        fault = self.get_object()
        rl = fault.detail.setdefault('result_list', [])
        right = request.data['right']
        rl.append(right)
        if not right:
            fault.times += 1
        fault.save()
        return response.Response(self.get_serializer(instance=fault).data)

    @decorators.list_route(['patch'])
    def batch_correct(self, request):
        from datetime import datetime
        return self.do_batch_action('corrected', True, extra_params=dict(update_time=datetime.now()))


@register()
class ExamViewSet(BatchActionMixin, viewsets.ModelViewSet):
    queryset = models.Exam.objects.all()
    serializer_class = serializers.ExamSerializer
    search_fields = ('name',)
    filter_fields = {
        'name': ['exact', 'in'],
        'is_active': ['exact', 'in'],
        'owner_type': ['exact'],
        'owner_id': ['exact', 'in'],
        'begin_time': ['gte', 'lte']
    }

    @decorators.list_route(['POST'])
    def batch_active(self, request):
        return self.do_batch_action('is_active', True)
