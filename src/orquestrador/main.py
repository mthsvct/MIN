from orquestrador import Orquestrador


if "__main__" == __name__:
    
    orq = Orquestrador(
        host="localhost",
        port=2000
    )
    orq.start()




