from django.test import TestCase
import factory.django, random
from millerapp.models import Person, Company, Phone, Email, Address
#import factory
# Create your tests here.

#Test for the Person model

class CompanyFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Company
		django_get_or_create = ('company_name',
			'company_website',
			)
		abstract = False

	company_name='Miller Diversified'
	company_website='http://www.millerdiversified.com'

class PersonFactory(factory.django.DjangoModelFactory):

	class Meta:
		model = Person
		django_get_or_create = ('first_name',
			'last_name',
			'title',
			'employer'
			)
		abstract = False
	
	first_name='Joshua'
	last_name='Konieczny'
	title='CEO, bitch'
	employer = CompanyFactory()

	'''
	@classmethod
	def _prepare(cls, create, **kwargs):
		pers = super(PersonFactory, cls)._prepare(create, **kwargs)
		pers.employer.add(CompanyFactory())
		return pers
	'''

class PhoneFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Phone
		django_get_or_create = (
				'phone_no',
				'person',
				'phone_type',
			)

	phone_no = "555-555-5555"
	phone_type = 1
	person = PersonFactory()

class AddressFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Address

		django_get_or_create = (
				'street_1',
				'street_2',
				'city',
				'state',
				'zip_code',
				'person'
			)

	street_1 = '330A Highland Ave'
	street_2 = 'Apartment 3'
	city = 'Somerville'
	state = 'MA'
	zip_code = '02144'

class EmailFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Email

		django_get_or_create = (
				'email',
				'person',
			)

	person = PersonFactory()
	email = 'joshua.konieczny@gmail.com'


class PersonTest(TestCase):
	def test_create_person(self):

		person = PersonFactory()

		# Check we can find it
		all_people = Person.objects.all()
		self.assertEqual(len(all_people), 1)
		only_person = all_people[0]
		self.assertEqual(only_person, person)
		# Check attributes
		self.assertEqual(only_person.first_name, 'Joshua')
		self.assertEqual(only_person.last_name, 'Konieczny')
		self.assertEqual(only_person.title, 'CEO, bitch')

	def test_create_person_with_employer(self):	
		#Create a person with an employer
		comp = CompanyFactory()
		person = PersonFactory(first_name="Joshua", last_name="Konieczny", title="CEO, bitch", employer = comp)

		#Trace person's employer attributes
		peeps = Person.objects.all()
		only_person = peeps[0]

		self.assertEqual(only_person.employer.company_name , "Miller Diversified")
		self.assertEqual(only_person.employer.company_website , "http://www.millerdiversified.com")

		#Test that only one company was created
		comps = Company.objects.all()
		self.assertEqual(len(comps), 1)

	def test_create_multiple_employees(self):
		comp = CompanyFactory()
		person1 = PersonFactory(first_name="Joshua", last_name="Konieczny", title="CEO, bitch", employer = comp)
		person2 = PersonFactory(first_name="Claire", last_name="Konieczny", title="Manager", employer = comp)

		#Trace person's employer attributes
		peeps = Person.objects.all()

		self.assertEqual(len(peeps),2)

		self.assertEqual(peeps[0].employer.company_name , "Miller Diversified")
		self.assertEqual(peeps[0].employer.company_website , "http://www.millerdiversified.com")

		self.assertEqual(peeps[1].employer.company_name , "Miller Diversified")
		self.assertEqual(peeps[1].employer.company_website , "http://www.millerdiversified.com")

		#Test that only one company was created
		comps = Company.objects.all()
		self.assertEqual(len(comps), 1)

class CompanyTest(TestCase):

	def test_create_company(self):
		comp = CompanyFactory()

		all_comps=Company.objects.all()
		self.assertEqual(len(all_comps),1)
		only_comp=all_comps[0]
		self.assertEqual(only_comp, comp)

		self.assertEqual(only_comp.company_name, "Miller Diversified")
		self.assertEqual(only_comp.company_website, "http://www.millerdiversified.com")

class PhoneTest(TestCase):
	def test_create_phone_number(self):
		#Set up phone with all relationships
		comp = CompanyFactory()
		person = PersonFactory(employer = comp)
		phone = PhoneFactory(person = person)

		#Test that it appears
		phones = Phone.objects.all()
		only_phone = phones[0]

		self.assertEqual(len(phones), 1)
		self.assertEqual(phones[0], phone)
		self.assertEqual(only_phone.phone_no, '555-555-5555')
		self.assertEqual(only_phone.phone_type, 1)
		#self.assertEqual(only_phone.contact_name, None)

		#Test that Person relationship worked
		self.assertEqual(only_phone.person.first_name , 'Joshua')
		self.assertEqual(only_phone.person.last_name , 'Konieczny')
		self.assertEqual(only_phone.person.title , 'CEO, bitch')

		#Test that the Employer relationship worked
		self.assertEqual(only_phone.person.employer.company_name , "Miller Diversified")
		self.assertEqual(only_phone.person.employer.company_website , "http://www.millerdiversified.com")

	def test_invalid_phone(self):
		#Try to set up phone with bad number
		phone = PhoneFactory(phone_no = '55-555-5555')
		self.assertEqual(phone.phone_no, '55-555-5555')
		#Django doesn't enforce this when the entry is saved!


class AddressTest(TestCase):
	def test_create_address(self):
		comp = CompanyFactory()
		person = PersonFactory(employer = comp)
		address = AddressFactory(person = person)

		#Check that address was created
		addresses = Address.objects.all()
		only_address = Address.objects.all()[0]

		self.assertEqual(len(addresses), 1)
		self.assertEqual(only_address, address)
		self.assertEqual(only_address.street_1, '330A Highland Ave')
		self.assertEqual(only_address.street_2, 'Apartment 3')
		self.assertEqual(only_address.city, 'Somerville')
		self.assertEqual(only_address.zip_code, '02144')

		#Check that person relationship worked
		self.assertEqual(only_address.person.first_name, 'Joshua')
		self.assertEqual(only_address.person.last_name, 'Konieczny')
		self.assertEqual(only_address.person.title, 'CEO, bitch')

		#Check that company relationship worked
		self.assertEqual(only_address.person.employer.company_name, 'Miller Diversified')
		self.assertEqual(only_address.person.employer.company_website, 'http://www.millerdiversified.com')


class EmailTest(TestCase):
	def test_create_email(self):
		comp = CompanyFactory()
		person = PersonFactory(employer = comp)
		email = EmailFactory(person = person)

		emails = Email.objects.all()
		only_email = emails[0]

		#Test that email was created correctly
		self.assertEqual(only_email.email, 'joshua.konieczny@gmail.com')

		#Test person relationship
		self.assertEqual(only_email.person.first_name, 'Joshua')
		self.assertEqual(only_email.person.last_name, 'Konieczny')
		self.assertEqual(only_email.person.title, 'CEO, bitch')

		#Test Company relationship
		self.assertEqual(only_email.person.employer.company_name, "Miller Diversified")
		self.assertEqual(only_email.person.employer.company_website, 'http://www.millerdiversified.com')






		



