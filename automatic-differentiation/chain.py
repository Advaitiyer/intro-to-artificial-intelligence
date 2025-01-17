import math

def d_neg(operands, v):
    """
    Operands is a singleton list [x]
    x is a Variable potentially dependent on v
    Evaluates the derivative of (-x) with respect to v
    Recursively uses the chain rule on x
    Returns the derivative as a float
    """
    return -operands[0].derivative(v)

def d_add(operands, v):
    """
    Operands is a list [x, y]
    x and y are Variables potentially dependent on v
    Evaluates the derivative of (x+y) with respect to v
    Recursively uses the chain rule on the operands
    Returns the derivative as a float
    """
    return operands[0].derivative(v) + operands[1].derivative(v)

def d_sub(operands, v):
    """
    Operands is a list [x, y]
    x and y are Variables potentially dependent on v
    Evaluates the derivative of (x-y) with respect to v
    Recursively uses the chain rule on the operands
    Returns the derivative as a float
    """
    return operands[0].derivative(v) - operands[1].derivative(v)

def d_mul(operands, v):
    """
    Operands is a list [x, y]
    x and y are Variables potentially dependent on v
    Evaluates the derivative of (x*y) with respect to v
    Recursively uses the chain rule on the operands
    Returns the derivative as a float
    """
    return operands[0].derivative(v) * operands[1].value+operands[0].value * operands[1].derivative(v)

def d_truediv(operands, v):
    """
    Operands is a list [x, y]
    x and y are Variables potentially dependent on v
    Evaluates the derivative of (x/y) with respect to v
    Recursively uses the chain rule on the operands
    Returns the derivative as a float
    """
    return (operands[0].derivative(v) * operands[1].value - operands[0].value * operands[1].derivative(v)) / ((operands[1].value) ** 2)

def d_pow(operands, v):
    """
    Operands is a list [x, y]
    x and y are Variables potentially dependent on v
    Evaluates the derivative of (x**y) with respect to v
    Recursively uses the chain rule on the operands
    Returns the derivative as a float
    """
    if (operands[0].value<0):
        return operands[1].value * ((operands[0].value) ** (operands[1].value-1)) * operands[0].derivative(v)
    else:
        return operands[1].value * ((operands[0].value) ** (operands[1].value-1)) * operands[0].derivative(v) + (operands[0].value) ** (operands[1].value) * math.log(operands[0].value) * operands[1].derivative(v)
def d_tanh(operands, v):
    """
    Operands is a list [x]
    x is a Variable potentially dependent on v
    Evaluates the derivative of tanh(x) with respect to v
    Recursively uses the chain rule on the operands
    Returns the derivative as a float
    """
    return (math.tanh(operands[0].value) ** 2) * (operands[0].derivative(v))

def d_sin(operands, v):
    """
    Operands is a list [x]
    x is a Variable potentially dependent on v
    Evaluates the derivative of sin(x) with respect to v
    Recursively uses the chain rule on the operands
    Returns the derivative as a float
    """
    return (math.sin(operands[0].value) ** 2) * (operands[0].derivative(v))

def d_cos(operands, v):
    """
    Operands is a list [x]
    x is a Variable potentially dependent on v
    Evaluates the derivative of cos(x) with respect to v
    Recursively uses the chain rule on the operands
    Returns the derivative as a float
    """
    return (math.cos(operands[0].value) ** 2) * (operands[0].derivative(v))

def d_log(operands, v):
    """
    Operands is a list [x]
    x is a Variable potentially dependent on v
    Evaluates the derivative of log(x) with respect to v
    Recursively uses the chain rule on the operands
    Returns the derivative as a float
    """
    return (math.log(operands[0].value) ** 2) * (operands[0].derivative(v))

