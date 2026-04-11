#Método de Euler
def Euler(f, a, b, N, x0):
  h = (b - a) / N

  tpontos = np.arange(a, b, h)
  xpontos = []
  x=x0

  for t in tpontos:
      xpontos.append(x)   # salva o valor atual
      x += h * f(x, t)
  return tpontos, xpontos
