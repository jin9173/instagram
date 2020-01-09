from django.shortcuts import render, redirect
from .models import Post, PostLike, PostImage
from .forms import PostCreateForm, CommentCreateForm


def post_list(request):
    posts = Post.objects.order_by('-pk')
    comment_form = CommentCreateForm()
    context = {
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'posts/post-list.html', context)


def post_like(request, pk):
    """
    pk가 pk인 Post와 (변수명 post사용)
    request.user로 전달되는 User (변수명 user사용)에 대해
    1. PostLike(post=post, user=user)인 PostLike객체가 존재하는지 확인한다
    2-1. 만약 해당 객체가 이미 있다면, 삭제한다
    2-2. 만약 해당 객체가 없다면 새로 만든다
    3. 완료 후 posts:post-list로 redirect한다
    URL: /posts/<pk>/like/
    """
    post = Post.objects.get(pk=pk)
    user = request.user
    print('post:', post)
    print('user:', user)

    post_like_qs = PostLike.objects.filter(post=post, user=user)
    # user, post에 해당하는 PostLike가 있는 경우
    if post_like_qs.exists():
        # 삭제
        post_like_qs.delete()
    # 없는 경우
    else:
        # 만든다
        PostLike.objects.create(post=post, user=user)

    return redirect('posts:post-list')


def post_create(request):
    """
    URL:        /posts/create/, name='post-create'
    Template:   /posts/post-create.html
    forms.PostCreateForm을 사용
    """
    if request.method == 'POST':
        text = request.POST['text']
        images = request.FILES.getlist('image')

        post = Post.objects.create(
            author=request.user,
            content=text
        )
        for image in images:
            post.postimage_set.create(image=image)

        return redirect('posts:post-list')
    else:
        form = PostCreateForm()
        context = {
            'form': form,
        }
        return render(request, 'posts/post-create.html', context)


def comment_create(request, post_pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=post_pk)
        # Form인스턴스를 만드는데, data에 request.POST로 전달된 dict를 입력
        form = CommentCreateForm(data=request.POST)
        # Form인스턴스 생성시, 주어진 데이터가
        # 해당 Form이 가진 Field들에 적절한 데이터인지 검증
        if form.is_valid():
            form.save(post=post, author=request.user)
        return redirect('posts:post-list')
