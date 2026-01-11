def getMaxRating(customer_rating, k, m):
    # Write your code here
    n = len(customer_rating)
    if m == 1:
        return max(customer_rating)+k
    res = 0
    for i in range(31, -1, -1):
        bit = 1<<i
        cycle = bit << 1
        x = []
        for r in customer_rating:
            if r % cycle >= bit:
                x.append(0)
            else:
                x.append(bit-(r%cycle))
        x.sort()
        requiredOperations = sum(x[:m])

        if requiredOperations <= k:
            res |= bit
            k-=requiredOperations
            seen = 0
            for j in range(n):
                if seen==m:
                    break
                x = customer_rating[j]
                if (x%cycle) < bit:
                    add = bit - (x%cycle)
                    if add <= requiredOperations:
                        customer_rating[j]+=add
                        seen+=1
    return res

print(getMaxRating([1, 3, 2],5,1))