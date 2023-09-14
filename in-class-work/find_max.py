# CSC 415
# 12 Sept, 2023
# Bridget Knight

import time

# Example 1: Use a simple algorithm to find the maximum number in a one-dimensional array
# Time complexity of O(n) -- use one for loop
def find_max(numbers):
    max = numbers[0]
    for idx, num in enumerate(numbers, start=1):
        if(num >= numbers[idx-1]):
            max = num
            
    return str(max)

# Example 2: Find the maximum element in a 2D array. Use a single for loop and measure the elapsed time.
# Time complexity: O(N * M)
def find_max_2D_single(arr):
    columns = len(arr[0])
    rows = len(arr)
    max = arr[0][0]
    
    for i in range(0, rows * columns):
        
        # Get current indices
        row = i // columns
        col = i % columns
        
        #print(arr[row][col])
        if(arr[row][col] > max):
            max = arr[row][col]

    return str(max)
    
if __name__ == "__main__":

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
    # Example 1 (list)
    # Get times to determine speed of algorithm
    start = time.time()

    numbers = [0,1,2,5,3,9,2,9,8,12,0,54]
    print("* * * * * EXAMPLE 1 * * * * *")
    print("Maximum: "+find_max(numbers))
    
    end = time.time()
    print("Elapsed time: "+str(end-start)+" seconds")
    print()
    
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
    # Example 2 (2D array) - ONE FOR-LOOP
    # Get times to determine speed of algorithm
    start = time.time()
    
    arr = [
        [1,2,3,4,5],
        [7,1,2,3,1]
    ]
    
    print("* * * * * EXAMPLE 2: Single For-Loop * * * * *")
    print("Maximum: "+find_max_2D_single(arr))
    
    end = time.time()
   # print("Elapsed time: "+str(end-start)+" seconds")
    
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
    # Example 2 (2D array) - TWO FOR-LOOPS
    # Get times to determine speed of algorithm
    #start = time.time()
    
    #print("* * * * * EXAMPLE 2: Two For-Loops * * * * *")
    #print("Maximum: "+find_max_2D_single(arr))
    
    #end = time.time()
    #print("Elapsed time: "+str(end-start)+" seconds")
    
    
    
