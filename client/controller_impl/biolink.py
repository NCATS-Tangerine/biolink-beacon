# Utility method for Biolink identifier management

class BiolinkTerm:

	def __init__(self,name):
                self.name = name
                self.objectId = ''.join(x for x in name.title() if x.isalpha())

	BIOLINK_PREFIX = "biolink"
	BIOLINK_BASEURI = "http://bioentity.io/vocab/"

	def prefix():
		return BiolinkTerm.BIOLINK_PREFIX

	def baseUri(): 
		return BiolinkTerm.BIOLINK_BASEURI

	def isCurie(id):
		return id.startswith(BiolinkTerm.BIOLINK_PREFIX+":") 

	def getCurieObjectId(curie):
		return curie[len(BiolinkTerm.BIOLINK_PREFIX)+1:]

	def objectId(self):
		return objectId 

	def curie(self):
		return BiolinkTerm.prefix()+":"+self.objectId 

	def uri(self):
		return BiolinkTerm.baseUri()+self.objectId

