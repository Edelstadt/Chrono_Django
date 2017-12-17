from django.core.exceptions import ValidationError
from django.db import models


class Author(models.Model):
    surname = models.CharField(verbose_name=("Author surname"), max_length=50)
    lastname = models.CharField(verbose_name=("Author lastname"), max_length=50)

    def __str__(self):
        return self.lastname


class Book(models.Model):
    title = models.CharField(verbose_name=("Book title"), max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, )
    year = models.PositiveIntegerField(verbose_name=("Publication year"))
    isbn = models.PositiveIntegerField(verbose_name=("ISBN"), blank=True, null=True)
    publisher = models.CharField(verbose_name=("Publisher"), max_length=50)
    place_publish = models.CharField(verbose_name=("Place publish"), max_length=50)

    def __str__(self):
        return self.title


class URL(models.Model):
    author = models.ForeignKey(Author, blank=True, null=True,
                               on_delete=models.CASCADE, )
    page_title = models.CharField(verbose_name=("Page title"), max_length=50)
    web_title = models.CharField(verbose_name=("Web title"), max_length=50)
    url = models.URLField(verbose_name=("URL"))
    date_visit = models.DateField(verbose_name=("Date visit"))
    date_citate = models.DateField(verbose_name=("Date visit"))

    def __str__(self):
        return self.page_title


class Name(models.Model):
    LANGUAGE_CHOICES = (
        ('CS', 'Czech'),
        ('DE', 'German'),
        ('LAT', 'Latin'),
    )
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='CS')
    name = models.CharField(max_length=50, verbose_name=("Name"))

    def __str__(self):
        return self.name


class Since(models.Model):
    century = models.PositiveIntegerField(blank=True, null=True)
    year = models.PositiveIntegerField(blank=True, null=True)
    date = models.DateField(verbose_name="Date", blank=True, null=True)


class Until(models.Model):
    century = models.PositiveIntegerField(blank=True, null=True)
    year = models.PositiveIntegerField(blank=True, null=True)
    date = models.DateField(verbose_name="Date", blank=True, null=True)


class Saint(models.Model):
    VENERATED_CHOICES = (
        ('CAT', 'Catholic'),
        ('ORT', 'Orthodoxy'),
    )
    names = models.ManyToManyField(Name, related_name="saint_name")
    source_book = models.ManyToManyField(Book, verbose_name=("Source book"), blank=True)
    source_url = models.ManyToManyField(URL, verbose_name=("Source book"), blank=True)
    since = models.ForeignKey(Since, on_delete=models.CASCADE, blank=True, null=True)
    until = models.ForeignKey(Until, blank=True, null=True, on_delete=models.CASCADE, )
    venerated = models.CharField(max_length=3, choices=VENERATED_CHOICES, default='CAT')
    significant_in = models.CharField(max_length=50, verbose_name=("Significant in Country, City, ..."),
                                      blank=True, null=True)
    comment = models.CharField(verbose_name=("Commentary"), max_length=250, blank=True, null=True)
    # date = models.DateField(verbose_name=("Date"))
    day = models.PositiveSmallIntegerField(verbose_name='Day')
    month = models.PositiveSmallIntegerField(verbose_name='Month')

    def display_names(self):
        return ', '.join([name.name for name in self.names.all()])

    display_names.short_description = 'Names'
    display_names.allow_tags = True

    def __str__(self):
        # print(self.names.all())
        return ', '.join([name_s.name for name_s in self.names.all()])

    def clean(self):
        super(Saint, self).clean()
        if self.source_book == None and self.source_url == None:
            raise ValidationError('Must be at least source')
