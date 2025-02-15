from tortoise import Tortoise, fields, models


class Patient(models.Model):
    id = fields.IntField(pk=True)
    nom = fields.CharField(max_length=100)
    diagnostics = fields.ReverseRelation["Diagnostic"]

class Docteur(models.Model):
    nom = fields.CharField(max_length=100)
    patients = fields.ReverseRelation["Patient"]

class Diagnostic(models.Model):
    contenu = fields.JSONField()
    questions = fields.JSONField()
    patient = fields.ForeignKeyField('models.Patient', related_name='diagnostics')
    genre = fields.CharField(max_length=100)
