import sys
sys.dont_write_bytecode = True # Sem cache
from infra.instalar_dependencias import *

if __name__ == "__main__":
    instalar_dependencias()

    from src.interface import *
    interface_grafica()
    