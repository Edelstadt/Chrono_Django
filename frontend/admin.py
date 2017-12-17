from django.contrib import admin
from django.db.models.base import ModelBase

from frontend import models as frontend_models

# # Very hacky!
for name, var in frontend_models.__dict__.items():
    if type(var) is ModelBase:
        admin.site.register(var)


class URLInLine(admin.ModelAdmin):
    list_display = ["page_title", "web_title", ]


class AuthorAdmin(admin.ModelAdmin):
    list_display = ["surname", "lastname", ]


class NameAdmin(admin.ModelAdmin):
    list_display = ["name", "language", ]


class SinceAdmin(admin.ModelAdmin):
    list_display = ["year", "century", ]


class UntilAdmin(admin.ModelAdmin):
    list_display = ["year", "century", ]


class BookAdmin(admin.ModelAdmin):
    list_display = ["title", ]


class SaintAdmin(admin.ModelAdmin):
    # inlines = [URLInLine, BookAdmin, NameAdmin, SinceAdmin, UntilAdmin]
    fieldsets = ((None, {'fields': ('names', 'source_book', 'source_url', 'since', 'until',
                                    'venerated', 'significant_in', 'comment', 'date')}),)
    list_display = ('display_names',)

    def get_names(self, obj):
        return "\n".join([p.name for p in obj.names.all()])

# admin.site.register(URL, URLInLine)
# admin.site.register(Author, AuthorAdmin)
# admin.site.register(Book, BookAdmin)
# admin.site.register(Name, NameAdmin)
# admin.site.register(Since, SinceAdmin)
# admin.site.register(Until, UntilAdmin)
# admin.site.register(Saint, SaintAdmin)
