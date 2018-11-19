from django.contrib import admin

# Register your models here.
from app.models import UserModel, AddressModel

class AddressInfo(admin.TabularInline):
    extra = 3
    model = AddressModel


class UserAdmin(admin.ModelAdmin):

    list_display = 'u_name', 'u_password'
    search_fields = 'u_name',
    list_filter = 'u_name',

    fieldsets = (
        ('基本信息', {'fields': ('u_name',)}),
        ('可选信息', {'fields': ('u_password',)}),
    )


class AddressAdmin(admin.ModelAdmin):
    list_display = 'a_address', 'a_user'


admin.site.register(UserModel, UserAdmin)
admin.site.register(AddressModel, AddressAdmin)