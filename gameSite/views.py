from django.shortcuts import render, get_object_or_404
import json
import urllib
from datetime import datetime
from django.conf import settings
from . import models, forms
from .models import Location, Stand, Income, MessageLog
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . import lineNotifyMessage   # Line Notify 

from django.http import JsonResponse
from django.template.loader import render_to_string

# Create your views here.
# def index(request):
#     years = range(1960,2021)
#     try:
#         urid = request.GET['user_id']
#         urpass = request.GET['user_pass']
#         uryear = request.GET['byear']
#         urfcolor = request.GET.getlist('fcolor')
#     except:
#         urid = None

#     if urid != None and urpass == '12345':
#         verified = True
#     else:
#         verifeid = False
#     return render(request, 'index.html', locals())

def login(request):
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            login_name=request.POST['username'].strip()
            login_password=request.POST['password']
            user = authenticate(username=login_name, password=login_password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    print("success")
                    messages.add_message(request, messages.SUCCESS, '成功登入了')
                    return redirect('/')
                else:
                    messages.add_message(request, messages.WARNING, '帳號尚未啟用')
            else:
                messages.add_message(request, messages.WARNING, '登入失敗')
        else:
            messages.add_message(request, messages.INFO,'請檢查輸入的欄位內容')
    else:
        login_form = forms.LoginForm()
    return render(request, 'login.html', locals())

def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.INFO, "成功登出了")
    return redirect('/')

def index(request, pid=None, del_pass=None):
    if request.user.is_authenticated:
        username = request.user.username
        useremail = request.user.email
        try:
            user = models.User.objects.get(username=username)
            diaries = models.Diary.objects.filter(user=user).order_by('-ddate')
        except:
            pass
    messages.get_messages(request)
    return render(request, 'index.html', locals())

@login_required(login_url='/login/')
def userinfo(request):
    if request.user.is_authenticated:
        username = request.user.username
    user = User.objects.get(username=username)
    try:
        profile = models.Profile.objects.get(user=user)
    except:
        profile = models.Profile(user=user)

    if request.method == 'POST':
        profile_form = forms.ProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            messages.add_message(request, messages.INFO, "個人資料已儲存")
            profile_form.save()  
            return HttpResponseRedirect('/userinfo')
        else:
            messages.add_message(request, messages.INFO, '要修改個人資料，每一個欄位都要填...')
    else:
        profile_form = forms.ProfileForm()
    return render(request, 'userinfo.html', locals())


# def index(request, pid=None, del_pass=None):
#     posts = models.Post.objects.filter(enabled = True).order_by('-pub_time')[:30]
#     moods = models.Mood.objects.all()
#     try:
#         user_id = request.GET['user_id']
#         user_pass = request.GET['user_pass']
#         user_post = request.GET['user_post']
#         user_mood = request.GET['mood']
#     except:
#         user_id = None
#         message = '如要張貼訊息，則每一個欄位都要填...'

#     if del_pass and pid:
#         try:
#             post = models.Post.objects.get(id=pid)
#         except:
#             post = None
#         if post:
#             if post.del_pass == del_pass:
#                 post.delete()
#                 message = "資料刪除成功"
#             else:
#                 message = "密碼錯誤"
#     elif user_id != None:
#         mood = models.Mood.objects.get(status=user_mood)
#         post = models.Post.objects.create(mood=mood, nickname=user_id, del_pass=user_pass, message=user_post)
#         post.save()
#         message='成功儲存！請記得你的編輯密碼[{}]!，訊息需經審查後才會顯示。'.format(user_pass)

#     return render(request, 'index.html', locals())


def listing(request):
    posts = models.Post.objects.filter(enabled=True).order_by('-pub_time')[:150]
    moods = models.Mood.objects.all()
    return render(request, 'listing.html', locals())

