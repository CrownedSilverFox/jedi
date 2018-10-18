from django.db import models


class Planet(models.Model):
    name = models.CharField(max_length=20, unique=True)


class Jedi(models.Model):
    name = models.CharField(max_length=20, db_index=True)
    planet = models.ForeignKey(Planet, db_index=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Джедай'
        verbose_name_plural = 'Джедаи'

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.TextField(max_length=300, db_index=True)
    answer = models.CharField(max_length=20, db_index=True)

    class Meta:
        verbose_name_plural = 'Вопросы'
        verbose_name = 'Вопрос'


class PadawanAnswer(models.Model):
    answer = models.CharField(max_length=20, db_index=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Ответы падавана'
        verbose_name = 'Ответ падавана'


class Padawan(models.Model):
    name = models.CharField(max_length=20, db_index=True)
    master = models.ForeignKey(Jedi,
                               verbose_name="Мастер",
                               blank=True,
                               on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    answers = models.ManyToManyField(PadawanAnswer)

    class Meta:
        verbose_name = 'Падаван'
        verbose_name_plural = 'Падаваны'

    def __str__(self):
        return self.name


class Test(models.Model):
    key = models.CharField(max_length=10, unique=True)
    questions = models.ManyToManyField(Question, db_index=True)





