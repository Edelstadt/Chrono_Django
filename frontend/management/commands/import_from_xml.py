from django.core.management.base import BaseCommand
from lxml import etree as ET

from frontend.models import Author, Book, URL, Name, Saint


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        # Saint.objects.all().delete()
        with open('./output.xml', 'rt') as f:
            tree = ET.parse(f)
            root = tree.getroot()

            authors = tree.xpath('//author')
            for author in authors:
                name = author.find('name').text
                surname = author.find('surname').text
                try:
                    Author.objects.get(lastname=name, surname=surname)
                except Author.DoesNotExist:
                    Author.objects.create(lastname=name, surname=surname)

            articles = tree.xpath('//book')
            for article in articles:
                name = article.find('author').find('name').text
                surname = article.find('author').find('surname').text
                isbn = article.find('isbn').text
                title = article.find('publication_title').text
                place = article.find('place_issue').text
                publisher = article.find('publisher').text
                year = article.find('year_publication').text
                try:
                    author = Author.objects.get(lastname=name, surname=surname)
                except Author.DoesNotExist:
                    author = Author.objects.create(lastname=name, surname=surname)
                try:
                    article = Book.objects.get(title=title, author=author,
                                               year=year, isbn=isbn, publisher=publisher,
                                               place_publish=place)
                except Book.DoesNotExist:
                    article = Book.objects.create(title=title, author=author,
                                                  year=year, isbn=isbn, publisher=publisher,
                                                  place_publish=place)

            urls = tree.xpath('//url')
            for url in urls:
                name = url.find('author').find('name').text
                surname = url.find('author').find('surname').text
                page_title = url.find('page_title').text
                web_title = url.find('web_title').text
                addrese = url.find('addrese').text
                date_visit = url.find('date_visit').text
                date_citation = url.find('date_citation').text
                try:
                    author = Author.objects.get(lastname=name, surname=surname)
                except Author.DoesNotExist:
                    author = Author.objects.create(lastname=name, surname=surname)
                try:
                    url = URL.objects.get(page_title=page_title, author=author,
                                          web_title=web_title, url=addrese,
                                          date_visit=date_visit,
                                          date_citate=date_citation)
                except URL.DoesNotExist:
                    url = URL.objects.create(page_title=page_title, author=author,
                                             web_title=web_title, url=addrese,
                                             date_visit=date_visit,
                                             date_citate=date_citation)

            articles = tree.xpath('//article')
            Saint.objects.all().delete()
            for article in articles:
                date = article.find('date').text
                date = [int(s) for s in str(date).split('-') if s.isdigit()]
                day = date[1]
                month = date[0]
                name_cs = ""
                name_de = ""
                name_lat = ""
                for name in article.findall('name'):

                    lang = name.attrib['lang']
                    name_lg = name.text
                    if lang == 'CS':
                        name_cs = name_lg
                    elif lang == 'DE':
                        name_de = name_lg
                    elif lang == 'LAT':
                        name_lat = name_lg

                since = article.find('since').text
                until = article.find('until').text
                venerated = article.find('venerated').text
                significant_in = article.find('significant_in').text
                comment = article.find('comment').text

                name_cs_db = False
                if name_cs != "":
                    try:
                        name_cs_db = Name.objects.get(language='CS', name=name_cs)
                    except Name.DoesNotExist:
                        name_cs_db = Name.objects.create(language='CS', name=name_cs)
                name_de_db = False
                if name_de != "":
                    try:
                        name_de_db = Name.objects.get(language='DE', name=name_de)
                    except Name.DoesNotExist:
                        name_de_db = Name.objects.create(language='DE', name=name_de)
                name_lat_db = False
                if name_lat != "":
                    try:
                        name_lat_db = Name.objects.get(language='LAT', name=name_lat)
                    except Name.DoesNotExist:
                        name_lat_db = Name.objects.create(language='LAT', name=name_lat)

                if venerated == 'Catholic':
                    venerated = 'CAT'
                else:
                    venerated = 'ORT'

                name_list = [name_cs_db, name_de_db, name_lat_db]
                source = Book.objects.get(title='Historická chronologie')
                for name in name_list:
                    if name != False:
                        try:
                            saint = Saint.objects.get(name=name, source_book=source,
                                                      venerated=venerated,
                                                      comment=comment, day=day, month=month)
                        except Saint.DoesNotExist:
                            saint = Saint.objects.create(venerated=venerated,
                                                         comment=comment, day=day, month=month)

                            saint.save()
                            for name in name_list:
                                if name:
                                    saint.name.add(name)
                                    saint.save()
                            saint.source_book.add(source)
                            saint.save()
