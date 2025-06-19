from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm, CommentForm


# Create your views here.
def post_list(request):
	# Filtramos los posts que ya han sido publicados y los ordenamos en orden descendente
	posts = Post.objects.filter(
	    published_date__lte=timezone.now()).order_by('-published_date')
	# Renderizamos la plantilla con los posts filtrados
	return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
	# Obtenemos el post por su ID (pk) o devolvemos un error 404 si no existe
	post = get_object_or_404(Post, pk=pk)
	# Renderizamos la plantilla con el post obtenido
	return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_new(request):
	# Si la petición es POST, significa que el usuario está enviando datos del formulario
	if request.method == "POST":
		# Construimos el formulario con los datos del POST
		form = PostForm(request.POST)
		# Validamos que el formulario sea correcto
		if form.is_valid():
			# Guardamos el formulario y lo asociamos al usuario actual
			post = form.save(commit=False)
			post.author = request.user
			#post.published_date = timezone.now()
			post.save()
			# Redirigimos al usuario a la página de detalle del post recién creado
			return redirect('post_detail', pk=post.pk)
	# Si el formulario no es válido o si la petición es GET, mostramos el formulario vacío
	else:
		form = PostForm()
	# Renderizamos la plantilla con el formulario
	return render(request, 'blog/post_edit.html', {'form': form, 'title': 'Nueva publicación'})


@login_required
def post_edit(request, pk):
	# Obtenemos el post por su ID (pk) o devolvemos un error 404 si no existe
    post = get_object_or_404(Post, pk=pk)
    # Si la petición es POST, significa que el usuario está enviando datos del formulario
    if request.method == "POST":
        # Construimos el formulario con los datos del POST y los datos del post existente
        form = PostForm(request.POST, instance=post)
        # Validamos que el formulario sea correcto
        if form.is_valid():
            # Guardamos el formulario y lo asociamos al usuario actual
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            
            return redirect('post_detail', pk=post.pk)
    else:
        # Si la petición es GET, construimos el formulario con los datos del post existente
        form = PostForm(instance=post)
	# Renderizamos la plantilla con el formulario
    return render(request, 'blog/post_edit.html', {'form': form, 'title': 'Editar publicación'})


@login_required
def post_draft_list(request):
	# Filtramos los posts que no han sido publicados y los ordenamos en orden descendente
    posts = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
	# Renderizamos la plantilla con los posts filtrados
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.publish()
    return redirect('post_list')


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
    return redirect('post_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})
