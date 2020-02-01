from django.db import models
from django.contrib.auth.models import User #giris-cikis, kayit, section yapilabilir

# Create your models here.
class Post(models.Model):
    header = models.CharField(max_length=50)
    content = models.TextField(max_length=3000)
    draft = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True) #object in ilk yazildiginda tutuldugu durum
    updated = models.DateTimeField(auto_now=True) #object ne zaman updated oldugunu tutar
    image = models.ImageField(blank=True) #formlarda bos gecilebilir defaut false olarak beliritilir
    liked = models.IntegerField(default=0) 
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='articles') #one to many iliskisi kuruyoruz. CASCADE ozel. kullanici 
                                                                                        #kaldirildiginda  onunla iliskili her bilgiyi kaldir
    def __str__(self):  #admin panelinde string yerine header gorunsun istiyoruz
        return self.header

class Comment(models.Model):
    header = models.CharField(max_length=30)  #help_text ile kullaniciya o kisimla ilgili bilgi vermek istedimizde kullanilir
    content = models.TextField(max_length=280)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='comments') #hangi posta bagli oldugu, related_name postan bilgi cekmekte kolaylik sagliyor

    def __str__(self):
        return f"{self.header}'e demisler ki"  #fstring kullanildi, self.header,self ile bu classtan urettigimiz nesneyi isaret ediyor; git onunn headerini al diyoruz

