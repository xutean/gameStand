from django.contrib import admin
from gameSite import models
from .models import Location, Stand, Income, MessageLog

class PostAdmin(admin.ModelAdmin):
    list_display=('nickname', 'message', 'enabled', 'pub_time')
    ordering=('-pub_time',)
admin.site.register(models.Mood)
admin.site.register(models.Post, PostAdmin)
# admin.site.register(models.User)
admin.site.register(models.Profile)
admin.site.register(models.Diary)

# Register your models here.
class StandInline(admin.TabularInline):
    model = Stand
    extra = 1
class SiteAdmin(admin.ModelAdmin):
    list_display = ('siteID', 'siteCity', 'siteDesc')
    fields = ['siteID', 'siteCity', 'siteDesc']
    inlines = [StandInline]
admin.site.register(Location, SiteAdmin)


class IncomeInstanceInline(admin.TabularInline):
    model = Income     # IncomeInstance
    extra = 1
@admin.register(Stand)
class StandAdmin(admin.ModelAdmin):
    list_display = ('standID', 'standDesc', 'location', 'employee', 'standPrice')   # 用到 
    inlines = [IncomeInstanceInline]


@admin.register(Income) 
class IncomeAdmin(admin.ModelAdmin):    
    list_display = ('standID', 'workDay', 'employee', 'amount', 'note')   # BookInstance list 用到
    list_filter = ('standID', 'employee')

@admin.register(MessageLog) 
class MessageLogAdmin(admin.ModelAdmin):    
    list_display = ('sender', 'message', 'sendTime', 'toWhom', 'isMail', 'isLine', 'isELK')   

admin.site.site_header = '遊戲機台 管理網站'
admin.site.site_title = '我的遊戲機台網站'
admin.site.index_title = '後台管理'