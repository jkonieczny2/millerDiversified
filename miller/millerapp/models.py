from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, EmailValidator
from django.dispatch import receiver


#CREATE DATA MODELS HERE

#Model for user of site
class UserProfile(models.Model):
	#Links the user profile to instance of User
	user = models.OneToOneField(User)

	#Add other behavior here

	def __unicode__(self):
		return self.user.username

#Model for Company
class Company(models.Model):
	company_name = models.CharField(max_length=200)
	company_website = models.URLField(max_length=200, null=True)

#Model for a contractor/contact/manager, all of which are Entity
class Person(models.Model):
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	employer = models.ForeignKey(
		Company,
		models.SET_NULL,
		blank=True,
		null=True
		) #on_delete=models.CASCADE
	title = models.CharField(max_length=100, default='employee')

#Phone, Email, Address classes.  Apply to all Entities.
#Helper class field to choose type of phone number
'''
class PhoneTypeField(models.Field):
	description = 'Choose Work, Home, or Cell'

	def __init__(self, *args, **kwargs):
		kwargs['choices'] = [
			(1, 'Work'),
			(2, 'Home'),
			(3, 'Cell')
		]
		super(PhoneTypeField, self).__init__(*args, **kwargs)
#Helper field to choose state
class StateField(models.Field):
	description = 'Limits choices to the 50 U.S. States'

	def __init__(self, *args, **kwargs):
		kwargs['choices'] = [
			("AK","Alaska"),("AL","Alabama"),("AR","Arkansas"),("AZ","Arizona"),("CA","California"),
			("CO","Colorado"),("CT","Connecticut"),("DE","Delaware"),("FL","Florida"),("GA","Georgia"),
			("HI","Hawaii"),("IA","Iowa"),("ID","Idaho"),("IL","Illinois"),("IN","Indiana"),
			("KS","Kansas"),("KY","Kentucky"),("LA","Louisiana"),("MA","Massachusetts"),("MD","Maryland"),
			("ME","Maine"),("MI","Michigan"),("MN","Minnesota"),("MO","Missouri"),("MS","Mississippi"),
			("MT","Montana"),("NC","North Carolina"),("ND","North Dakota"),("NE","Nebraska"),("NH","New Hampshire"),
			("NJ","New Jersey"),("NM","New Mexico"),("NV","Nevada"),("NY","New York"),("OH","Ohio"),("OK","Oklahoma"),
			("OR","Oregon"),("PA","Pennsylvania"),("RI","Rhode Island"),("SC","South Carolina"),("SD","South Dakota"),
			("TN","Tennessee"),("TX","Texas"),("UT","Utah"),("VA","Virginia"),("VT","Vermont"),("WA","Washington"),
			("WI","Wisconsin"),("WV","West Virginia"),("WY","Wyoming"),("DC","District of Columbia"),
		]

		super(StateField, self).__init__(*args, **kwargs)
'''

class Phone(models.Model):
	PHONE_CHOICES = [
			(1, 'Work'),
			(2, 'Home'),
			(3, 'Cell')
		]


	phone_no = models.CharField(
		max_length=14,
		validators=[RegexValidator(regex='^(\d{1}-)?(\d{3}-\d{3}-\d{4})$',
		message='Invalid phone numer')]
		)

	person = models.ForeignKey(Person, on_delete = models.CASCADE)

	phone_type = models.IntegerField(choices=PHONE_CHOICES,
		default=1,
		)

	contact_name = models.CharField(max_length=100, null=True)

class CompanyPhone(models.Model):
	PHONE_CHOICES = [
			(1, 'Work'),
			(2, 'Home'),
			(3, 'Cell')
		]

	phone_no = models.CharField(
		max_length=14,
		validators=[RegexValidator(regex='^(\d{1}-)?(\d{3}-\d{3}-\d{4})$',
		message='Invalid phone numer')]
		)
	company = models.ForeignKey(Company, on_delete = models.CASCADE)
	phone_type = models.IntegerField(choices=PHONE_CHOICES, default=1)
	contact_name = models.CharField(max_length=100, null=True)

