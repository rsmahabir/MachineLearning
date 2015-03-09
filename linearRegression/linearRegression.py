import numpy as np 
from sklearn import linear_model

def loadTrainData():
	f = open('abalone.txt','rb')
	train_data = []
	values = []
	for line in f:
		line = line.strip().split('\t')
		line = [float(x) for x in line]
		train_data.append(line[:-1])
		values.append(line[-1])
	return train_data,values

class SingularError(StandardError):
	pass

class LinearRegression():
	def __init__(self,alpha = 0.1,epochs = 50,method = 'sgd'):
		self.weights = None
		self.bias = 1.0
		self.alpha = alpha
		self.epochs = epochs
		self.method = method

	def error(self,predict,y):
		return ((predict - y) ** 2).sum()

	def predict(self,test_data):
		if self.method == 'sgd':
			result = np.dot(test_data,self.weights) + self.bias
		else:
			result = np.dot(test_data,self.weights)
		return result

	def __StandRegress(self,train_data,values):
		xTx = np.dot(train_data.T,train_data)
		if np.linalg.det(xTx) == 0.0:
			raise SingularError('This matrix is singular, cannot do inverse')
		self.weights = np.dot(np.dot(np.linalg.inv(xTx),train_data.T),values)

	def __SGD(self,train_data,values):
		"""
		stochastic gradient descent
		"""
		for i in xrange(self.epochs):
			for x,y in zip(train_data,values):
				error = np.dot(self.weights.T,x) + self.bias - y
				nabla_b = error
				nabla_w = error * x

				self.weights = self.weights - self.alpha * nabla_w
				self.bias = self.bias - self.alpha * nabla_b

			predictResult = self.predict(train_data)
			diff = ((values - predictResult) ** 2).sum()
			print 'epoch {0}, diff is :{1}'.format(i,diff)

	def fit(self,train_data,values):
		if self.method != 'sgd':
			for x in train_data:
				x.append(1.0)
		#convert list objects to numpy array
		train_data = np.array(train_data)
		m,n = train_data.shape
		values = np.array(values)

		#self.weights = np.random.randn(n,)
		self.weights = np.ones((n,))

		if self.method == 'sgd':
			self.__SGD(train_data,values)
		else:
			try:
				self.__StandRegress(train_data,values)
			except SingularError,e:
				print e
				self.__SGD(train_data,values)
		print 'Weights are :{0} ,by {1} method'.format(self.weights,self.method)
		print 'Bias is:{0}'.format(self.bias)

train_data,y = loadTrainData()
lr = LinearRegression(method='std')
lr.fit(train_data,y)

py = lr.predict(train_data)
error = lr.error(py,y)
print 'STD error is:{0}'.format(error)

train_data1,y1 = loadTrainData()
lrSGD = LinearRegression()
lrSGD.fit(train_data1,y1)

pySGD = lrSGD.predict(train_data1)
errorSGD = lrSGD.error(pySGD,y1)
print 'SGD error is:{0}'.format(errorSGD)

clf = linear_model.LinearRegression()
clf.fit(train_data1,y1)
pyCLF = clf.predict(train_data1)
errorpyCLF = lr.error(pyCLF,y1)
print clf.coef_
print errorpyCLF