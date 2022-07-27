from django.db import models

# Create your models here.
class Professor(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return '%s' % (self.name)


class Module(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return '%s' % (self.name)


class ModuleInstance(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    professor = models.ManyToManyField(Professor)
    year = models.IntegerField()
    semester = models.IntegerField()

    def __str__(self):
        return '%s, %s, %s, %s' % (self.module.name, self.professor.name, self.year, self.semester)


class Ratings(models.Model):
    moduleInstance = models.ForeignKey(ModuleInstance, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return '%s, %s, %s, %s, %s' % (
            self.moduleInstance.module.name, self.professor.name, self.moduleInstance.year,
            self.moduleInstance.semester, self.rating)
