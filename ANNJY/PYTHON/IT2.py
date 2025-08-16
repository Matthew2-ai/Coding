def ONsquareTime(n):
    iteration=0
    for i in range(0,n):
        for j in range(0,n):
            print("*",end=" ")
            iteration+=1
        print("")
    print("\nWhen n is ",n"Iterations = ",iteration,"\n")

    OnsquareTime(5)
    ONsquaretime(4)
    ONsquareTime(3)

    print("\nWith every 'n' the time taken equals n^2")
    print("O(n^2)")
