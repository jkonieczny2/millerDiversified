from django.db import models
from django.contrib.auth.models import User

#Model for user of site
class UserProfile(models.Model):
	#Links the user profile to instance of User
	user= models.OneToOneField(User)

	#Add other behavior here

	def __unicode__(self):
		return self.user.username

#Model for a Company
class Company(models.Model):
	company_name = models.CharField(max_length=200)


#Model for a contractor/contact/manager
class Person(models.Model):
	person_first_name = models.CharField(max_length=200)
	person_last_name = models.CharField(max_length=200)
	works_for = models.ForeignKey(Company) #on_delete=models.CASCADE


#Model for phone numbers; applies ONLY to a person

#Helper class field to choose type of phone number
class PhoneTypeField(models.Field):
	description = 'Choose Work, Home, or Cell'

	def __init__(self, *args, **kwargs):
		kwargs['choices'] = [
			(1,'Work'),
			(2, 'Home'),
			(3,'Cell')
		]
		super(PhoneTypeField, self).__init__(*args, **kwargs)

class Phone(models.Model):
	phone_no = models.IntegerField()
	phone_owner = models.ForeignKey(Person, on_delete = models.CASCADE)
	phone_type = PhoneTypeField()
