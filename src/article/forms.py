from django import forms
from article.models import Post, Comment



class ArticleForm(forms.Form):
    header = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)
    liked  = forms.IntegerField(required=True)
    draft = forms.BooleanField(required=True)


class ArticleModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        #exclude = ['image', 'owner']

    #def clean_header(self):   #self ile olusturdugumuz formu isaret ediyrouz  GUNCELLEME KISMINDA KAPATTRIK
    #    header = self.cleaned_data.get('header') 
    #    #if Post.object.filter():
    #    #    raise forms.ValidationError('Baslik abc olamaz') 
    #    #return header  
    #    if Post.objects.filter(header=header).exists():
    #        raise forms.ValidationError('Bir baska makale bulunmakta') #eger makale varsa hata bassin  
    #    return header
        

    def clean_content(self):
        if len(self.cleaned_data.get('content')) < 50:
            raise forms.ValidationError('Icerik 50 karakterden kisa olamaz')       
        return self.cleaned_data.get('content')   


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['post']
        #def clean_liked(self):
        #    if len(self.cleaned_data.get('content')) < 30:
        #        raise forms.ValidationError('Icerik karakteri az')
        #    return self.cleaned_data.get('content')

        
