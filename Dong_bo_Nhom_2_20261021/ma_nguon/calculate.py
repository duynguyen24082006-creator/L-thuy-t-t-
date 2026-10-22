from pathlib import Path
import json, math, csv
import numpy as np
from scipy.integrate import quad

ROOT=Path(__file__).parent
P={'m0':3450.,'payload':4100.,'persons':2,'person_mass':65.,'g':9.81,'front_fraction':.3,'rear_fraction':.7,
   'vmax_kmh':95.,'psi_max':.31,'f0':.018,'threshold':22.2,'K':.65,'F':4.5,'eta':.85,
   'lambda_v':.9,'nv':2600.,'nmin':800.,'a':.5,'b':1.5,'c':1.,'tire_width_in':8.25,'rim_in':16.,'lambda_t':.95,
   'ip':1.25,'ih1':5.5,'top':.8,'phi':.75,'mb':1.,'nshift':2340.,'shift_seconds':1.,'delta_coast':1.05,
   'target_factor':.95,'drive_intervals_per_smooth_segment':1600,'coast_dt':.01}
P['M']=P['m0']+P['payload']+P['persons']*P['person_mass'];P['G']=P['M']*P['g']
P['G1']=P['front_fraction']*P['G'];P['G2']=P['rear_fraction']*P['G']
P['W']=P['K']*P['F'];P['vmax']=P['vmax_kmh']/3.6;P['nN']=P['nv']/P['lambda_v']
P['r0']=(P['tire_width_in']+P['rim_in']/2)*.0254;P['rb']=P['r0']*P['lambda_t']
def f(v,side=None):
    high=(v>P['threshold']) if side is None else side=='high'
    return P['f0']*(1+v*v/1500) if high else P['f0']
def resistance(v,side=None):return P['G']*f(v,side)+P['W']*v*v
P['fvmax']=f(P['vmax']);P['Pfmax']=P['G']*P['fvmax'];P['Pwmax']=P['W']*P['vmax']**2
P['Pcmax']=resistance(P['vmax']);P['Nv']=P['Pcmax']*P['vmax']/(1000*P['eta'])
P['Nmax']=P['Nv']/(P['a']*P['lambda_v']+P['b']*P['lambda_v']**2-P['c']*P['lambda_v']**3)
P['nM']=P['b']/(2*P['c'])*P['nN']
P['i0']=2*math.pi*P['rb']*P['nv']/(60*P['top']*P['ip']*P['vmax'])
P['q']=P['ih1']**(1/3);P['ih']=[P['ih1'],P['ih1']/P['q'],P['ih1']/P['q']**2,1.,P['top']]
P['it']=[i*P['ip']*P['i0'] for i in P['ih']];P['iR']=1.2*P['ih1']
P['delta']=[1.05+.05*(i*P['ip'])**2 for i in P['ih']]
P['Pphi']=P['phi']*P['mb']*P['G2']
def engine(n):
    x=n/P['nN'];N=P['Nmax']*(P['a']*x+P['b']*x*x-P['c']*x*x*x)
    return N,60000/(2*math.pi)*N/n
P['Mmax']=engine(P['nM'])[1]
P['ih_min']=P['psi_max']*P['G']*P['rb']/(P['Mmax']*P['i0']*P['ip']*P['eta'])
P['ih_max']=P['Pphi']*P['rb']/(P['Mmax']*P['i0']*P['ip']*P['eta'])
def speed(n,k):return 2*math.pi*n*P['rb']/(60*P['it'][k])
def rpm(v,k):return v*60*P['it'][k]/(2*math.pi*P['rb'])
def values(v,k,side=None):
    n=rpm(v,k);N,M=engine(n);pk=M*P['it'][k]*P['eta']/P['rb'];pw=P['W']*v*v;pf=P['G']*f(v,side)
    D=(pk-pw)/P['G'];Dphi=(P['Pphi']-pw)/P['G'];j=(min(pk,P['Pphi'])-pf-pw)/(P['M']*P['delta'][k])
    if abs(j)<1e-12:j=0.
    return {'n':n,'Ne':N,'Me':M,'v':v,'v_kmh':3.6*v,'Pk':pk,'Pw':pw,'Pf':pf,'Pc':pf+pw,'f':f(v,side),'D':D,'Dphi':Dphi,'j':j,'invj':1/j if j>0 else None}
P['vstart']=speed(P['nmin'],0);P['target']=P['target_factor']*P['vmax']
P['peak_v1']=speed(P['nM'],0);P['peak_pk1']=values(P['peak_v1'],0)['Pk']
P['peak_required']=P['psi_max']*P['G']+P['W']*P['peak_v1']**2
P['peak_margin']=P['peak_pk1']-P['peak_required'];P['peak_pkR']=P['peak_pk1']*1.2
P['peak_D1']=values(P['peak_v1'],0)['D']
alpha=math.asin(P['peak_D1']/math.sqrt(1+P['f0']**2))-math.atan(P['f0'])
P['grade_at_torque_peak_percent']=100*math.tan(alpha)

engine_ns=[800.,1200.,1600.,2000.,P['nM'],2400.,P['nv'],P['nN']]
rows_ne=[]
for n in engine_ns:
    N,M=engine(n)
    rows_ne.append({'n':n,'Ne':N,'Me':M,'Nk':N*P['eta'],'gears':[values(speed(n,k),k) for k in range(5)]})
