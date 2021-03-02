import os
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from shutil import copyfile
import csv
#from .forms import UploadFileForm
#from .models import XML, DOCX, CSV

from .static.conference import parse_conference_xml
from .static.abstracts import parse_abstracts_xml, check_abstracts_consistency, check_abstract_count_words
from .static.generator import generate_book

MEDIA_ROOT = settings.MEDIA_ROOT
CSV_PATH = MEDIA_ROOT + "/matches.csv"

# Create your views here.
def index(request):
    """Функция отображения для домашней страницы сайта."""
    return render(request, 'index.html', context={})


def save_copy_file(object_file, name):
    path = default_storage.save(name, ContentFile(object_file.file.read()))
    #tmp_file = os.path.join(settings.MEDIA_ROOT, path)


def send_files_to_server(request):
    if request.method == 'POST':
        #try:
        files = request.FILES
        # сохраняем копии загруженных пользователем файлов на наш сервер для дальнейшей работы с ними
        save_copy_file(files['conference'], 'conference.xml')
        save_copy_file(files['abstracts'], 'abstracts.xml')
        save_copy_file(files['template'], 'tpl.docx')
        save_copy_file(files['csv'], 'matches.csv')
        return render(request, 'edit_csv_page.html')


def show_csv(request):
    """ показать csv-файл на экране, чтобы отредактировать его """
    matches_dict = {}

    with open(CSV_PATH, mode='r') as infile:
        reader = csv.reader(infile, delimiter=':')
        # This skips the first row of the CSV file.
        next(reader)
        for rows in reader:
            key = rows[0]
            value = rows[1]
            matches_dict[key] = value
    return JsonResponse({'matches_dict': matches_dict})
    # return render(request, 'edit_csv_page.html', {'matches_dict': matches_dict})

def save_csv(request):
    '''TODO: подправить сохранение в csv (прилетает QueryDict)'''
    """получает данные из таблицы (edit_csv_page.html), перезаписывает их в CSV"""
    if request.method == 'POST':
        changed_csv = request.POST
        print(changed_csv)

        with open(CSV_PATH, 'w') as f:
            w = csv.DictWriter(f, changed_csv.keys())
            w.writeheader()
            w.writerow(changed_csv)


def process():
    # открываем копию файла с сервера
    conference_file = default_storage.open('conference.xml', 'r')
    # отдаем эту копию функции "parse_conference_xml"
    conference = parse_conference_xml(conference_file)
    # закрываем файл
    conference_file.close()

    abstracts_file = default_storage.open('abstracts.xml', 'r')
    abstracts_file_copy = default_storage.open('abstracts.xml', 'r')
    matches_file = default_storage.open('matches.csv', 'r')
    status_string = []
    abstracts, status_string = parse_abstracts_xml(abstracts_file, abstracts_file_copy, matches_file, status_string)
    abstracts_file.close()
    abstracts_file_copy.close()
    matches_file.close()

    status_string.append({"mores":[]})
    status_string = check_abstracts_consistency(abstracts, status_string)
    status_string.append({"warnings": []})
    status_string = check_abstract_count_words(abstracts, status_string)

    template_file = default_storage.open('tpl.docx', 'r')

    generate_book(conference, abstracts, str(template_file))

    template_file.close()

    # удаляем все временные файлы  с сервера для экономии места
    default_storage.delete('conference.xml')
    default_storage.delete('abstracts.xml')
    default_storage.delete('tpl.docx')
    default_storage.delete('matches.csv')
    default_storage.delete('generated_doc_tmp.docx')

    return render(request, 'uploaded.html', {'status':status_string,'book':default_storage.open('book_of_abstracts.docx', 'r')})
    #except:
        #return render(request, 'error.html', {'error':"Something gone wrong. You may have mistaken the files."})
        #return JsonResponse({'res':""})
    
    
    # handle_files(files)
    # form.save()
    # download_book(default_storage.open('book_of_abstracts.docx', 'r'))
    
    
    # Redirect to the document list after POST
    # return HttpResponseRedirect(reverse('upload_file'))
    # return JsonResponse({'result':'OK'})

    # else:
    #     form = UploadFileForm()
    #return JsonResponse({'result':'NEOK'})
    #return render(request, 'upload.html', {'form': form})

    # Load documents for the list page
    # documents = Document.objects.all()

    # Render list page with the documents and the form
    # return render(request, 'uploaded.html', {'documents': ""})


def download_file(request):
    path_to_file = request.GET.get('file_name')

    with open(path_to_file, 'rb') as f:
        contents = f.read()

    
    response = HttpResponse(contents, content_type='application/msword')
    response['Content-Disposition'] = 'attachment; filename=book_of_abstracts.docx'
    default_storage.delete('book_of_abstracts.docx')
    return response


# def handle_files_xml(file):
#    newdoc = XML(docfile=file)
#    newdoc.save()


# def handle_files_docx(file):
#    newdoc = DOCX(docfile=file)
#    newdoc.save()


# def handle_files_csv(file):
#    newdoc = CSV(docfile=file)
#    newdoc.save()




