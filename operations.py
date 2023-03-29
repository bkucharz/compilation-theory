import operator
import numpy as np
operations = {"+": operator.add,
              "-": operator.sub,
              "/": operator.truediv,
              "*": operator.mul,
              "=": lambda x, y: y,
              "+=": operator.add,
              "-=": operator.sub,
              "/=": operator.truediv,
              "*=": operator.mul,
              ".+": np.add,
              ".-": operator.sub,
              "./": operator.truediv,
              ".*": np.dot,
              ">=": operator.ge,
              "<=": operator.le,
              "==": operator.eq,
              "<": operator.lt,
              ">": operator.gt,
              }