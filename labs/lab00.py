from random import randint

def get_random():
    limit = 2 # starting limit
    # Generate 50 random numbers and increase upper limit by 1 each time
    for i in range (1,51):
        x = randint(1, limit)
        limit = limit+1
        print(x)
        
def run_mult():
    # Generate 10 multiplication questions with new random numbers each time
    for i in range(0,9):
        x = randint(1,10)
        y = randint(1,10)
        ans = int(input("Question "+str(i+1)+". Compute "+str(x)+"*"+str(y)+": "))
        if(ans==x*y):
            print("Right!")
        else:
            print("Wrong! The answer is "+str((x*y))+".")

if __name__ == "__main__":
        get_random() # Problem 1
        run_mult() # Problem 2
        