from django.db import models


class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20, unique=True)
    carrera = models.CharField(max_length=100)
    semestre = models.SmallIntegerField()
    correo = models.CharField(max_length=100)

    class Meta:
        # La tabla se crea a mano con schema.sql, Django solo la usa
        managed = False
        db_table = "estudiante"

    def __str__(self):
        return f"{self.matricula} - {self.nombre}"
