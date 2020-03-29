from django import forms
from blog.models import Comment


class CommentForm(forms.ModelForm):
    name = forms.CharField(max_length=35, required=False)
    content = forms.CharField(widget=forms.Textarea, max_length=250, required=False)

    class Meta:
        model = Comment
        fields = ('name', 'content',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean(self):
        name = self.cleaned_data.get('name')
        content = self.cleaned_data.get('content')
        if not self.user.is_authenticated and not name:
            raise forms.ValidationError('Bạn chưa nhập tên')
        if not content:
            raise forms.ValidationError('Bạn chưa nhập nội dung')
        return self.cleaned_data
