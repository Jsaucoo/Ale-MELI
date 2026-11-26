# Simulación por agentes + Monte Carlo: productos A publicados al precio recomendado (~10% neto)
# Período: dic-2026 a may-2027. Es un modelo de escenarios con supuestos, NO un pronóstico.
# Uso: python3 simulacion_6_meses_A.py
import csv, random, statistics as st, os
HERE=os.path.dirname(os.path.abspath(__file__))
COM=0.14; FIJO=3360; IVA=0.21; ENV={1:7790,2:9500,3:12500,4:16000}
def cargos(pv,t): return (pv*COM+(FIJO if pv<33000 else 0)+(ENV[t] if pv>=33000 else 0))*(1+IVA)

# mayorista y tramo de peso desde la calculadora original
P={}
src=open(os.path.join(HERE,"calc_ganancia_meli.py")).read().split("P=[",1)[1].split("\n]",1)[0]
for g,n,may,pv,t in eval("["+src+"]"): P[n]=(g,may,t)
REC={r["producto"]:r for r in csv.DictReader(open(os.path.join(HERE,"precios_minimos_productos_A.csv")))}

MESES=["dic-26","ene-27","feb-27","mar-27","abr-27","may-27"]
# estacionalidad por grupo (1 = mes normal). Dic: regalos. Ene-feb: vacaciones/viajes. May: Hot Sale + frío (baterías)
EST={"A1":[1.2,1.0,0.9,1.0,1.0,1.2],"A2":[1.0,1.1,1.0,1.0,1.1,1.4],"A3":[1.4,1.3,1.1,0.9,0.8,1.1],
     "A4":[2.6,1.2,0.9,0.7,0.7,1.3],"A5":[1.8,1.0,0.9,0.8,0.8,1.0],"A6":[1.0,1.0,1.0,1.2,1.0,1.0],"A7":[1.0,1.0,1.0,1.1,1.0,1.0]}
VIS={"A1":260,"A2":320,"A3":200,"A4":260,"A5":160,"A6":130,"A7":320}  # visitas/mes de una publicación nueva bien armada
# perfiles de comprador: (tolerancia de precio sobre el de mercado, prob. de compra si el precio le cierra, peso de la reputación)
PERF={"cazador_precio":(1.03,0.045,0.6),"confianza_marca":(1.12,0.035,1.0),"regalo":(1.20,0.050,0.7),"urgente":(1.25,0.060,0.4)}
def mezcla(g,mes):
    m={"cazador_precio":0.40,"confianza_marca":0.30,"regalo":0.10,"urgente":0.20}
    if g in("A2","A6","A7"): m.update(urgente=0.35,regalo=0.02,cazador_precio=0.40,confianza_marca=0.23)
    if mes==0 and g in("A3","A4","A5"): m.update(regalo=0.45,cazador_precio=0.25,confianza_marca=0.20,urgente=0.10)
    s=sum(m.values()); return {k:v/s for k,v in m.items()}
ADS={"A4","A5"}  # Mercado Ads en diciembre: +50% visitas, cuesta 6% de lo vendido con ads

