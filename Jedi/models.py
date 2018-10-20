from django.db import models


class Planet(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Jedi(models.Model):
    name = models.CharField(max_length=20, unique=True)
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

    def __str__(self):
        return self.text[:20] + ('...' if len(self.text) > 20 else '')


class Test(models.Model):
    key = models.CharField(max_length=10, unique=True)
    questions = models.ManyToManyField(Question, db_index=True)

    def __str__(self):
        return self.key


class Padawan(models.Model):
    name = models.CharField(max_length=20, db_index=True)
    master = models.ForeignKey(Jedi,
                               verbose_name="Мастер",
                               blank=True,
                               null=True,
                               on_delete=models.CASCADE)
    planet = models.ForeignKey(Planet, db_index=True, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, default=None, null=True, blank=True)

    class Meta:
        verbose_name = 'Падаван'
        verbose_name_plural = 'Падаваны'

    def __str__(self):
        return self.name


class PadawanAnswer(models.Model):
    answer = models.CharField(max_length=20, db_index=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    padawan = models.ForeignKey(Padawan, on_delete=models.CASCADE, default=None)

    class Meta:
        verbose_name_plural = 'Ответы падавана'
        verbose_name = 'Ответ падавана'

    def __str__(self):
        return self.answer
