from django.contrib import admin
from .models import Person, Address, Email, Phone
from .models import Company, CompanyAddress, CompanyPhone, CompanyEmail
from .models import Project, ProjectAddress, ProjectManagers

#Tee up inlines for the Person admin page
class PhoneInline(admin.TabularInline):
	model = Phone
	extra = 0

class EmailInline(admin.TabularInline):
	model = Email
	extra = 0

class AddressInline(admin.StackedInline):
	model = Address
	extra = 0

#Begin Person admin class
class PersonAdmin(admin.ModelAdmin):
	#list_display = ()
	#list_filter = []
	#search_fields = []

	inlines = [
		AddressInline,
		PhoneInline,
		EmailInline,
	]

#Tee up inlines for the Company model
class CompanyPhoneInline(admin.TabularInline):
	model = CompanyPhone
	extra = 0

class CompanyAddressInline(admin.StackedInline):
	model = CompanyAddress
	extra = 0

class CompanyEmailInline(admin.TabularInline):
	model = CompanyEmail
	extra = 0

class CompanyAdmin(admin.ModelAdmin):

	inlines = [
		CompanyAddressInline,
		CompanyPhoneInline,
		CompanyEmailInline,
	]

#Tee up inlines for Project
class ProjectAddressInline(admin.StackedInline):
	model = ProjectAddress
	extra = 0

class ProjectManagersInline(admin.TabularInline):
	model = ProjectManagers
	extra = 0

class ProjectAdmin(admin.ModelAdmin):

	inlines = [
		ProjectAddressInline,
		ProjectManagersInline,
	]

# Register your models here.
admin.site.register(Person, PersonAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Project, ProjectAdmin)