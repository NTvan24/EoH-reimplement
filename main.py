from eoh import EOH
from problem import TSPCONST
if __name__ == "__main__":
    problem = TSPCONST()
    eoh = EOH(problem)
    eoh.run()