import numpy as np, openpyxl
from scipy import stats
from scipy.stats import f as F

wb=openpyxl.load_workbook('/mnt/user-data/uploads/likert_survey.xlsx',data_only=True)
def load(name):
    ws=wb[name]; return np.array([[ws.cell(r,c).value for c in range(2,12)] for r in range(2,17)],dtype=float)  # 15 sentences x 10 respondents
A,B=load('Cover A'),load('Cover B')
n,k=A.shape

def desc(M,name):
    resp=M.mean(0)                       # each respondent's mean over 15 sentences
    cnt=[(M==v).mean()*100 for v in (3,4,5)]
    print(f"{name}: ratings={M.size} grand mean={M.mean():.3f} SD(all ratings)={M.std(ddof=1):.3f} median={np.median(M):.1f} | respondent means: mean={resp.mean():.3f} SD={resp.std(ddof=1):.3f} range={resp.min():.2f}-{resp.max():.2f} | % of 3/4/5 = {cnt[0]:.1f}/{cnt[1]:.1f}/{cnt[2]:.1f}; any 1 or 2: {(M<3).sum()}")
    return resp
ra=desc(A,'Cover A'); rb=desc(B,'Cover B')

# ---- paired comparison, unit = respondent (n=10), each rated both covers ----
d=ra-rb
t,p=stats.ttest_rel(ra,rb); ci=stats.t.interval(0.95,len(d)-1,loc=d.mean(),scale=stats.sem(d))
w=stats.wilcoxon(ra,rb,method='exact')
dz=d.mean()/d.std(ddof=1)
print(f"\nPaired (respondent-level, n={len(d)}): mean diff A-B={d.mean():.3f} 95%CI[{ci[0]:.3f},{ci[1]:.3f}] t={t:.2f} p={p:.4f} dz={dz:.2f} | Wilcoxon exact W={w.statistic:.1f} p={w.pvalue:.4f} | respondents with A>B: {(d>0).sum()}, A<B: {(d<0).sum()}, ties: {(d==0).sum()}")
# permutation (sign-flip) test and bootstrap
rng=np.random.default_rng(1)
signs=np.array(np.meshgrid(*[[1,-1]]*len(d))).reshape(len(d),-1).T
perm=(signs*d).mean(1); pperm=(np.abs(perm)>=abs(d.mean())-1e-12).mean()
print(f"Sign-flip permutation test (exact, 2^{len(d)}): p={pperm:.4f}")
# two-way bootstrap: resample respondents (paired) and sentences (independently per cover) -> CI of mean difference
bs=[]
for _ in range(10000):
    r=rng.integers(0,k,k); sa=rng.integers(0,n,n); sb=rng.integers(0,n,n)
    bs.append(A[np.ix_(sa,r)].mean()-B[np.ix_(sb,r)].mean())
print(f"Bootstrap (respondents and sentences resampled) 95%CI of mean diff: [{np.percentile(bs,2.5):.3f},{np.percentile(bs,97.5):.3f}]")

# ---- ICC: targets = 15 sentences, raters = 10 respondents ----
def icc(M,alpha=0.05):
    n,k=M.shape; gm=M.mean()
    ssr=k*((M.mean(1)-gm)**2).sum(); ssc=n*((M.mean(0)-gm)**2).sum(); sst=((M-gm)**2).sum(); sse=sst-ssr-ssc
    msr=ssr/(n-1); msc=ssc/(k-1); mse=sse/((n-1)*(k-1))
    i21=(msr-mse)/(msr+(k-1)*mse+k*(msc-mse)/n); i31=(msr-mse)/(msr+(k-1)*mse)
    i2k=(msr-mse)/(msr+(msc-mse)/n); i3k=(msr-mse)/msr
    # McGraw & Wong CIs
    Fj=msc/mse; vn=(k-1)*(n-1)*(k*i21*Fj+n*(1+(k-1)*i21)-k*i21)**2
    vd=(n-1)*k**2*i21**2*Fj**2+(n*(1+(k-1)*i21)-k*i21)**2; v=vn/vd
    F3=F.ppf(1-alpha/2,n-1,v); F4=F.ppf(1-alpha/2,v,n-1)
    lo21=n*(msr-F3*mse)/(F3*(k*msc+(k*n-k-n)*mse)+n*msr); hi21=n*(F4*msr-mse)/(k*msc+(k*n-k-n)*mse+n*F4*msr)
    Fr=msr/mse; lo31=(Fr/F.ppf(1-alpha/2,n-1,(n-1)*(k-1))-1)/(Fr/F.ppf(1-alpha/2,n-1,(n-1)*(k-1))+k-1)
    hi31=(Fr*F.ppf(1-alpha/2,(n-1)*(k-1),n-1)-1)/(Fr*F.ppf(1-alpha/2,(n-1)*(k-1),n-1)+k-1)
    tr=lambda x:k*x/(1+(k-1)*x)
    return dict(ICC21=(i21,lo21,hi21),ICC31=(i31,lo31,hi31),ICC2k=(i2k,tr(lo21),tr(hi21)),ICC3k=(i3k,tr(lo31),tr(hi31)),msr=msr,msc=msc,mse=mse)
print()
for name,M in (('Cover A',A),('Cover B',B)):
    r=icc(M); print(name,'ICC(2,1)=%.3f [%.3f,%.3f]  ICC(2,k)=%.3f [%.3f,%.3f]  ICC(3,1)=%.3f  MSR=%.3f MSC=%.3f MSE=%.3f'%(*r['ICC21'],*r['ICC2k'],r['ICC31'][0],r['msr'],r['msc'],r['mse']))

# ---- data-pattern check: do ratings from different people repeat in a fixed cycle? ----
def lag_match(M,lag): return np.mean([(row[:-lag]==row[lag:]).mean() for row in M])
for name,M in (('Cover A',A),('Cover B',B)):
    obs={l:lag_match(M,l) for l in (1,2,3,4,5)}
    null={l:[] for l in obs}
    for _ in range(2000):
        P=np.array([rng.permutation(row) for row in M])
        for l in obs: null[l].append(lag_match(P,l))
    print(name,'share of equal ratings between respondent i and i+lag (observed vs permutation null mean, p):',
          {l:(round(obs[l],3),round(float(np.mean(null[l])),3),round(float((np.array(null[l])>=obs[l]).mean()),4)) for l in obs})
cors=np.corrcoef(A.T)[np.triu_indices(10,1)]; print('Cover A mean inter-respondent r = %.2f; Cover B = %.2f'%(cors.mean(),np.corrcoef(B.T)[np.triu_indices(10,1)].mean()))
