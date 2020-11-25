import sys, os, json

class DB(object):
	def __init__(self, path):
		self.path = path
		if not os.path.exists(path):
			print('create DB')
			self.data = {
				"IAs": {},
				"INGs": {}
			}
			with open(path, 'w') as f:
				f.write(json.dumps(self.data, sort_keys=True, indent=4))
		else:
			print('read DB')
			with open(path, 'r') as f:
				self.data = json.load(f)

	def write(self, data):
		self.data = data
		with open(self.path, 'w+') as f:
			f.write(json.dumps(self.data, sort_keys=True, indent=4))

	def getContent(self):
		return self.data