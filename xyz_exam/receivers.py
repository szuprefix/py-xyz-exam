# -*- coding:utf-8 -*-
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django_szuprefix.common.signals import to_save_version

from . import models, helper

import logging

log = logging.getLogger('django')


@receiver(post_save, sender=models.Answer)
def cal_performance(sender, **kwargs):
    try:
        created = kwargs['created']
        if not created:
            return
        answer = kwargs['instance']
        paper = answer.paper
        performance, created = paper.performances.update_or_create(paper=paper, party=answer.party, user=answer.user)

        stat, created = models.Stat.objects.get_or_create(paper=paper, party=answer.party)
        stat.add_answer(answer)
        # print 'stat'
        stat.save()
    except Exception, e:
        import traceback
        log.error("exam cal_performance with answer %s error:%s", answer.id, traceback.format_exc())

@receiver(post_save, sender=models.Answer)
def save_fault(sender, **kwargs):
    try:
        created = kwargs['created']
        if not created:
            return
        answer = kwargs['instance']
        helper.record_fault(answer)
    except Exception, e:
        import traceback
        log.error("exam save_fault with answer %s error:%s", answer.id, traceback.format_exc())


@receiver(pre_save, sender=models.Paper)
def save_paper_version(sender, **kwargs):
    to_save_version.send_robust(sender, instance=kwargs['instance'])