road=[]
for v,side,label in [(0,None,None),(5,None,None),(10,None,None),(15,None,None),(20,None,None),(22.2,'low','22,200−'),(22.2,'high','22,200+'),(24,None,None),(P['target'],None,None),(P['vmax'],None,None)]:
    pf=P['G']*f(v,side);pw=P['W']*v*v
    road.append({'v':v,'label':label,'f':f(v,side),'Pf':pf,'Pw':pw,'Pc':pf+pw,'Pphi':P['Pphi'],'Dphi':(P['Pphi']-pw)/P['G'],'Nf':pf*v/1000,'Nw':pw*v/1000,'Nc':(pf+pw)*v/1000})

def trajectory(Ngrid=1600,dtcoast=.01):
    records=[];phases=[];shifts=[];t=s=0.;v=P['vstart']
    def append(stage,kind,k,v,side=None,dt=0.,ds=0.):
        nonlocal t,s
        t+=dt;s+=ds
        if kind=='drive':r=values(v,k,side)
        else:r={'n':None,'Ne':0.,'Me':0.,'v':v,'v_kmh':3.6*v,'Pk':0.,'Pw':P['W']*v*v,'Pf':P['G']*f(v),'Pc':resistance(v),'f':f(v),'D':None,'Dphi':(P['Pphi']-P['W']*v*v)/P['G'],'j':-resistance(v)/(P['M']*P['delta_coast']),'invj':None}
        r.update({'stage':stage,'kind':kind,'gear':k+1,'side':side,'dt':dt,'ds':ds,'t':t,'S':s});records.append(r)
    def ode(v):return -resistance(v)/(P['M']*P['delta_coast'])
    for k in range(5):
        start=v;ta=t;sa=s;end=speed(P['nshift'],k) if k<4 else P['target'];stage=f'Kéo {k+1}'
        assert P['nmin']-1e-8<=rpm(v,k)<=P['nN']+1e-8
        cuts=[v]+([P['threshold']] if v<P['threshold']<end else [])+[end]
        for l,h in zip(cuts[:-1],cuts[1:]):
            side='high' if (l+h)/2>P['threshold'] else 'low';vs=np.linspace(l,h,Ngrid+1)
            prev=values(vs[0],k,side);assert prev['j']>0
            append(stage,'drive',k,float(vs[0]),side)
            for nv in vs[1:]:
                cur=values(float(nv),k,side);assert cur['j']>0
                dv=float(nv)-prev['v'];dt=dv/2*(prev['invj']+cur['invj']);ds=dv/2*(prev['v']*prev['invj']+cur['v']*cur['invj'])
                append(stage,'drive',k,float(nv),side,dt,ds);prev=cur
        v=end;phases.append({'stage':stage,'kind':'drive','gear':k+1,'v0':start,'v1':v,'dt':t-ta,'ds':s-sa,'t':t,'S':s})
        if k<4:
            start=v;ta=t;sa=s;stage=f'Chuyển {k+1}→{k+2}';append(stage,'coast',k,v)
            nsteps=round(P['shift_seconds']/dtcoast);dt=P['shift_seconds']/nsteps
            for _ in range(nsteps):
                a1=ode(v);v2=v+dt*a1/2;a2=ode(v2);v3=v+dt*a2/2;a3=ode(v3);v4=v+dt*a3;a4=ode(v4)
                nv=v+dt*(a1+2*a2+2*a3+a4)/6;ds=dt*(v+2*v2+2*v3+v4)/6
                v=nv;append(stage,'coast',k,v,None,dt,ds)
            phases.append({'stage':stage,'kind':'coast','gear':k+1,'v0':start,'v1':v,'dt':t-ta,'ds':s-sa,'t':t,'S':s})
            shifts.append({'from':k+1,'to':k+2,'v0':start,'v1':v,'dv':start-v,'dt':t-ta,'ds':s-sa,'n_after':rpm(v,k+1)})
    return records,phases,shifts

records,phases,shifts=trajectory(P['drive_intervals_per_smooth_segment'],P['coast_dt'])
P['time']=records[-1]['t'];P['distance']=records[-1]['S']
fine,_,_=trajectory(2*P['drive_intervals_per_smooth_segment'],P['coast_dt']/2)
checks={'time_s':P['time'],'distance_m':P['distance'],'grid_double_delta_t':fine[-1]['t']-P['time'],'grid_double_delta_S':fine[-1]['S']-P['distance'],'power_residual_kW':engine(P['nv'])[0]*P['eta']-P['Pcmax']*P['vmax']/1000,'force_residual_N':values(P['vmax'],4)['Pk']-P['Pcmax'],'source_torque_relative_difference':(10000/1.047)/(60000/(2*math.pi))-1}
assert abs(checks['power_residual_kW'])<1e-8 and abs(checks['force_residual_N'])<1e-8
assert all(records[i]['t']>=records[i-1]['t'] and records[i]['S']>=records[i-1]['S'] for i in range(1,len(records)))
assert P['peak_pk1']<P['Pphi'] and P['peak_pkR']<P['Pphi']
assert P['peak_margin']>0
example0=values(2.,0);example1=values(2.01,0)
example={'vA':2.,'vB':2.01,'jA':example0['j'],'jB':example1['j'],'dt':.01/2*(1/example0['j']+1/example1['j']),'ds':.01/2*(2/example0['j']+2.01/example1['j'])}
data={'parameters':P,'engine_rows':rows_ne,'road_rows':road,'phases':phases,'shifts':shifts,'checks':checks,'worked_example':example}
(ROOT/'model.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
with (ROOT/'trajectory.csv').open('w',newline='',encoding='utf-8') as file:
    w=csv.DictWriter(file,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
print(json.dumps(P,ensure_ascii=False,indent=2));print(json.dumps(checks,indent=2));print('rows',len(records))
