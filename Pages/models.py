from django.db import models
from Test.models import Hint
import re
from pymorphy2 import MorphAnalyzer

# Create your models here.


class HelpFunctions(models.Model):
    class Meta():
        abstract = True

    def is_hint_need(self, text):
        hints = Hint.objects.all()
        morph = MorphAnalyzer()
        defined_words = [hint.defined_word for hint in hints]
        # print(defined_words)
        normal_defined_words = [morph.normal_forms(hint.defined_word)[0] for hint in hints]
        # print("DEFINED WORDS:", normal_defined_words)
        recognized_words = []
        if type(text) == list:
            text = ','.join(text)
        words_of_text = re.split('\.|,|-|\?|\*| ', text)
        normal_words = [morph.normal_forms(word) for word in words_of_text]
        # print("NORMAL WORDS:", normal_words)
        for list_of_normals in range(len(normal_words)):
            for word in normal_words[list_of_normals]:
                if word in normal_defined_words:
                    recognized_words.append(defined_words[normal_defined_words.index(word)])
        # print("RECOGNIZED WORDS:", recognized_words)
        return recognized_words
