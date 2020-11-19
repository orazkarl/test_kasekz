from django import forms
from .models import Post, Comment
from ckeditor.widgets import CKEditorWidget
from mptt.forms import TreeNodeChoiceField


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)



class CommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for visible in self.visible_fields():
        #     visible.field.widget.attrs['class'] = 'form-control'
        self.fields['parent'].widget.attrs.update({'class': 'd-none'})
        self.fields['parent'].label = ''
        self.fields['parent'].required = False
        self.fields['text'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Comment
        fields = ['text']

        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'col-sm-12'}),
        #     'email': forms.TextInput(attrs={'class': 'col-sm-12'}),
        #     'content': forms.Textarea(attrs={'class': 'form-control'}),
        # }

    def save(self, *args, **kwargs):
        Comment.objects.rebuild()
        return super(CommentForm, self).save(*args, **kwargs)