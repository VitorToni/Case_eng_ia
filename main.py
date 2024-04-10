import sys
sys.dont_write_bytecode = True # Sem cache

from infra.instalar_dependencias import *
from src.controler import *

if __name__ == "__main__":
    instalar_dependencias()
    print(hello_world())
    