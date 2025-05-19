from django.shortcuts import render,redirect
from .forms import RegisterUserForm,CreatePostForm,commentForm,update_profile_form
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import  LoginRequiredMixin
from .models import Post,Profile,Comment
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import ListView,DetailView
from django.http import JsonResponse

class homeView(ListView):
    model = Post
    template_name = "Fluxx/home.html"
    paginate_by = 6
    ordering = "-created_at"
    
def registerView(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registered successfully. Please log in.")
            return redirect('login')
    else:
        form = RegisterUserForm()
    return render(request, 'Fluxx/register.html', {'form': form})
    	

def loginView(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,"user does not exist")
    return render(request, 'Fluxx/login.html')
    
    
def logoutView(request):
    logout(request)
    return redirect('login')

@login_required()
def CreatePostView(request):
    
    if request.method=="POST":
        form = CreatePostForm(request.POST)
        if form.is_valid():
            postForm = form.save(commit=False)
            postForm.author = request.user
            postForm.save()
            messages.success(request, "post created")
            return redirect('home')

    else:
        form = CreatePostForm()
    return render(request, "Fluxx/createPost.html",{"form":form})


@login_required
def like_post(request,post_id):
    post =get_object_or_404(Post,id=post_id)
    
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        
    return redirect('home')

@login_required
def follow(request,user_id):
    user = get_object_or_404(User,id=user_id)
    profile = user.profile
    
    if request.user != user:
        if request.user in profile.followers.all():
            profile.followers.remove(request.user)
        else:
            profile.followers.add(request.user)
    return redirect("profile", user_id=user_id)


@login_required
def comment(request, pk):
    post = get_object_or_404(Post, id=pk)
    comments = post.comments.all()
    
    if request.method == "POST":
        form = commentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = commentForm()
         
    context = {
        'form': form,
        'comments': comments,
        'post': post,
    }
    return render(request, "Fluxx/post_detail.html", context)

@login_required
def profile(request,user_id):
    user = get_object_or_404(User,id=user_id)
    profile,created = Profile.objects.get_or_create(user=user)
    
    return render(request,"Fluxx/profile.html",{"profile":profile,"user":user})


def  post_delete_view(request,post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if post.author != request.user:
        return JsonResponse({"error":"unauthorize"},status=403)

    if request.method=="POST":
        post.delete()
        return redirect("home")
    return JsonResponse({'error': 'Invalid request'}, status=400)

def update_profile(request):
 
    if request.method=="POST":
        form = update_profile_form(request.POST,requst.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = update_profile_form(instance = request.user)
    
    return render(request,"Fluxx/update-profile.html",{"form":form})
        
    
    