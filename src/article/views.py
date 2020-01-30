from django.shortcuts import render, get_object_or_404,  redirect, reverse
from django.http import HttpResponse, Http404
from datetime import datetime
from article.models import Post, Comment
from article.forms import ArticleForm
from article.forms import ArticleModelForm, CommentForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, DetailView, FormView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin





# Create your views here.

def post_detail(request, post_id): #>3
    pk = post_id
    #try:
     #   post = Post.objects.get(id=pk) #get ile nesne donmesi saglandi        
    #except Post.DoesNotExist:
    #    return HttpResponse('post bulunamadi')
    post = get_object_or_404(Post, id=pk, draft=False)        
    comments = post.comments.all()
    #return HttpResponse('detay sayfasini duzenledim' + str(pk))
    form = CommentForm(request.POST or None) 
    context = {  #anlamsal icerik ureticilerimiz ->context

        'post': post,
        'comments' : comments,
        'form' : form
    }
    if request.method == 'POST':
        if form.is_valid():
            form.instance.post = post   #**instance nesnesi arka tarafta bir model tutuyor
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Basariyla olsuruldu') #message.info ile bunun bilgi mesaji oldugunu soyledi

            return redirect('post_detail', post_id=post_id)    #redirect; yeniden yonlendirme post_detail->urlde yazdigimiz nameden geldi yine urlden post_id verdigimizden parametreyi yazamk durumuzndayiz

    return render(request,'article/post_detail.html',context)   

def post_list(request): #>2
    queryset = Post.objects.all()
    context = {
        'postlar': queryset
    }
    return render(request, 'article/post_list.html',{'postlar': queryset})


def anasayfa(request):  #>1
    #return HttpResponse('Anasayfaya hosgeldiniz!')
    context = {
        'django': True,
        'flask': True,
        'pehape': False,
        'now': datetime.now()
    }
    return render(request,template_name='article/index.html', context=context)


def create_post(request):
    form = ArticleForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid(): #formu kontrol et
            #data = form.cleaned_data
            #return HttpResponse(str(data))  
            header = form.cleaned_data['header']
            content = form.cleaned_data['content']
            liked = form.cleaned_data['liked']
            draft = form.cleaned_data['draft']
            post = Post.objects.create (
                header=header, 
                content=content, 
                liked=liked,
                draft=draft,
                owner=request.user #o anda gris yapmis kullaniciyi bize donduruyor
            )
            post.save()
            return  HttpResponse('nesne yaratildi')
    else:
        print(request.user)
        return render(request, 'article/post_create.html', {'form': form})


def createPostMF(request):
    form = ArticleModelForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.owner = request.user
            form.save()
            return HttpResponse('nesne yaratildi')
     
    return render(request, 'article/post_create.html',{'form': form})    


    

"""
    CLASS BASED VIEW REFACTORING
"""

class ArticleListView(ListView):
    model = Post
    template_name = 'article/post_list.html'
    queryset = Post.objects.all()
    context_object_name = 'posts'


class ArticleCreateView(LoginRequiredMixin ,CreateView):
    #login_url = '/admin'  #logout ise login yapma istegi sunduk, setting.py  dan ekledik
    model = Post
    #fields = '__all__'  #form_class = ArticleModelForm verdigimizde de geliyor form ekrarni
    form_class = ArticleModelForm
    success_url = reverse_lazy('anasayfa')      #redirect 
    template_name = 'article/post_create.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user

        return super().form_valid(form) #super: createviewi isaret edip classiniza dokunmanizij sagliyor ust sinifta tanimlanmis classlarin attributelerine ulsamamizi sagliyor

    

class ArticleDetailView(DetailView, SuccessMessageMixin ,FormView):
    model = Post
    template_name = 'article/post_detail.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'
    form_class = CommentForm
    succcess_url = reverse_lazy('anasayfa')
    success_message = 'Basariyla yorum eklendi'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.object)
        context['comments'] = self.object.comments.all()
        return context 

    #def form_valid(self, form):
    #    #self.object = self.get_object()
    #    form.instance.post = self.get_object()
    #    form.save()
    #    return super().form_valid(form)



class ArticleUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Post
    form_class = ArticleModelForm
    template_name = 'article/post_create.html'
    success_url = reverse_lazy('anasayfa')
    success_message = 'Basari ile guncellendi'
    pk_url_kwarg = 'post_id' 


class  ArticleDeleteView(LoginRequiredMixin, SuccessMessageMixin,DeleteView):
    model = Post
    template_name = 'article/post_delete.html'
    pk_url_kwarg = 'post_id'
    success_message = 'Basari ile silindi'
    success_url = reverse_lazy('anasayfa')

    def delete(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.INFO, self.success_message)
        return super().delete(request, *args, **kwargs)




