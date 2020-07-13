## Autograd: a program for automatic differentiation

**Description:** Implementation of a small-scale automatic differentiation framework, like PyTorch and Tensorflow.

The functions for the experiment are as follows:

<img src="https://latex.codecogs.com/gif.latex?x=2"/>

<img src="https://latex.codecogs.com/gif.latex?y=5"/>

<img src="https://latex.codecogs.com/gif.latex?z=x*y"/>

<img src="https://latex.codecogs.com/gif.latex?v=1+2*z"/>

```javascript
x = Variable(2)
y = Variable(5)
z = x*y
v = 1+2*z
v.derivative(z) # evaluates dv/dz = 2
v.derivative(y) # evaluates dv/dy = 5
v.derivative(x) # evaluates dv/dx = 10
```
Various rules of differentiation are implemented as follows:

- d.mul: <img src="https://latex.codecogs.com/gif.latex?z=y_{1}.y_{2}"/>

<img src="https://latex.codecogs.com/gif.latex?\frac{dz}{dx}=(\frac{dy_{1}}{dx}).y_{2}+y_{1}.(\frac{dy_{2}}{dx})"/>

- d.truediv: <img src="https://latex.codecogs.com/gif.latex?z=\frac{y_{1}}{y_{2}}"/>

<img src="https://latex.codecogs.com/gif.latex?\frac{dz}{dx}=\frac{(\frac{dy_{1}}{dx}).y_{2}-y_{1}.(\frac{dy_{2}}{dx})}{(y_{2})^2}"/>

- d.pow: <img src="https://latex.codecogs.com/gif.latex?z=(y_{1})^{y_{2}}"/>

Assuming <img src="https://latex.codecogs.com/gif.latex?y_{1}>0"/>, <img src="https://latex.codecogs.com/gif.latex?\frac{dz}{dx}=y_{2}.(y_{1})^{y_{2}-1}.(\frac{dy_{1}}{dx})+(y_{1})^{y_{2}}.\ln{y_{1}}.(\frac{dy_{2}}{dx})"/>

When operand <img src="https://latex.codecogs.com/gif.latex?y_{1}\leq0"/>, the second term can be replaced with <img src="https://latex.codecogs.com/gif.latex?0"/>, otherwise <img src="https://latex.codecogs.com/gif.latex?\ln{y_{1}}"/> is not defined.

- d.tanh: <img src="https://latex.codecogs.com/gif.latex?z=\tanh({y_{1}})"/>

<img src="https://latex.codecogs.com/gif.latex?\frac{dz}{dx}=(1-(\tanh({y_{1}}))^{2}).(\frac{dy_{1}}{dx})"/>

- d.sin: <img src="https://latex.codecogs.com/gif.latex?z=\sin({y_{1}})"/>

<img src="https://latex.codecogs.com/gif.latex?\frac{dz}{dx}=\cos({y_{1}}).(\frac{dy_{1}}{dx})"/>

d.cos: <img src="https://latex.codecogs.com/gif.latex?z=\cos({y_{1}})"/>

<img src="https://latex.codecogs.com/gif.latex?\frac{dz}{dx}=-\sin({y_{1}}).(\frac{dy_{1}}{dx})"/>

- d.log: <img src="https://latex.codecogs.com/gif.latex?z=\log({y_{1}})"/>

<img src="https://latex.codecogs.com/gif.latex?\frac{dz}{dx}=\frac{1}{y_{1}}.(\frac{dy_{1}}{dx})"/>

Gradient descent is implemented as follows:

```javascript
gradient_descent(parameters, error_function, num_iters, learning_rate, verbose):
  errors = []
  for i in range(0,(num_iters-1)):
    e = error_function(parameters)
    append e to errors
    for p in parameters:
      p = p - learning_rate.grad(e)
    end for
    if verbose:
      print i and e
    end if
  end for
return errors
```