@login_required(login_url='/login/')
def posting(request):
    if request.user.is_authenticated:
        username = request.user.username
        useremail = request.user.email
    messages.get_messages(request)
        
    if request.method == 'POST':
        user = User.objects.get(username=username)
        diary = models.Diary(user=user)
        post_form = forms.DiaryForm(request.POST, instance=diary)
        if post_form.is_valid():
            messages.add_message(request, messages.INFO, "日記已儲存")
            post_form.save()  
            return HttpResponseRedirect('/')
        else:
            messages.add_message(request, messages.INFO, '要張貼日記，每一個欄位都要填...')
    else:
        post_form = forms.DiaryForm()
        messages.add_message(request, messages.INFO, '要張貼日記，每一個欄位都要填...')
    return render(request, 'posting.html', locals())

@login_required(login_url='/login/')
def income(request):
    if request.user.is_authenticated:
        username = request.user.username
        useremail = request.user.email
    messages.get_messages(request)
        
    if request.method == 'POST':
        user = User.objects.get(username=username)
        income = models.Income(user=user)
        income_form = forms.IncomeForm(request.POST, instance=diary)
        if income_form.is_valid():
            messages.add_message(request, messages.INFO, "收入已儲存")
            income_form.save()  
            return HttpResponseRedirect('/')
        else:
            messages.add_message(request, messages.INFO, '要填報收入，每一個欄位都要填...')
    else:
        income_form = forms.IncomeForm()
        messages.add_message(request, messages.INFO, '要填報收入，每一個欄位都要填...')
    return render(request, 'income.html', locals())

