from django import forms
from blog.models import Comment, Post

class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('author', 'title', 'text')
        # widgets are css styling to individual title tab or text tab
        # widget is a dictionary, key is field, value is forms.widgetname
        # value of widget gives attribute of which class to be used for styling that key field
        # editable class comes from medium editor library
        # the classes are CSS pre-defined are editable and medium, our CSS are textinputclass and postcontent
        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})

        }

class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ('author', 'text')
        widgets = {
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
        }
