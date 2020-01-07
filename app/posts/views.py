from django.shortcuts import render, redirect

from posts.models import Post, PostLike


def post_list(request):
    posts = Post.objects.order_by('-pk')
    context = {
        'posts': posts,
    }
    return render(request, 'posts/post-list.html', context)


def post_like(request, pk):
    """
    pk가 pk인 Post에 대한
    1. PostLike객체를 생성한다
    2. 만약 이미 있다면, 삭제한다
    3. 완료 후 posts:postlist로 redirect한다
    """
    post = Post.objects.get(pk=pk)
    user = request.user

    post_like_qs = PostLike.objects.filter(post=post, user=user)

    if post_like_qs.exists():
        post_like_qs.delete()
    else:
        PostLike.objects.create(post=post, user=user)

    return redirect('posts:post-list')
