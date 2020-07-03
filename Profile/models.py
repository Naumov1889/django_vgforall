from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import validate_comma_separated_integer_list
from django.contrib.auth.models import User
from Test.models import Test, UserResultTestArchive
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta


# import datetime

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.CharField(max_length=10, default="", blank=True, null=True)
    city_of_residence = models.CharField(max_length=30, default="", blank=True, null=True)
    country_of_residence = models.CharField(max_length=30, default="", blank=True, null=True)
    sex = models.CharField(max_length=7, default="", blank=True, null=True)
    available_tests = models.CharField(max_length=1000, validators=[validate_comma_separated_integer_list], blank=True, null=True)
    finished_tests = models.CharField(max_length=1000, validators=[validate_comma_separated_integer_list], blank=True, null=True)
    activation_salt = models.CharField(max_length=30, default="none", blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_integer_finished_tests(self):
        integers_finished_tests = []
        finished_tests = self.finished_tests
        string_finished_tests = finished_tests.split(",")
        if len(string_finished_tests) == 1 and '' in string_finished_tests:
            return integers_finished_tests
        else:
            integers_finished_tests = [int(id_elem) for id_elem in string_finished_tests]
            return integers_finished_tests

    def reset_tests(self):
        self.finished_tests = ""
        self.save()

    def reset_test(self, current_test_id):
        new_finished_tests = []
        finished_tests = self.finished_tests
        if not self.finished_tests:
            finished_tests = ''
        string_finished_tests = finished_tests.split(",")
        for test in string_finished_tests:
            if test == current_test_id:
                continue
            else:
                new_finished_tests.append(test)

        self.finished_tests = ",".join(new_finished_tests)
        self.save()

    def add_finished_test(self, new_finished_test):
        if self.finished_tests == "":
            self.finished_tests = self.finished_tests + str(new_finished_test)
        else:
            self.finished_tests = self.finished_tests + "," + str(new_finished_test)

    def get_available_passed_tests(self):
        tests = Test.objects.all()
        available_tests = []
        passed_tests = []

        for test in tests.iterator():
            test_object = UserResultTestArchive.objects.filter(user=self.user, test=test).order_by(
                '-whenWasFinished').first()

            if test_object:
                passed_tests.append(test.id)
                when_available = test_object.whenWasFinished + timedelta(seconds=30)
                if when_available < datetime.now():
                    available_tests.append(test.id)
            else:
                available_tests.append(test.id)

        return available_tests, passed_tests

    # Creating a custom method
    def save_profile_n_user(self):
        self.user.save()
        self.save()

    def delete_user(self):
        self.user.delete()


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.profile = Profile.objects.create(user=instance)
    instance.profile.save()



class Callback(models.Model):
    name = models.CharField(max_length=50, verbose_name="Имя")
    email = models.CharField(max_length=120, blank=True, verbose_name="Почта")
    text = models.TextField(verbose_name="Вопрос")

    def __str__(self):
        return self.name + " / " + self.email

    class Meta(object):
        verbose_name = "Запрос на обратную связь"
        verbose_name_plural = "Запросы на обратную связь"