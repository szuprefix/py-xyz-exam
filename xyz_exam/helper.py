# -*- coding:utf-8 -*-
from __future__ import division, unicode_literals

__author__ = 'denishuang'
import re
from xyz_util.datautils import strQ2B
from . import models, choices


def distrib_count(d, a):
    a = str(a)
    counts = d.setdefault('counts', {})
    percents = d.setdefault('percents', {})
    counts[a] = counts.setdefault(a, 0) + 1
    tc = sum(counts.values())
    cas = [(int(float(k)), v) for k, v in counts.iteritems()]
    cas.sort()
    s = 0
    for k, v in cas:
        s += v
        percents[str(k)] = s / float(tc)
    d['count'] = tc
    return d


def answer_is_empty(a):
    if isinstance(a, (list, tuple)):
        return not any(a)
    return not a


def answer_equal(standard_answer, user_answer):
    if len(standard_answer) != len(user_answer):
        return False
    l = zip(standard_answer, user_answer)
    return all([b in a.split('|') for a, b in l])


RE_MULTI_ANSWER_SPLITER = re.compile(r"[|()、]")


def split_answers(s):
    if isinstance(s, (list, tuple)):
        return s
    return RE_MULTI_ANSWER_SPLITER.split(strQ2B(s))


"""
In [36]: answer_match(['A|C','B','C','D'],['C','B'],True)
Out[36]: 0.5

In [37]: answer_match(['A','B','C','D'],['C','B'])
Out[37]: 0.5

In [38]: answer_match(['A','B','C','D'],['B'])
Out[38]: 0.25

In [39]: answer_match(['A','B','C','D'],['B'],True)
Out[39]: 0.0

In [40]: answer_match(['A','B','C','D'],['B','E'])
Out[40]: 0.0

In [41]: answer_match(['A','B','C','D'],['B','A','D','C'])
Out[41]: 1.0
"""


def answer_match(standard_answer, user_answer, one_by_one=False):
    sa = standard_answer
    ua = user_answer
    lsa = len(sa)
    lua = len(ua)
    if lua > lsa:
        return -1
    l = zip(sa[:lua], ua)
    c = 0
    for s, u in l:
        if one_by_one:
            if u in split_answers(s):
                c += 1
        else:
            if u in sa:
                c += 1
            else:
                c = 0
                break
    return c / lsa


def extract_fault(answer):
    m = dict([(a['number'], a) for a in answer.detail if not (answer_is_empty(a['userAnswer']) or a['right'])])
    p = answer.paper.content_object
    rs = []
    for g in p['groups']:
        for q in g['questions']:
            qnum = q['number']
            q['group'] = dict(title=g.get('title'), memo=g.get('memo'), number=g.get('number'))
            if qnum in m:
                rs.append((q, m[qnum]))
    return rs


def record_fault(answer):
    user = answer.user
    paper = answer.paper

    fs = extract_fault(answer)
    nums = [a['number'] for a in answer.detail]
    models.Fault.objects.filter(user=answer.user, paper=answer.paper).exclude(question_id__in=nums).update(
        is_active=False)
    for question, qanswer in fs:
        question_id = question['number']
        lookup = dict(user=user, paper=paper, question_id=question_id)
        fault = models.Fault.objects.filter(**lookup).first()
        if not fault:
            models.Fault.objects.create(
                question=question,
                question_type=choices.MAP_QUESTION_TYPE.get(question['type']),
                detail=dict(lastAnswer=qanswer), **lookup
            )
        else:
            fault.times += 1
            fault.detail['last_answer'] = qanswer
            fault.corrected = False
            fault.question = question
            fault.is_active = True
            fault.question_type = choices.MAP_QUESTION_TYPE.get(question['type'])
            from datetime import datetime
            fault.create_time = datetime.now()
            rl = fault.detail.setdefault('result_list', [])
            rl.append(False)
            fault.save()


def restruct_fault(paper):
    import textdistance
    jws = textdistance.JaroWinkler()

    qtm = {}
    from copy import deepcopy
    gs = deepcopy(paper.content_object.get('groups'))
    nums = []
    for g in gs:
        for q in g.get('questions'):
            q['group'] = dict(title=g.get('title'), memo=g.get('memo'), number=g.get('number'))
            qtm[q.get('title')] = q
            nums.append(q.get('number'))
    models.Fault.objects.filter(paper=paper).exclude(question_id__in=nums).update(is_active=False)
    bm = {True: [], False: []}
    for f in paper.faults.all():
        q = f.question
        t1 = q.get('title')
        tp1 = t1.split('题】')[-1]
        qn = None
        mdl = 0.8
        for t2 in qtm.keys():
            tp2 = t2.split('题】')[-1]
            dl = jws.similarity(tp1, tp2)
            if dl > mdl:
                qn = qtm.get(t2)
                mdl = dl
        if not qn:
            bm[False].append(f.id)
            f.is_active = False
            f.save()
            continue
        t2 = qn.get('title')
        if t1 != t2 or q.get('options') != qn.get('options') or q.get('answer') != qn.get('answer') or q.get('explanation') != qn.get('explanation'):
            bm[True].append(f.id)
            f.question = qn
            f.save()
    return bm


def cal_correct_straight_times(rl):
    c = 0
    for i in range(len(rl) - 1, -1, -1):
        if not rl[i]:
            break
        c += 1
    return c