class Email(models.Model):
	person = models.ForeignKey(Person, on_delete=models.CASCADE)
	email = models.CharField(
		max_length=200,
		validators=[EmailValidator()]
		)

class CompanyEmail(models.Model):
	company = models.ForeignKey(Company, on_delete=models.CASCADE)
	email = models.CharField(
		max_length=200,
		validators=[EmailValidator()]
		)


class Address(models.Model):
	STATES = [
			("AK","Alaska"),("AL","Alabama"),("AR","Arkansas"),("AZ","Arizona"),("CA","California"),
			("CO","Colorado"),("CT","Connecticut"),("DE","Delaware"),("FL","Florida"),("GA","Georgia"),
			("HI","Hawaii"),("IA","Iowa"),("ID","Idaho"),("IL","Illinois"),("IN","Indiana"),
			("KS","Kansas"),("KY","Kentucky"),("LA","Louisiana"),("MA","Massachusetts"),("MD","Maryland"),
			("ME","Maine"),("MI","Michigan"),("MN","Minnesota"),("MO","Missouri"),("MS","Mississippi"),
			("MT","Montana"),("NC","North Carolina"),("ND","North Dakota"),("NE","Nebraska"),("NH","New Hampshire"),
			("NJ","New Jersey"),("NM","New Mexico"),("NV","Nevada"),("NY","New York"),("OH","Ohio"),("OK","Oklahoma"),
			("OR","Oregon"),("PA","Pennsylvania"),("RI","Rhode Island"),("SC","South Carolina"),("SD","South Dakota"),
			("TN","Tennessee"),("TX","Texas"),("UT","Utah"),("VA","Virginia"),("VT","Vermont"),("WA","Washington"),
			("WI","Wisconsin"),("WV","West Virginia"),("WY","Wyoming"),("DC","District of Columbia"),
		]

	person = models.ForeignKey(Person, on_delete = models.CASCADE)

	street_1 = models.CharField(max_length=200)
	street_2 = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=2, choices=STATES)
	zip_code = models.CharField(max_length=16)

class CompanyAddress(models.Model):
	STATES = [
			("AK","Alaska"),("AL","Alabama"),("AR","Arkansas"),("AZ","Arizona"),("CA","California"),
			("CO","Colorado"),("CT","Connecticut"),("DE","Delaware"),("FL","Florida"),("GA","Georgia"),
			("HI","Hawaii"),("IA","Iowa"),("ID","Idaho"),("IL","Illinois"),("IN","Indiana"),
			("KS","Kansas"),("KY","Kentucky"),("LA","Louisiana"),("MA","Massachusetts"),("MD","Maryland"),
			("ME","Maine"),("MI","Michigan"),("MN","Minnesota"),("MO","Missouri"),("MS","Mississippi"),
			("MT","Montana"),("NC","North Carolina"),("ND","North Dakota"),("NE","Nebraska"),("NH","New Hampshire"),
			("NJ","New Jersey"),("NM","New Mexico"),("NV","Nevada"),("NY","New York"),("OH","Ohio"),("OK","Oklahoma"),
			("OR","Oregon"),("PA","Pennsylvania"),("RI","Rhode Island"),("SC","South Carolina"),("SD","South Dakota"),
			("TN","Tennessee"),("TX","Texas"),("UT","Utah"),("VA","Virginia"),("VT","Vermont"),("WA","Washington"),
			("WI","Wisconsin"),("WV","West Virginia"),("WY","Wyoming"),("DC","District of Columbia"),
		]

	company = models.ForeignKey(Company, on_delete = models.CASCADE)

	street_1 = models.CharField(max_length=200)
	street_2 = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=2, choices=STATES)
	zip_code = models.CharField(max_length=16)
