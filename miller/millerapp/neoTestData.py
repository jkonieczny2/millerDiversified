from millerapp.neomodels import Structure , Branch , Commit
from datetime import datetime

#Create Project structure
project = Structure(name = 'Project' , ID='PROJECT1' , description = "A MD construction project")
project.save()

#Create a couple of Branches for the project
branch1 = Branch(name = 'Branch 1' , ID = 'PROJECT1_BRANCH1' , reason_for_branch = "Initial Branch")
branch2 = Branch(name = 'Branch 2' , ID = 'PROJECT1_BRANCH2' , reason_for_branch = "Second Branch") #If using same ID, want to make sure it breaks
branch1.save()
branch2.save()

#Link branches to project
project.branch.connect(branch1)
project.branch.connect(branch2)

#Create a couple of Commits (actually gets tricky with 2 branches and 2 commits)
commit1 = Commit(name = "Initial Commit" , ID = "PROJECT1_BRANCH1_COMMIT1" , commit_message='initial commit')
commit2 =  Commit(name = "Second Commit" , ID = "PROJECT1_BRANCH1_COMMIT2" , commit_message='second commit')
commit1.save()
commit2.save()

#Link initial to Branch 1 (for now)
#Will actually need to copy commit history for all branches!
#Would expect this to break trying to connect 2 nodes to this prop
branch1.initial_commit.connect(commit1)
branch1.current_commit.connect(commit2)

#Link second commit to first commit and VV
commit1.next_commit.connect(commit2)
commit2.previous_commit.connect(commit1)


