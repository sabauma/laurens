class Stack(object):
  def __init__(self):
    self.internal   = []

  def push(self,value):
    return self.internal.append(value)

  def extend(self,values):
    if values == []:
        return 0
    values.reverse()
    for v in values:
      self.internal.append(v)

  def pop(self):
    return self.internal.pop()

  def peek(self):
    if len(self.internal) == 0:
      return "Empty"
    return self.internal[0]

  def __len__(self):
    return len(self.internal)

  def __str__(self):
    return "Stack - " + str(self.internal)

## from collections import deque
## 
## class Stack(object):
##   def __init__(self):
##     self.dq   = deque()
## 
##   def push(self,value):
##     return self.dq.append(value)
## 
##   def extend(self,values):
##     values = values.reverse()
##     for v in values:
##       self.push(v)
## 
##   def pop(self):
##     return self.dq.pop()
## 
##   def peek(self):
##     return self.dq[0]
## 
##   def __len__(self):
##     return len(self.dq)
