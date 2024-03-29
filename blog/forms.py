# coding: utf-8 

from django import forms


from .models import Post, Comment

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)


class PostsListForm(forms.Form):
    search = forms.CharField(required=False)
    sort_field = forms.ChoiceField(choices=(('author', 'Автор'), ('-pub_date', u'Дата публикации')), required=False)

    def clean_search(self):
        search = self.cleaned_data.get('search')
        return search


class BlogForm(forms.Form):
    title = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea)



