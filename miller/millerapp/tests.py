from django.test import TestCase
import factory.django, random
from millerapp.models import Person, Company
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
		person = PersonFactory(employer = comp)

		#Trace person's employer attributes
		peeps = Person.objects.all()
		only_person = peeps[0]

		self.assertEqual(only_person.employer.company_name , "Miller Diversified")
		self.assertEqual(only_person.employer.company_website , "http://www.millerdiversified.com")


class CompanyTest(TestCase):

	def test_create_company(self):
		comp = CompanyFactory()

		all_comps=Company.objects.all()
		self.assertEqual(len(all_comps),1)
		only_comp=all_comps[0]
		self.assertEqual(only_comp, comp)

		self.assertEqual(only_comp.company_name, "Miller Diversified")
		self.assertEqual(only_comp.company_website, "http://www.millerdiversified.com")





		



