class Calc: 

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def add(self):
        return self.a + self.b

    def dif(self):
        return self.a - self.b

    def seki(self):
        return self.a*self.b

    def shou(self):
        if self.b == 0:
            return "Not Devide!"
        else:
            return self.a/self.b

    def lotOfParam(a,b,c,d,e,f,g,h,i,j,k,l,m,n):
	return a+b+c+d+e+f+g
