from django.db import models
from django.contrib.auth.models import User
from .validators import validate_file_extension_xml, validate_file_extension_docx, validate_file_extension_csv

#id_facility = models.ManyToManyField(Facility)

# Create your models here.
# class XML(models.Model):
#     file = models.FileField(upload_to="documents/%Y/%m/%d", validators=[validate_file_extension_xml])


# class DOCX(models.Model):
#     file = models.FileField(upload_to="documents/%Y/%m/%d", validators=[validate_file_extension_docx])

# class CSV(models.Model):
#     file = models.FileField(upload_to="documents/%Y/%m/%d", validators=[validate_file_extension_csv])


class Track(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name


class PrimaryAuthor(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default="")
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.user.get_full_name()


class CoAuthor(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default="")
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.user.get_full_name()


class Speaker(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default="")
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.user.get_full_name()


class Abstract(models.Model):
    id = models.AutoField(primary_key=True)
    track = models.ForeignKey(Track, on_delete=models.DO_NOTHING, default="")
    primaryAuthor = models.ManyToManyField(PrimaryAuthor)
    coAuthor = models.ManyToManyField(CoAuthor)
    speaker = models.ForeignKey(Speaker, on_delete=models.DO_NOTHING, default="")
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title
