import numpy as np

N = 10        # number or people
M = 3          # number of goods

inventory = np.random.randint(0,10,(N,M))

cash_min = 1
cash_var = 1
cash = cash_min + np.abs(cash_var*np.random.randn(N))


utility = np.random.random((N,M))

prices = [[utility[:,j].mean()] for j in range(M)]

def get_value(inv, u):
    total = 0
    for i in range(inv.max()):
        total += ((inv>i) * u*0.9**i).sum()
    return total

orig_inv = inventory.sum()
orig_cash = cash.sum()

print(get_value(inventory, utility))


total_iter = 1000
num_trials = 10
num_trades = 0
for iter_num in range(total_iter):
    i = np.random.randint(N)
    item_i = np.argmax(utility[i]*0.9**inventory[i])
    p_item_i = np.array(prices[item_i]).mean()
    for t in range(num_trials):
        j=-1
        item_j = -1
        fail=0
        while j<0 or inventory[j,item_i]<1 or item_j < 0 or item_j == item_i:
            j = np.random.randint(N-1)
            if j>=i:
                j+=1
            item_j = np.argmax(utility[j]*0.9**inventory[j])
            fail += 1
            if fail > 10:
                break
        p_item_j = np.array(prices[item_j]).mean()
        if p_item_i > p_item_j:
            inventory[i,item_i]+=1
            inventory[j,item_i]-=1
            cash[i]-=p_item_i
            cash[j]+=p_item_i
            num_trades += 1

assert inventory.sum() == orig_inv
assert orig_cash == cash.sum()

print(num_trades)
print(get_value(inventory, utility))

