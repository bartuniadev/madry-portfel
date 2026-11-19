# Real (inflation-adjusted) value after tax of 10 000 zl, assumed inflation 4%/yr
infl=0.04
X0,X1,Y0,Y1=70,600,250,30
vmin,vmax=6000,13000
def x(t): return X0+(X1-X0)*t/10
def y(v): return Y0-(Y0-Y1)*(v-vmin)/(vmax-vmin)
def real(nominal,t): return nominal/((1+infl)**t)
series={}
series['cash']=[real(10000,t) for t in range(11)]
series['lokata']=[real(10000*(1+0.03*0.81)**t,t) for t in range(11)]
def edo(t):
    nom=10000*(1+infl+0.015)**t
    return real(nom-0.19*(nom-10000),t)
series['edo']=[edo(t) for t in range(11)]
for k,v in series.items():
    print(k, ' '.join(f"{x(t):.0f},{y(val):.0f}" for t,val in enumerate(v)), round(v[-1]))
for g in range(6000,13001,1000): print(g, round(y(g)))
