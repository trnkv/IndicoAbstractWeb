import os
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from shutil import copyfile
#from .forms import UploadFileForm
#from .models import XML, DOCX, CSV

from .static.conference import parse_conference_xml
from .static.abstracts import parse_abstracts_xml, check_abstracts_consistency, check_abstract_count_words
from .static.generator import generate_book

# Create your views here.
def index(request):
    """Функция отображения для домашней страницы сайта."""
    return render(request, 'index.html', context={})


def save_copy_file(object_file, name):
    path = default_storage.save(name, ContentFile(object_file.file.read()))
    #tmp_file = os.path.join(settings.MEDIA_ROOT, path)


def upload_file(request):
    if request.method == 'POST':
        #form = UploadFileForm(request.POST, request.FILES)
        #if form.is_valid():
        files = request.FILES
        save_copy_file(files['conference'], 'conference.xml')
        save_copy_file(files['abstracts'], 'abstracts.xml')
        save_copy_file(files['template'], 'tpl.docx')
        save_copy_file(files['csv'], 'matches.csv')
        save_copy_file(files['final'], 'final.docx')

        conference_file = default_storage.open('conference.xml', 'r')
        conference = parse_conference_xml(conference_file)
        conference_file.close()
        
        abstracts_file = default_storage.open('abstracts.xml', 'r')
        abstracts_file_copy = default_storage.open('abstracts.xml', 'r')
        matches_file = default_storage.open('matches.csv', 'r')
        abstracts = parse_abstracts_xml(abstracts_file, abstracts_file_copy, matches_file)
        abstracts_file.close()
        abstracts_file_copy.close()
        matches_file.close()

        check_abstracts_consistency(abstracts)
        check_abstract_count_words(abstracts)

        template_file = default_storage.open('tpl.docx', 'r')
        generate_book(conference, abstracts, template_file, default_storage.open('book_of_abstracts.docx', 'w'))
        template_file.close()
        # handle_files(files)
        # form.save()
        # return render(request, 'upload.html', {'form': form, 'files':files})
        
        # Redirect to the document list after POST
        #return HttpResponseRedirect(reverse('upload_file'))
        return JsonResponse({'result':'OK'})
    # else:
    #     form = UploadFileForm()
    #return JsonResponse({'result':'NEOK'})
    #return render(request, 'upload.html', {'form': form})

    # Load documents for the list page
    # documents = Document.objects.all()

    # Render list page with the documents and the form
    # return render(request, 'uploaded.html', {'documents': ""})


# def handle_files_xml(file):
#    newdoc = XML(docfile=file)
#    newdoc.save()


# def handle_files_docx(file):
#    newdoc = DOCX(docfile=file)
#    newdoc.save()


# def handle_files_csv(file):
#    newdoc = CSV(docfile=file)
#    newdoc.save()




