from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
    UniqueIdProperty, RelationshipTo, RelationshipFrom , DateProperty , StructuredRel , DateTimeProperty)
from neomodel.cardinality import OneOrMore , ZeroOrMore , One

try:
	from millerapp.neomodels import *
except ImportError:
	from neomodels import *

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


#HEAD relationship, connects Branch to current HEAD commit
class HEAD(StructuredRel):
	branch = RelationshipTo('Branch' , 'HEAD_BRANCH' , One)
	commit  = RelationshipTo('Commit' , 'HEAD_COMMIT' , One)

