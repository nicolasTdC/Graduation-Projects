import autograd.numpy
from autograd import grad
from autograd import hessian
import numpy as np

#Funcoes para teste
def quadratica(x):
  f=0
  for i in range(1, len(x) + 1):
      f+= (i) * x[i-1] ** 2
  return f

def rosenbrook(x):
  f=0
  for i in range(1,  int(len(x)/2) + 
                 1):
    f+= 10 * (x[2*(i-1)] - x[2*(i-1) - 1] ** 2) ** 2 + (x[2*(i-1) - 1] - 1) ** 2
  return f

def styblinsk_tang(x):
  f = 0
  for i in range(1, len(x) + 1):
    f +=  x[i-1] ** 4 - 16 *  x[i-1] ** 2 + 5 * x[i-1]
  return f

def rastringin(x):
  f = 0
  for i in range(1, len(x) + 1):
    f += x[i-1] ** 2 - 10 * autograd.numpy.cos(2 * np.pi * x[i-1])
  return f

# Metodos
def metodo_gradiente(x_0, f, epsilon, alpha = 10e-4, sigma = 0.5, M = 300):
  k = 0
  x_k = x_0
  n= len(x_0)
  grad_f = grad(f)
  while ( np.linalg.norm(grad_f(x_k)) >= epsilon and k < M):
    d_k = np.array([- grad_f(x_k)[i] for i in range(n) ])
    t_k = 1
    while (f(x_k + t_k*d_k) > f(x_k) + alpha*t_k*np.inner(grad_f(x_k), d_k)):
      t_k = sigma*t_k
    x_k = x_k + t_k*d_k
    k = k + 1
  return x_k, k

def metodo_newton(x_0, f, epsilon, alpha=1e-4, beta=1e-3, gama=1e-6, sigma=0.5, rho=1e-3, M = 300):
    k = 0
    x_k = x_0
    n = len(x_0)
    grad_f = grad(f)
    hess_f = hessian(f)
    norma_grad = np.linalg.norm(grad_f(x_k))
    while (norma_grad >= epsilon and k < M):
        
        u = 0
        A = hess_f(x_k) + u * np.identity(n)
        b = np.array([- grad_f(x_k)[i] for i in range(n) ])
        flag = 0
        while flag == 0:
            try:
                d_k = np.linalg.solve(A, b)
                norma_d_k = np.linalg.norm(d_k)
                if (np.inner(grad_f(x_k), d_k) > -gama * norma_grad * norma_d_k):
                    u = max(2 * u, rho)
                    A = hess_f(x_k) + u * np.identity(len(x_k))
                else:
                    flag = 1
            except:
                u = max(2 * u, rho)
        norma_d_k = np.linalg.norm(d_k)
        if norma_d_k < beta * norma_grad:
            d_k = (beta * (norma_grad / norma_d_k)) * d_k
        t_k = 1
        while (f(x_k + t_k * d_k) > f(x_k) + alpha * t_k * np.inner(grad_f(x_k), d_k)):
            t_k = sigma * t_k
        x_k = x_k + t_k * d_k
        k = k + 1
        norma_grad = np.linalg.norm(grad_f(x_k))
    return x_k, k

def metodo_secante_c_posto1(x_0, f, epsilon, gama = 1e-6, beta = 1e-3, alpha = 10e-4, sigma = 0.5, M = 300):
  n = len(x_0)
  k = 0
  x_k = x_0
  H_k = np.identity(n)

  grad_f = grad(f)
  d_k = -np.dot(H_k, grad_f(x_k))
  norma_grad = np.linalg.norm(grad_f(x_k))
  norma_d_k = np.linalg.norm(d_k)
  while (norma_grad >= epsilon and k < M):
    if (np.inner(grad_f(x_k), d_k) > -gama * norma_grad * norma_d_k):
      d_k = -grad_f(x_k)
      H_k = np.identity(n)
    if (norma_d_k < beta*norma_grad):
      d_k = beta*(norma_grad/norma_d_k)*d_k
         
    t_k = 1
    while (f(x_k + t_k*d_k) > f(x_k) + alpha*t_k*np.inner(grad_f(x_k), d_k)):
      t_k = sigma*t_k
  
    x_kk = x_k + t_k*d_k
    k = k + 1
  
    s_k = t_k*d_k
    y_k = grad_f(x_kk) - grad_f(x_k)
    z_k = np.dot(H_k, y_k)
    w_k = s_k - z_k
    
    if (np.inner(w_k, y_k) > 0):
      H_k = H_k + np.matmul(w_k, np.transpose(w_k))/np.inner(w_k, y_k)
    else:
      H_k = H_k
  
    x_k = x_kk
    norma_grad = np.linalg.norm(grad_f(x_k))
  return x_k, k
  
  
def metodo_secante_DFP( x_0, f, epsilon, gama = 1e-6, beta = 1e-3, alpha = 10e-4, sigma = 0.5, M = 300):
  k = 0
  n = len(x_0)
  x_k = x_0
  H_k = np.identity(n)
  grad_f = grad(f)
  d_k = -np.dot(H_k, grad_f(x_k))
  norma_grad = np.linalg.norm(grad_f(x_k))
  norma_d_k = np.linalg.norm(d_k)
  while (norma_grad >= epsilon and k < M):
    if (np.inner(grad_f(x_k), d_k) > -gama * norma_grad * norma_d_k):
      d_k = -grad_f(x_k)
      H_k = np.identity(n)
    if (norma_d_k < beta*norma_grad):
      d_k = beta*(norma_grad/norma_d_k)*d_k

    t_k = 1
    while (f(x_k + t_k*d_k) > f(x_k) + alpha*t_k*np.inner(grad_f(x_k), d_k)):
      t_k = sigma*t_k

    x_kk = x_k + t_k*d_k
    k = k + 1

    s_k = t_k*d_k
    y_k = grad_f(x_kk) - grad_f(x_k)
    z_k = np.dot(H_k, y_k)
    w_k = s_k - z_k

    if (np.inner(w_k, y_k) > 0):
      H_k = H_k + np.matmul(s_k, np.transpose(s_k))/np.inner(s_k, y_k) - np.matmul(z_k, np.transpose(z_k))/np.inner(z_k, y_k)
    else:
      H_k = H_k

    x_k = x_kk
    norma_grad = np.linalg.norm(grad_f(x_k))
  return x_k, k