def correr(ref_factor, seed):
    R=random.Random(seed); ventas_cum=0
    ref={n:float(REC[n]["precio_sugerido_presmar"])*ref_factor*R.lognormvariate(0,0.12) for n in REC}
    filas={n:[0]*6 for n in REC}; gan={n:0.0 for n in REC}; fact={n:0.0 for n in REC}
    for mes in range(6):
        rep=0.45+0.55*min(1,ventas_cum/60)            # vendedor nuevo: menos visibilidad y confianza al principio
        for n,r in REC.items():
            g,may,t=P[n]; pv=float(r["precio_recomendado"]); rel=pv/ref[n]
            ranking=min(1,1/rel)**2                       # Mercado Libre muestra menos lo que está caro vs. la competencia
            v=VIS[g]*EST[g][mes]*rep*ranking*(1.5 if mes==0 and g in ADS else 1)
            if mes==0: v*=0.75                            # en dic las publicaciones recién arrancan; corte de regalos ~18/12
            visitas=max(0,int(R.gauss(v,v*0.25))); u=0
            mz=mezcla(g,mes)
            for _ in range(visitas):                       # cada visita es un comprador con un perfil
                p=R.random(); acc=0
                for k,w in mz.items():
                    acc+=w
                    if p<=acc: break
                tol,pb,wrep=PERF[k]
                if rel<=tol and R.random()<pb*(1-wrep*(1-rep)): u+=1
            dev=sum(1 for _ in range(u) if R.random()<0.03)  # 3% devoluciones: perdés cargos + envío de vuelta
            neto_u=pv-cargos(pv,t)-may*1.21
            ads=0.06*pv*u if mes==0 and g in ADS else 0
            gan[n]+=neto_u*(u-dev)-dev*(cargos(pv,t)*0.5+ENV[t]*1.21)-ads
            fact[n]+=pv*(u-dev); filas[n][mes]=u; ventas_cum+=u
    return filas,gan,fact,rep

def escenario(nombre,ref_factor,N=1000):
    res=[correr(ref_factor,s) for s in range(N)]
    q=lambda xs,p: sorted(xs)[int(p*(len(xs)-1))]
    prod=[]
    for n,r in REC.items():
        us=[sum(x[0][n]) for x in res]; gs=[x[1][n] for x in res]; fs=[x[2][n] for x in res]
        mens=[st.median([x[0][n][m] for x in res]) for m in range(6)]
        prod.append(dict(grupo=r["grupo"],producto=n,precio=int(r["precio_recomendado"]),
            unid_p10=q(us,.1),unid_med=q(us,.5),unid_p90=q(us,.9),
            fact_med=round(q(fs,.5)),gan_p10=round(q(gs,.1)),gan_med=round(q(gs,.5)),gan_p90=round(q(gs,.9)),
            **{MESES[m]:mens[m] for m in range(6)}))
    tot=[sum(x[1].values()) for x in res]; tf=[sum(x[2].values()) for x in res]
    tu=[sum(sum(v) for v in x[0].values()) for x in res]
    mesT=[st.median([sum(x[0][n][m] for n in REC) for x in res]) for m in range(6)]
    return dict(nombre=nombre,prod=prod,tot=(q(tot,.1),q(tot,.5),q(tot,.9)),fact=q(tf,.5),
                unid=(q(tu,.1),q(tu,.5),q(tu,.9)),mes=mesT,rep=st.median([x[3] for x in res]))

if __name__=="__main__":
    E=[escenario("base (competencia vende al sugerido Presmar)",1.0),
       escenario("competencia agresiva (vende 10% bajo el sugerido)",0.9)]
    for e in E:
        print("\n=== ",e["nombre"]); print("unidades 6m p10/med/p90:",e["unid"]," facturación med:",round(e["fact"]),
              " ganancia p10/med/p90:",[round(x) for x in e["tot"]]," por mes:",e["mes"])
        with open(os.path.join(HERE,f"simulacion_6m_{'base' if e is E[0] else 'agresiva'}.csv"),"w",newline="") as f:
            w=csv.DictWriter(f,fieldnames=list(e["prod"][0])); w.writeheader(); w.writerows(e["prod"])
        g={}
        for p in e["prod"]:
            a=g.setdefault(p["grupo"],[0,0,0]); a[0]+=p["unid_med"]; a[1]+=p["gan_med"]; a[2]+=p["fact_med"]
        for k,v in sorted(g.items()): print(f"  {k}: unidades {v[0]:.0f}  facturación {v[2]:,}  ganancia {v[1]:,}")
        for p in sorted(e["prod"],key=lambda p:-p["gan_med"]):
            print(f"  {p['grupo']} {p['producto'][:34]:34} u {p['unid_p10']:>3}/{p['unid_med']:>3}/{p['unid_p90']:>3}  gan {p['gan_med']:>10,}  meses {[p[m] for m in MESES]}")
