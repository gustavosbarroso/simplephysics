#Imports
import numpy as np
import matplotlib.pyplot as plt
#Função
def f(x):
  return np.exp(-x**2) #função de exemplo, podendo ser qualquer outra
#Integração
def integraTrapezio(f, a, b, N):
  h=(b-a)/N
  s=0.5*(f(a) + f(b))
  for k in range (1,N):
    s+= f(a+ k*h)
  return h*s
#Resultado
print(f": {integraTrapezio(f,0, 3, 100):.4f}") 
