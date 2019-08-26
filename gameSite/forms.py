#_*_ encoding: utf-8 *_*
from django import forms
from . import models

class ContactForm(forms.Form):
    CITY = [
        ['TP', 'Taipei'],
        ['TY', 'Taoyuang'],
        ['TC', 'Taichung'],
        ['TN', 'Tainan'],
        ['KS', 'Kaohsiung'],
        ['NA', 'Others'],
    ]
    user_name = forms.CharField(label='您的姓名', max_length=50, initial='XUTEAN')
    # user_city = forms.ChoiceField(label='居住城市', choices=CITY)
    # user_school = forms.BooleanField(label='是否在學', required=False)
    user_email = forms.EmailField(label='訊息送至（email）')
    user_message = forms.CharField(label='您的意見', widget=forms.Textarea(attrs={'cols': 30, 'rows': 5}))

class LineForm(forms.Form):
    CITY = [
        ['TP', 'Taipei'],
        ['TY', 'Taoyuang'],
        ['TC', 'Taichung'],
        ['TN', 'Tainan'],
        ['KS', 'Kaohsiung'],
        ['NA', 'Others'],
    ]
    user_name = forms.CharField(label='您的姓名', max_length=50, initial='XUTEAN')
    # user_city = forms.ChoiceField(label='居住城市', choices=CITY)
    # user_school = forms.BooleanField(label='是否在學', required=False)
    # user_email = forms.EmailField(label='訊息將 Line 至 xutean')
    user_message = forms.CharField(label='您的訊息', widget=forms.Textarea(attrs={'cols': 30, 'rows': 5}))

class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['mood', 'nickname', 'message', 'del_pass']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['mood'].label = '現在心情'
        self.fields['nickname'].label = '你的暱稱'
        self.fields['message'].label = '心情留言'
        self.fields['del_pass'].label = '設定密碼'

class LoginForm(forms.Form):
    # username = forms.CharField(label='姓名', widget=forms.TextInput(attrs={'width':'400px', 'height':'30px'}))
    username = forms.CharField(label='姓名', widget=forms.Textarea(attrs={'cols': 20, 'rows': 1}))  # It's OK
    password = forms.CharField(label='密碼', widget=forms.PasswordInput(attrs={'width':'400px', 'height':'30px'}))  # width Not work

class DateInput(forms.DateInput):
    input_type = 'date'

class DiaryForm(forms.ModelForm):

    class Meta:
        model = models.Diary
        fields = ['budget', 'weight', 'note', 'ddate']
        widgets = {
            'ddate': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super(DiaryForm, self).__init__(*args, **kwargs)
        self.fields['budget'].label = '今日花費(元)'
        # self.fields['budget'].widget.attrs['wdith'] = '200px'
        self.fields['weight'].label = '今日體重(KG)'
        self.fields['note'].label = '心情留言'
        self.fields['ddate'].label = '日期'
        self.fields['note'].widget.attrs['cols'] = 50
        self.fields['note'].widget.attrs['rows'] = 5
        # self.fields['note'].widget.attrs['width'] = '200px'  # Not work
        # self.fields['note'].widget.attrs['height'] = '10px'  # Not work

class ProfileForm(forms.ModelForm):

    class Meta:
        model = models.Profile
        fields = ['height', 'male', 'website']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['height'].label = '身高(cm)'
        self.fields['male'].label = '是男生嗎'
        self.fields['website'].label = '個人網站'
        
class IncomeForm(forms.ModelForm):
    class Meta:
        model = models.Income
        fields = ['standID', 'workDay', 'employee', 'amount', 'note']
        
        widgets = {
            'workDay': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super(IncomeForm, self).__init__(*args, **kwargs)
        self.fields['amount'].label = '今日收費(元)'
        self.fields['note'].label = '留言註記'
        self.fields['workDay'].label = '日期'
        self.fields['note'].widget.attrs['cols'] = 50
        self.fields['note'].widget.attrs['rows'] = 5 

class IncomeForm4Create(forms.ModelForm):
    class Meta:
        model = models.Income
        fields = [  'amount', 'workDay', 'standID', 'note']
        
        widgets = {
            'workDay': DateInput(),
        }
        
    def __init__(self, user, *args, **kwargs):
        super(IncomeForm4Create, self).__init__(*args, **kwargs)
        #  以下是一個  join 關係
        self.fields['standID'].queryset = models.Stand.objects.filter(employee=user)
        self.fields['note'].widget.attrs['cols'] = 50
        self.fields['note'].widget.attrs['rows'] = 2 
    
class IncomeForm4Update(forms.ModelForm):
    class Meta:
        model = models.Income
        fields = [  'amount', 'workDay', 'note']
        
        # widgets = {
        #     'workDay': DateInput(),
        # }
        
    def __init__(self, *args, **kwargs):
        super(IncomeForm4Update, self).__init__(*args, **kwargs)
        #  以下是一個  join 關係
        # self.fields['standID'].queryset = models.Stand.objects.filter(employee=user)
        self.fields['note'].widget.attrs['cols'] = 50
        self.fields['note'].widget.attrs['rows'] = 2 


# class IncomeForm(forms.ModelForm):
#         model = models.Income
#         fields = ['amount', 'note', 'workDay']
#         widgets = {
#             'workDay': DateInput(),
#         }

    # def __init__(self, *args, **kwargs):
    #     super(IncomeForm, self).__init__(*args, **kwargs)
    #     self.fields['amount'].label = '今日收費(元)'
    #     self.fields['note'].label = '留言註記'
    #     self.fields['workDay'].label = '日期'
