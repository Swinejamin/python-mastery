total = 0

for line in open("Data/portfolio.dat"):
    ticker, shares, price = line.split()
    shares = int(shares)
    price = float(price)
    print(f"ticker:{ticker}, shares:{shares}, price:{price}, cost: {shares * price}")
    total += shares * price

print(total)
