from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse #Used to generate URLs by reversing the URL patterns

class Mood(models.Model):
    status = models.CharField(max_length=10, null=False)

    def __str__(self):
        return self.status

class Post(models.Model):
    mood = models.ForeignKey('Mood', on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10, default='不願意透漏身份的人')
    message = models.TextField(null=False)
    del_pass = models.CharField(max_length=10)
    pub_time = models.DateTimeField(auto_now=True)
    enabled = models.BooleanField(default=False)
    
    def __str__(self):
        return self.message

# class User(models.Model):
#     name = models.CharField(max_length=20, null=False)
#     email = models.EmailField()
#     password = models.CharField(max_length=20, null=False)
#     enabled = models.BooleanField(default=False)

#     def __str__(self):
#         return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    height = models.PositiveIntegerField(default=160)
    male = models.BooleanField(default=False)
    website = models.URLField(null=True)
    
    class Meta:
        verbose_name = '人員資訊'
        verbose_name_plural = '人員資訊'

    def __str__(self):
        return self.user.username


class Diary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget = models.FloatField(default=0)
    weight = models.FloatField(default=0)
    note = models.TextField()
    ddate = models.DateField()

    def __str__(self):
        return "{}({})".format(self.ddate, self.user)

# Create your models here.
#定義model的class類別之前都需要先import models
#每個class類別都代表一個資料表

class Location(models.Model):
    """
    Model 遊戲機安裝地點  (e.g. ).
    """
    #欄位名稱:name
    #CharField:大概是varchar, nvarchar之類的
    #max_length:此欄位最大長度
    #help_text:此欄位的註解，實務上在公司還真的很少人寫註解在資料表
    siteID = models.CharField(max_length=20, verbose_name = '地點代碼')
    siteDesc = models.CharField(max_length=120, verbose_name = '位址說明')
    CITY = (
        ('Tpe', '台北市'),
        ('NewTpe', '新北市'),
        ('Tauyan', '桃園市'),
        ('Taichong', '台中市'),
        ('Kaohsung', '高雄市'),
    )
    siteCity = models.CharField(max_length=10, choices=CITY, blank=True, default='Tpe', verbose_name = '城市')
    
    #__str__:Django framework的作法會在每個資料表都定義一個__str__
    #這是用來定義物件最常用的method用的，因此會直接回傳self.name    
    class Meta:
        verbose_name = '安裝地點'
        verbose_name_plural = '安裝地點'

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.siteID


class Stand(models.Model):
    """
    Model 機台  (e.g. ).
    """
    #欄位名稱:name
    #help_text:此欄位的註解，實務上在公司還真的很少人寫註解在資料表
    standID = models.CharField(max_length=20, verbose_name = '機台代碼')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, verbose_name = '安裝地點')
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name = '負責人')
    standDesc = models.CharField(max_length=120, null=True, verbose_name = '機台說明')
    standPrice = models.FloatField(default=0, verbose_name = '機台價格')

    class Meta:
        verbose_name = '機台'
        verbose_name_plural = '機台'

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.standID

    #get_absolute_url:這是自定義的函數，當你使用get_absolute_url的時候
    #會透過book-detail這個url mapping的這個網址mapping規則去導向網頁
    #當然最後會導向的網頁會顯示這個Book物件的詳細細節
    def get_absolute_url(self):
        """
        Returns the url to access a detail record for this book.
        """
        return reverse('stand-detail', args=[str(self.standID)])      


class Income(models.Model):
    """
    Model 機台收款.
    """
    #欄位名稱:name
    #help_text:此欄位的註解，實務上在公司還真的很少人寫註解在資料表
    standID = models.ForeignKey(Stand, on_delete=models.SET_NULL, null=True, verbose_name = '機台代碼')
    workDay = models.DateField(null=True, blank=True, verbose_name = '日期')
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name = '負責人')
    amount = models.FloatField(default=0, verbose_name = '金額')
    note = models.TextField(verbose_name = '備註說明')

    class Meta:
        # ordering = ["standID", "workDay"]   #108.8.21 有DB 1366 問題
        verbose_name = '機台收入'
        verbose_name_plural = '機台收入'

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return '({0}) {1} {2}'.format(self.standID.standID, self.workDay, self.amount)

    def get_absolute_url(self):
        """
        Returns the url to access the income of a particular stand.
        """
        return reverse('income-detail', args=[str(self.standID)])

class MessageLog(models.Model):
    sender = models.CharField(max_length=30, null=False)
    message = models.TextField(null=False)
    sendTime = models.DateTimeField(auto_now_add=True)
    toWhom = models.CharField(max_length=30)
    isMail = models.BooleanField(default=False)
    isLine = models.BooleanField(default=False)
    isELK = models.BooleanField(default=False)
    
    class Meta:
        # ordering = ["standID", "workDay"]   #108.8.21 有DB 1366 問題
        verbose_name = '訊息傳送Ｌog'
        verbose_name_plural = '訊息傳送Ｌog'

    def __str__(self):
        return '{0} {1} {1}'.format(self.sender, self.sendTime, self.message)