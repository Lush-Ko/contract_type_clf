from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    """

    @param request:
    @return:
    """
    data = {
        'title': 'Main page',
        'values': ['wpd', 'weq', 'asd'],
        'obj': {
            'car': 'BMW',
            'age': 18,
            'hobby': 'no'
        }
    }
    return render(request, 'main/index.html', data)


def about(request):
    """

    @param request:
    @return:
    """
    return render(request, 'main/about.html')
