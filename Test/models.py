from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
from django.core.exceptions import ValidationError
# from datetime import datetime, timedelta
from django.utils import timezone

# Create your models here.


def validate_audio_extension(value):
    types = ['audio/mp3', 'audio/wav']
    if value.file.content_type not in types:
        raise ValidationError(u'File not supported')


class Test(models.Model):
    class Meta():
        db_table = "Test"

    id = models.AutoField(primary_key=True)
    test_lesson_number = models.IntegerField(blank=False)
    test_title = models.CharField(max_length=100)
    test_timer = models.IntegerField(blank=True, default=0)
    test_publication_date = models.DateField()
    test_description = models.TextField(blank=True)
    test_author = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.test_title


class Question(models.Model):
    class Meta():
        abstract = True

    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=900, blank=False)
    audio = models.FileField(blank=True, null=True, upload_to="audios/%Y/%m/%d/%H/%M/%S/")
    image = ImageField(blank=True, null=True, upload_to="images/%Y/%m/%d/%H/%M/%S/")

    def set_id(self):
        current_id_variant = 0
        current_id_answer = 0
        increment = 0
        if QuestionWithVariants.objects.exists():
            current_id_variant = QuestionWithVariants.objects.latest("id").id
            increment = 1
        if QuestionWithAnswer.objects.exists():
            current_id_answer = QuestionWithAnswer.objects.latest("id").id
            increment = 1
        new_id = max(current_id_answer, current_id_variant) + increment
        return new_id


class QuestionWithAnswer(Question):
    class Meta():
        db_table = "Question_with_answer"

    id = models.AutoField(primary_key=True)
    question_answer = models.CharField(max_length=500, null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not (QuestionWithAnswer.objects.filter(id=self.id).exists()):
            self.id = self.set_id()
        super(QuestionWithAnswer, self).save()


class QuestionWithVariants(Question):
    class Meta():
        db_table = "Question_with_variants"

    id = models.AutoField(primary_key=True)
    question_variants = models.CharField(max_length=1000, blank=False)
    question_with_one_answer = models.BooleanField(default=0)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not (QuestionWithVariants.objects.filter(id=self.id).exists()):
            self.id = self.set_id()
        super(QuestionWithVariants, self).save()


class UsersAnswers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question_id = models.PositiveIntegerField(blank=False, default=1)
    question_text = models.CharField(max_length=300)
    user_answer = models.CharField(max_length=1000 * 1000, blank=True, null=True)

    def __str__(self):
        user_answer_promo = self.user.username + ' / ' + self.test.test_title + ' / ' + self.question_text + ' / '
        user_answer_promo += str(self.user_answer) if self.user_answer else 'None'
        return user_answer_promo


class Hint(models.Model):
    defined_word = models.CharField(max_length=100)
    hint = models.TextField(max_length=2000)

    def __str__(self):
        return self.defined_word

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.defined_word = self.defined_word.lower()
        super(Hint, self).save()


class Results(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE)

    # first_test_result = models.CharField(blank=True, max_length=100)
    # first_test_result_description = models.TextField(blank=True, max_length=100)
    #
    # second_test_result = models.CharField(blank=True, max_length=100)
    # second_test_result_description = models.TextField(blank=True, max_length=100)
    #
    # third_test_result = models.CharField(blank=True, max_length=100)
    # third_test_result_description = models.TextField(blank=True, max_length=100)
    #
    # fourth_test_result = models.CharField(blank=True, max_length=100)
    # fourth_test_result_description = models.TextField(blank=True, max_length=100)
    #
    # fifth_test_result = models.CharField(blank=True, max_length=100)
    # fifth_test_result_description = models.TextField(blank=True, max_length=100)
    #
    # six_test_result = models.CharField(blank=True, max_length=100)
    # six_test_result_description = models.TextField(blank=True, max_length=100)
    #
    # seventh_test_result = models.CharField(blank=True, max_length=100)
    # seventh_test_result_description = models.TextField(blank=True, max_length=100)
    #
    # eighth_test_result = models.CharField(blank=True, max_length=100)
    # eighth_test_result_description = models.TextField(blank=True, max_length=100)
    #
    # ninth_test_result = models.CharField(blank=True, max_length=100)
    # ninth_test_result_description = models.TextField(blank=True, max_length=100)
    #
    # tenth_test_result = models.CharField(blank=True, max_length=100)
    # tenth_test_result_description = models.TextField(blank=True, max_length=100)
    #
    # eleventh_test_result = models.CharField(blank=True, max_length=100)
    # eleventh_test_result_description = models.TextField(blank=True, max_length=100)
    #
    # twelfth_test_result = models.CharField(blank=True, max_length=100)
    # twelfth_test_result_description = models.TextField(blank=True, max_length=100)
    #
    # thirteenth_test_result = models.CharField(blank=True, max_length=100)
    # thirteenth_test_result_description = models.TextField(blank=True, max_length=100)
    #
    # fourteenth_test_result = models.CharField(blank=True, max_length=100)
    # fourteenth_test_result_description = models.TextField(blank=True, max_length=100)
    #
    # fifteenth_test_result = models.CharField(blank=True, max_length=100)
    # fifteenth_test_result_description = models.TextField(blank=True, max_length=100)

    # whenWasFinished = models.DateField(default=datetime.now())
    #
    # def __str__(self):
    #     return self.user_id.username + ' / ' + self.test_id.test_title


class UserResultTestArchive(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    result = models.TextField(blank=True, max_length=400)
    result_description = models.TextField(blank=True, null=True)
    whenWasFinished = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username + ' / ' + str(self.test.test_lesson_number) + ". "+ self.test.test_title + ' / ' + str(self.whenWasFinished) + ' / ' + str(self.result)


class UserFinalResultArchive(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    final_result_description = models.TextField(blank=True, null=True)
    lastFinishedTestDate = models.DateTimeField(default=None)
    whenWasCalculated = models.DateTimeField()

    def __str__(self):
        return self.user.username + " / " + str(self.whenWasCalculated)
