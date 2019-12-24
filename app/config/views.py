from django.shortcuts import render


def index(request):
    """
    settings.TEMPLATES의 DIRS에
        Instagram/app/templates 경로를 추가

    template: template/index.html
        <h1>Index</h1>
    """
    return render(request, 'index.html')
