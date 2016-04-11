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
	class Meta:
		verbose_name = 'Company'
		verbose_name_plural = 'Companies'

	company_name = models.CharField(max_length=200)
	company_website = models.URLField(max_length=200, null=True)

	def __str__(self):
		return self.company_name

#Model for a contractor/contact/manager
class Person(models.Model):
	class Meta:
		verbose_name = 'Person'
		verbose_name_plural = 'People'

	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	employer = models.ForeignKey(
		Company,
		models.SET_NULL,
		blank=True,
		null=True
		) #on_delete=models.CASCADE
	title = models.CharField(max_length=100, null=True, blank=True)

	def __str__(self):
		fullname = "%s %s"%(self.first_name, self.last_name)
		return fullname

#Phone, Email, Address classes.
class Phone(models.Model):
	PHONE_CHOICES = [
			(1, 'Work'),
			(2, 'Home'),
			(3, 'Cell'),
			(4, 'Fax')
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

	def __str__(self):
		return self.phone_no

class CompanyPhone(models.Model):
	class Meta:
		verbose_name = 'Company Phone'
		verbose_name_plural = 'Company Phones'

	PHONE_CHOICES = [
			(1, 'Work'),
			(2, 'Home'),
			(3, 'Cell'),
			(4, 'Fax')
		]

	phone_no = models.CharField(
		max_length=14,
		validators=[RegexValidator(regex='^(\d{1}-)?(\d{3}-\d{3}-\d{4})$',
		message='Invalid phone numer')]
		)
	company = models.ForeignKey(Company, on_delete = models.CASCADE)
	phone_type = models.IntegerField(choices=PHONE_CHOICES, default=1)
	contact_name = models.CharField(max_length=100, null=True, blank=True)

	def __str__(self):
		return self.phone_no

class Email(models.Model):
	person = models.ForeignKey(Person, on_delete=models.CASCADE)
	email = models.CharField(
		max_length=200,
		validators=[EmailValidator()]
		)

	def __str__(self):
		return self.email

class CompanyEmail(models.Model):
	class Meta:
		verbose_name = 'Company Email'
		verbose_name_plural = 'Company Emails'

	company = models.ForeignKey(Company, on_delete=models.CASCADE)
	email = models.CharField(
		max_length=200,
		validators=[EmailValidator()]
		)
	contact_name = models.CharField(max_length = 50, null=True, blank=True)

	def __str__(self):
		return self.email


class Address(models.Model):
	class Meta:
		verbose_name = 'Address'
		verbose_name_plural = 'Addresses'

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
	street_2 = models.CharField(max_length=100, null=True, blank=True)
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=2, choices=STATES)
	zip_code = models.CharField(max_length=16)

	def __str__(self):
		full_address = "%s %s"%(self.street_1, self.street_2)
		return full_address

class CompanyAddress(models.Model):
	class Meta:
		verbose_name = 'Company Address'
		verbose_name_plural = 'Company Addresses'

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
	street_2 = models.CharField(max_length=100, null=True, blank=True)
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=2, choices=STATES)
	zip_code = models.CharField(max_length=16)

	def __str__(self):
		full_address = "%s %s"%(self.street_1, self.street_2)
		return full_address

#Model for Projects
class Project(models.Model):
	#Choices
	STATUS_CHOICES = [
		(1, 'On Hold'),
		(2, 'Construction'),
		(3, 'PreConstruction'),
		(4, 'Prospect'),
		(5, 'Bidding to Subtrades'),
		(6, 'Project on Hold'),
		(7, 'Project Awarded'),
		(8, 'Design Phase'),
		(9, 'Estimating')
	]

	name = models.CharField(max_length = 100)
	size = models.IntegerField(null = True, blank = True)
	status = models.IntegerField(choices = STATUS_CHOICES, blank = True)
	owner = models.ForeignKey(Person, related_name = 'project_owner')
	architect = models.ForeignKey(Person, related_name = 'project_architect')

	def __str__(self):
		return self.name

class ProjectManagers(models.Model):
	class Meta:
		verbose_name = 'Project Manager'
		verbose_name_plural = 'Project Managers'

	ROLE_CHOICES = [
		(1, 'Manager'),
		(2, 'Superintendent'),
		(3, 'Coordinator'),
		(4, 'Estimator'),
	]

	project = models.ForeignKey(Project, default = 0)
	person = models.ForeignKey(Person)
	role = models.IntegerField(choices = ROLE_CHOICES)

class ProjectAddress(models.Model):
	class Meta:
		verbose_name = 'Project Address'
		verbose_name_plural = 'Project Address'

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

	project = models.OneToOneField(Project, on_delete = models.CASCADE)

	street_1 = models.CharField(max_length=200)
	street_2 = models.CharField(max_length=100, null=True, blank=True)
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=2, choices=STATES)
	zip_code = models.CharField(max_length=16)

	def __str__(self):
		full_address = "%s %s"%(self.street_1, self.street_2)
		return full_address

#Classes for project elements
