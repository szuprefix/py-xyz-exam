# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals

TYPE_EXERCISE = 1
TYPE_QUIZ = 2

CHOICES_TYPE = (
    (TYPE_EXERCISE, '练习'),
    (TYPE_QUIZ, '测验')
)

QUESTION_TYPE_SINGLE = 1
QUESTION_TYPE_MULTIPLE = 2
QUESTION_TYPE_INPUT = 3
QUESTION_TYPE_TEXTAREA = 4

CHOICES_QUESTION_TYPE = (
    (QUESTION_TYPE_SINGLE, '单选'),
    (QUESTION_TYPE_MULTIPLE, '多选'),
    (QUESTION_TYPE_INPUT, '填空'),
    (QUESTION_TYPE_TEXTAREA, '主观')
)

MAP_QUESTION_TYPE = {
    'single': QUESTION_TYPE_SINGLE,
    'multiple': QUESTION_TYPE_MULTIPLE,
    'input': QUESTION_TYPE_INPUT,
    'textarea': QUESTION_TYPE_TEXTAREA
}
