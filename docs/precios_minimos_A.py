# Uso: python3 precios_minimos_A.py <archivo con P y calc(), ej. líneas 3-52 de calc_ganancia_meli.py> salida.csv
exec(open(__import__("sys").argv[1]).read())
def minp(may,t,obj):
    # escaneo de $100 en $100: el escalón de $33.000 hace la función no monótona
    p=1000
    while p<5e6:
        if calc(may,p,t)[4]>=obj: return p
        p+=100
import csv
out=[]
for g,n,may,pv,t in P:
    p0,p10,p20=(minp(may,t,o) for o in (0.0001,0.10,0.20))
    # precio "redondo" recomendado: 10% neto, terminado en 900
    rec=int((p10+999)//1000*1000-100)
    if rec<p10: rec+=1000
    net=calc(may,rec,t)[3]
    out.append([g,n,round(pv),p0,p10,p20,rec,round(net),f"{(p0/pv-1)*100:+.0f}%"])
    print(f"{g} {n:38} sug {pv:9,.0f} | eq {p0:9,} | 10% {p10:9,} | 20% {p20:9,} | rec {rec:9,} gana {net:8,.0f} | {p0/pv-1:+.0%}")
with open(__import__('sys').argv[2],'w',newline='') as f:
    w=csv.writer(f); w.writerow(["grupo","producto","precio_sugerido_presmar","precio_equilibrio","precio_10%_neto","precio_20%_neto","precio_recomendado","ganancia_a_recomendado","equilibrio_vs_sugerido"]); w.writerows(out)
