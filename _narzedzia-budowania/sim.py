# debt payoff simulation
def sim(order_key, budget, debts):
    d=[dict(x) for x in debts]; months=0; interest=0.0
    while any(x['bal']>0.005 for x in d):
        months+=1
        for x in d:
            if x['bal']>0:
                i=x['bal']*x['rate']/12; x['bal']+=i; interest+=i
        left=budget
        for x in d:
            if x['bal']>0:
                p=min(x['min'],x['bal'],left); x['bal']-=p; left-=p
        if order_key:
            for x in sorted([x for x in d if x['bal']>0], key=order_key):
                p=min(left,x['bal']); x['bal']-=p; left-=p
                if left<=0: break
        if months>600: break
    return months, round(interest)
debts=[dict(n='limit',bal=1500,rate=0.12,min=50),dict(n='karta',bal=5000,rate=0.18,min=150),dict(n='pozyczka',bal=9000,rate=0.14,min=250)]
print('min only', sim(None,450,debts))
print('snowball', sim(lambda x:x['bal'],900,debts))
print('avalanche', sim(lambda x:-x['rate'],900,debts))
# min-only: budget not rolled over -> each debt separately
tot=0;mx=0
for x in debts:
    m,i=sim(None,x['min'],[x]); print(x['n'],m,i); tot+=i; mx=max(mx,m)
print('min separately',mx,tot)

# ETF fee chart: 500/month 30y 6% gross
def fv(rate,years,p=500):
    r=rate/12; n=years*12
    return p*((1+r)**n-1)/r
X0,X1,Y0,Y1=70,600,250,30; vmax=500000
def x(t): return X0+(X1-X0)*t/30
def y(v): return Y0-(Y0-Y1)*v/vmax
for name,rate in [('low',0.058),('high',0.04),('dep',None)]:
    pts=[]
    for t in range(0,31,2):
        v = 500*12*t if rate is None else (fv(rate,t) if t else 0)
        pts.append(f"{x(t):.0f},{y(v):.0f}")
    print(name,' '.join(pts), round(fv(rate,30)) if rate else 180000)
for g in range(0,500001,100000): print(g, round(y(g)))
