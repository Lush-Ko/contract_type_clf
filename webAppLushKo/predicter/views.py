from django.shortcuts import render, redirect
from .models import Documents
from .forms import DocumentsForm
from django.views.generic import DetailView
from dev import model_wrapper as mw
import pdfkit


def predicter_home(request):
    error = ''
    if request.method == 'POST':
        form = DocumentsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            documents = Documents.objects.order_by('-date')
            model_prediction = mw.Predictor(documents[0])
            dict_prediction = model_prediction.predict_from_file(str(documents[0].document))
            documents[0].interpretation_confidence = dict_prediction['confidence']
            documents[0].interpretation_class = dict_prediction['class']
            documents[0].interpretation_html = model_prediction.write_html_markup(
                text=model_prediction._get_document_text(documents[0].document),
                predicted_class=documents[0].interpretation_class,
                out_html_path=f'predict/html/out_html{documents[0].id_uniq}.html'
            )
            documents[0].interpretation_pdf = pdfkit.from_file(
                f'predict/html/out_html{documents[0].id_uniq}.html',
                f'predict/html/out_html{documents[0].id_uniq}.pdf'
            )
            return redirect('result-answer', pk=str(documents[0].id_uniq))
        else:
            error = 'Form has error, check your document or filename'
    else:
        form = DocumentsForm()

    return render(request, 'predicter/predicter_home.html', {
        'form': form,
        'error': error
    })


def all_doc(request):
    documents = Documents.objects.order_by('-date')
    return render(request, 'predicter/all_doc.html', {'documents': documents})


class DocumentsDetailView(DetailView):
    model = Documents
    template_name = 'predicter/details.html'
    context_object_name = 'document'


class DocumentsDetailViewPDF(DetailView):
    model = Documents
    template_name = 'predicter/details_pdf.html'
    context_object_name = 'document'


class DocumentsDetailViewHTML(DetailView):
    model = Documents
    template_name = 'predicter/details_html.html'
    context_object_name = 'document'


class DocumentsDetailViewOrigin(DetailView):
    model = Documents
    template_name = 'predicter/details_origin.html'
    context_object_name = 'document'
