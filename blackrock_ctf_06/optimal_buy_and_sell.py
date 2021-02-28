# Python3 Program to find 
# best buying and selling days
 
# This function finds the buy sell
# schedule for maximum profit
def max_profit(price, fee):
    profit = 0 
    n = len(price)
    # Prices must be given for at least two days
    if (n == 1):
        return
     
    # Traverse through given price array
    i = 0
    while (i < (n - 1)):
         
        # Find Local Minima
        # Note that the limit is (n-2) as we are
        # comparing present element to the next element
        while ((i < (n - 1)) and ((price[i + 1])<= price[i])):
            i += 1
         
        # If we reached the end, break
        # as no further solution possible
        if (i == n - 1):
            break
         
        # Store the index of minima
        buy = i
        buying = price[buy]
        i += 1
        
         
        # Find Local Maxima
        # Note that the limit is (n-1) as we are
        # comparing to previous element
        while ((i < n) and (price[i] >= price[i - 1])):
            i += 1
        while (i < n) and (buying + fee >= price[i - 1]): 
            i += 1   
        # Store the index of maxima
        sell = i - 1
        selling = price[sell]


        print("Buy on day: ",buy,"\t",
                "Sell on day: ",sell)
        print(buying, selling)
        profit += (selling - fee - buying)
    print(profit)

# sample test case
 
# Stock prices on consecutive days
price = [1, 3, 2, 8, 4, 9]
n = len(price)
 
# Fucntion call
max_profit(price, 2)
 
