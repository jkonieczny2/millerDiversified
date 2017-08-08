try:
	from neomodels import *
	from neoRelationships import *
except ImportError:
	from millerapp.neomodels import *
	from millerapp.neoRelationships import *

def makeNewCommit(branch , commit):
	#Make previous and next commit relationships
	current_head = branch.head.get_or_none()

	current_head.next_commit.connect(commit)
	commit.previous_commit.connect(current_head)
	
	#Reconnect HEAD to the new commit
	branch.head.reconnect(old_node = current_head , new_node = commit)



