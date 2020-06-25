# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from . import models
from django_szuprefix.utils import statutils


def detail_group_stat(qset, measure):
    r = {}
    for a in qset:
        statutils.group_stat(a.detail, ['number', measure], r, list_action='seperate')
    return r


def sort_by(a):
    if a['stat']['right']:
        return a['stat']['right'].get(True, 0) / (1 + a['stat']['right'].get(False))

def stats_paper(qset=None, measures=None, period=None):
    qset = qset if qset is not None else models.Paper.objects.all()
    qset = statutils.using_stats_db(qset)
    dstat = statutils.DateStat(qset, 'create_time')
    funcs = {
        'all': lambda: qset.count(),
        'tags': lambda : statutils.count_by(qset, 'tags')
    }
    return dict([(m, funcs[m]()) for m in measures])

def stats_answer(qset=None, measures=None, period=None):
    qset = qset if qset is not None else models.Answer.objects.all()
    qset = statutils.using_stats_db(qset)
    dstat = statutils.DateStat(qset, 'create_time')
    funcs = {
        'today': lambda: dstat.stat("今天", count_field="user_id", distinct=True, only_first=True),
        'yesterday': lambda: dstat.stat("昨天", count_field="user_id", distinct=True, only_first=True),
        'all': lambda: qset.values("user_id").distinct().count(),
        'count': lambda: dstat.get_period_query_set(period).count(),
        'daily': lambda: dstat.stat(period, count_field='user_id', distinct=True),
        'clazz': lambda: statutils.count_by(
            dstat.get_period_query_set(period),
            'user__as_school_student__clazz__name',
            count_field='user_id',
            distinct=True, sort="-"),
        'course': lambda: statutils.count_by_generic_relation(
            dstat.get_period_query_set(period),
            "paper__course_course__name",
            count_field='user_id',
            distinct=True, sort="-"),
        'chapter': lambda: statutils.count_by_generic_relation(
            dstat.get_period_query_set(period),
            "paper__course_chapter__name",
            count_field='user_id',
            distinct=True, sort="-"),
        'student': lambda: statutils.count_by(
            dstat.get_period_query_set(period),
            "user__as_school_student__clazz__name,user__as_school_student__name"),
        'student_course': lambda: statutils.count_with_generic_relation(
            dstat.get_period_query_set(period),
            "user__as_school_student__clazz__name,user__as_school_student__name,paper__owner",
            trans_map={'course.chapter': ['course__name']}),
        'right': lambda: detail_group_stat(dstat.get_period_query_set(period), 'right'),
        'userAnswer': lambda: detail_group_stat(dstat.get_period_query_set(period), 'userAnswer'),
    }
    return dict([(m, funcs[m]()) for m in measures])


def stats_fault(qset=None, measures=None, period=None):
    qset = qset if qset is not None else models.Fault.objects.all()
    qset = statutils.using_stats_db(qset)
    dstat = statutils.DateStat(qset, 'update_time')
    funcs = {
        'today': lambda: dstat.stat("今天", count_field="user_id", distinct=True, only_first=True),
        'count': lambda: dstat.get_period_query_set(period).count(),
        'all': lambda: qset.values("user_id").distinct().count(),
        'allCount': lambda: qset.count()
    }
    return dict([(m, funcs[m]()) for m in measures])

