def OnTime(n):
    iteration=0
    for i in range(1,n+1):
        iteration+=1
    print("When n is",n,"iterations = ",iteration)

    Ontime(10)
    Ontime(20)
    Ontime(42)

    print("\nWith every 'n' the time taken and iterations will increase")