def save_income_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            incomes = Income.objects.all()
            data['html_book_list'] = render_to_string('books/includes/partial_book_list.html', {
                'books': incomes
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def save_income_form_4Create(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            income = form.save(commit=False)
            income.employee = request.user
            income.save()
            data['form_is_valid'] = True
            incomes = models.Income.objects.all()
            data['html_book_list'] = render_to_string('books/includes/partial_book_list.html', {
                'books': incomes
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def save_income_form_4Update(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            income = form.save(commit=False)
            income.employee = request.user
            # income.standID = request.standID
            income.save()
            data['form_is_valid'] = True
            incomes = models.Income.objects.all()
            data['html_book_list'] = render_to_string('books/includes/partial_book_list.html', {
                'books': incomes
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required(login_url='/login/')
def income_list(request):
    if request.user.is_authenticated:
        username = request.user.username
        useremail = request.user.email
        me = models.User.objects.get(username=username)   # 只能看Login者的資料，取得user的 ID
    messages.get_messages(request)
    incomes = models.Income.objects.filter(employee=me.id)
    return render(request, 'books/book_list.html', {'books': incomes, 'username': username})
    # return render(request, 'books/book_list.html', locals())

def income_create(request):
    if request.method == 'POST':
        form = forms.IncomeForm4Create(request.user, request.POST)
    else:
        form = forms.IncomeForm4Create(request.user)
    return save_income_form_4Create(request, form, 'books/includes/partial_book_create.html')

def income_create_BAK(request):
    if request.method == 'POST':
        form = forms.IncomeForm(request.POST)
    else:
        form = forms.IncomeForm()
    return save_income_form(request, form, 'books/includes/partial_book_create.html')

def income_update(request, pk):
    income = get_object_or_404(Income, pk=pk)
    if request.method == 'POST':
        form = forms.IncomeForm4Update(request.POST, instance=income)
    else:
        form = forms.IncomeForm4Update(instance=income)   #IncomeForm(instance=income)
    return save_income_form_4Update(request, form, 'books/includes/partial_book_update.html')

def income_update_BAK(request, pk):
    income = get_object_or_404(Income, pk=pk)
    if request.method == 'POST':
        form = forms.IncomeForm(request.POST, instance=income)
    else:
        form = forms.IncomeForm(instance=income)   #IncomeForm(instance=income)
    return save_income_form(request, form, 'books/includes/partial_book_update.html')

def income_delete(request, pk):
    income = get_object_or_404(Income, pk=pk)
    data = dict()
    if request.method == 'POST':
        income.delete()
        data['form_is_valid'] = True
        incomes = Income.objects.all()
        data['html_book_list'] = render_to_string('books/includes/partial_book_list.html', {
            'books': incomes
        })
    else:
        context = {'book': income}
        data['html_form'] = render_to_string('books/includes/partial_book_delete.html', context, request=request)
    return JsonResponse(data)

def logMessage(sender, msg, toMail, isMail, isLine, isELK):
    aLog = {}
    aLog['sender'] = sender
    aLog['message'] = msg
    aLog['toWhom'] = toMail
    aLog['isMail'] = isMail
    aLog['isLine'] = isLine
    aLog['isELK'] = isELK
    msgLog = models.MessageLog.objects.create(**aLog)
    msgLog.save

@login_required(login_url='/login/')
def contact(request):
    if request.user.is_authenticated:
        username = request.user.username
        useremail = request.user.email
    messages.get_messages(request)
    
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            message = "已傳送，感謝您"
            user_name = form.cleaned_data['user_name']
            # user_city = form.cleaned_data['user_city']
            # user_school = form.cleaned_data['user_school']
            user_email  = form.cleaned_data['user_email']
            user_message = form.cleaned_data['user_message']
            mail_body = u'''
傳送人員：{}
反應訊息：如下
{}'''.format(user_name, user_message)
            send_mail(
    '機台訊息反映',
    mail_body,
    # 'a6898208@gmail.com',
    'xutean@gmail.com',
    [user_email],
    fail_silently=False,
)
            logMessage(username,user_message,user_email,True,False,False)
            # 透過　Line Notify 傳送訊息
            message = mail_body
            token = 'TdeotZwuPDqcqIySqV4g8b6L28TqWCsivuCUWsoriTO'
            lineNotifyMessage.sendMessage(token, message)
            logMessage(username,user_message,user_email,False,True,False)
            # 透過　Line Notify 傳送訊息
            # 透過　Line Notify 傳送訊息

        else:
            message = "請檢查您輸入的資訊是否正確！"
    else:
        form = forms.ContactForm()
    return render(request, 'contact.html', locals())

def contact＿BAK(request):
    if request.user.is_authenticated:
        username = request.user.username
        useremail = request.user.email
    messages.get_messages(request)
    
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            message = "感謝您的來信。"
            user_name = form.cleaned_data['user_name']
            user_city = form.cleaned_data['user_city']
            user_school = form.cleaned_data['user_school']
            user_email  = form.cleaned_data['user_email']
            user_message = form.cleaned_data['user_message']
            mail_body = u'''
傳送人員：{}
居住城市：{}
是否在學：{}
反應訊息：如下
{}'''.format(user_name, user_city, user_school, user_message)
            send_mail(
    '機台訊息反映',
    mail_body,
    # 'a6898208@gmail.com',
    'xutean@gmail.com',
    [user_email],
    fail_silently=False,
)

        else:
            message = "請檢查您輸入的資訊是否正確！"
    else:
        form = forms.ContactForm()
    return render(request, 'contact.html', locals())


def post2db(request):
    if request.method == 'POST':
        post_form = forms.PostForm(request.POST)
        if post_form.is_valid():
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''
            if result['success']:
                message = "您的訊息已儲存，要等管理者啟用後才看得到喔。"
                post_form.save()
                return HttpResponseRedirect('/list/')
            else:
                message = "Invalid reCAPTCHA. Please try again."
        else:
            message = '如要張貼訊息，則每一個欄位都要填...'
    else:
        post_form = forms.PostForm()
        message = '如要張貼訊息，則每一個欄位都要填...'          

    return render(request, 'post2db.html', locals())

# Create your views here.

def book_list(request):
    books = Income.objects.all()
    return render(request, 'books/book_list.html', {'books': books})