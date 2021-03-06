"""
Laurens main loop. Pretty bare-bones right now.
"""

import os
import sys
import config
import ast.ast
import ast.cont
import op

from debug         import logMsg, debug
from parse         import parse
from data.closure  import Closure
from data.argstack import ArgStack
from data.retstack import RetStack
from data.updstack import UpdStack
from data.heap     import Heap
from data.config   import Config

from rpython.rlib.jit import JitDriver, purefunction

def get_location(code):
    return "%s" % ( code )

jitdriver = JitDriver(greens=['code']
                     , reds=['config']
                     #, reds='auto'
                     , get_printable_location=get_location)

def terminateHuh(config):
  return (((config.code.op == op.ReturnConOp) or 
           (config.code.op == op.ReturnIntOp)) 
          and config.ret_stack.empty()
          and config.upd_stack.empty())

def loop(config):

  while True:
    jitdriver.jit_merge_point(code=config.code.expr, config=config)
    if terminateHuh(config):
        return config
    config = config.code.step(config)
    # Reduce until we get to a node backed by an AST
    while type(config.code) is not op.Eval:
        if terminateHuh(config):
            return config
        debug("-------------")
        debug(str(config))
        config = config.code.step(config)
    jitdriver.can_enter_jit(code=config.code.expr, config=config)
  return config

def run(fp):
    program_contents = ""
    while True:
        read = os.read(fp, 4096)
        if len(read) == 0:
            break
        program_contents += read
    os.close(fp)
    heap, global_env = parse(program_contents)
    loop(heap, global_env)


def lam(args,body):
  return ast.ast.Lambda([],args,False,body)

def mtclos(args, body):
  return Closure(ast.ast.Lambda([],args,False,body),[])

def test(main,heap,test_name):
  main_addr  = heap.new_addr()
  heap.set_addr(main_addr,main)
  debug("------------------------------------------------")
  debug(test_name)
  code   = op.Eval(ast.ast.App(ast.ast.Var("main"), []), {})
  answer = loop(Config(code, ArgStack(), RetStack(), UpdStack(), heap, {"main":ast.ast.Value(main_addr,False)}))
  debug(str(answer))


