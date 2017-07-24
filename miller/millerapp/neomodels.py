from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
    UniqueIdProperty, RelationshipTo, RelationshipFrom , DateProperty , StructuredRel)
from neomodel.cardinality import OneOrMore , ZeroOrMore

class TestNode(StructuredNode):
	code = StringProperty()

#Abstract base class for all concepts.
#Root of metadata hierarchy.
class Structure(StructuredNode):
	#PROPERTIES
	
	#Cannot be unique in case users want to share models with same name
	name = StringProperty(index = True, required = True)
	created_date = DateProperty(required = True , default_now = True)
	description = StringProperty(index = True , required = True)
	#GUID generated programatically
	ID = StringProperty(unique_index = True , required = True)

	#RELATIONSHIPS

	branch = RelationshipTo( 'Branch' , 'HAS_BRANCH' , OneOrMore)
	
#Branch class, defines git-style branch of a Structure.
class Branch(StructuredNode):
	#PROPERTIES	
	
	name = StringProperty(index = True , required = True)
	created_date = DateProperty(required = True , default_now = True)
	reason_for_branch = StringProperty(index = True , required = True)
	ID = StringProperty(unqiue_index = True , required = True)

	#RELATIONSHIPS
	
	initial_commit = RelationshipTo('Commit' , 'INITIAL_COMMIT' , OneOrMore)



#Child Relationship class.  Used to define details of a Child relationship.
class ChildRelationship(StructuredRel):
	relationship_name = StringProperty(required = True)
	ID = StringProperty(required = True)

	#Parent and child class names
	parent_class_name = StringProperty()
	child_class_name = StringProperty()

	#Parent and child classes
	parent_class = RelationshipTo('Structure' , 'CHILD_RELATIONSHIP_PARENT_CLASS' , OneOrMore)
	child_class = RelationshipTo('Structure' , 'CHILD_RELATIONSHIP_CHILD_CLASS' , OneOrMore)

	
#Commit class.  All Branches must have at least one.
#Stores records of all changes made to a Branch.
#Can link to other Commits via prev_commit or next_commit
class Commit(StructuredNode):
	#PROPERTIES
	
	name = StringProperty(index = True , required = True)
	created_date = DateProperty(required = True , default_now = True)
	commit_message = StringProperty(index = True , required = True)
	ID = StringProperty(unique_index = True , required = True)

	#RELATIONSHIPS

	previous_commit = RelationshipTo('Commit' , 'PREV_COMMIT' , ZeroOrMore)
	next_commit = RelationshipTo('Commit' , 'NEXT_COMMIT' , ZeroOrMore)
	#Child link.  Must link to a SPECIFIC COMMIT of another class.
	child = RelationshipTo('COMMIT' , 'HAS_CHILD' , ZeroOrMore , model = ChildRelationship)

