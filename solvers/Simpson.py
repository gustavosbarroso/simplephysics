#Imports
import numpy as np
import matplotlib.pyplot as plt
#Função
def f(x):
  return np.exp(-x**2) #Função de exemplo, podendo ser qualquer outra
#Integração
def integraSimpson(f, a, b, N):
  h=(b-a)/N
  s=(f(a) + f(b))
  for k in range (1,N):
    if k%2==0:
      s+= 2*f(a + k*h)
    else:
      s+= 4*f(a + k*h)
  return (h*s)/3
#Resultado
print(f": {integraSimpson(f,0, 3, 100):.4f}")
