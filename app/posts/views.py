from django.shortcuts import render


def post_list(request):
    return render(request, 'posts/post-list.html')
