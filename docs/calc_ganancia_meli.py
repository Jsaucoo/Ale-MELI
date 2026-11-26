# Supuestos (ver informe): Clásica 14%, cargo fijo $3.360 si precio < $33.000,
# envío gratis a cargo vendedor si precio >= $33.000 según peso, IVA 21% sobre cargos de MELI.
COM=0.14; FIJO=3360; IVA=0.21
ENV={1:7790,2:9500,3:12500,4:16000}  # 1: <=1kg (fuente), 2: 1-2kg, 3: 2-5kg, 4: >5kg/voluminoso (estimados)
P=[ # grupo, nombre, mayorista sin IVA, precio venta, tramo peso
("A1","MTX-6175 Traba disco c/alarma",30812.06,48467.40,1),
("A1","MTX-6177 Traba disco 5,5mm",11027.48,17346.20,1),
("A1","MTX-6178 Traba manillar",9243.62,14540.20,1),
("A1","KIT Antirrobo (6175+6178)",30812.06+9243.62,62000,1),
("A2","Kronwell PSTX4L",18985.58,34344.00,1),
("A2","Kronwell PS12V5-3B",19227.00,34710.90,2),
("A2","Kronwell PSTZ6S",22959.30,41310.00,2),
("A2","Kronwell PS12V7-3B",30200.31,52986.40,2),
("A2","Kronwell PSTX7L",30556.57,53611.50,2),
("A2","Kronwell PS12V9-4B",34324.76,60222.80,3),
("A2","Motobatt MTZ5S",23553.80,41325.10,1),
("A2","Motobatt MTX5L",26722.77,46885.10,2),
("A2","Motobatt MTZ7S",35775.97,62768.90,2),
("A3","SP52500 Kit Moto Espejo+abraz.",44578.58,78213.10,1),
("A3","SP52501 Kit Moto Espejo+interfaz",40119.83,70390.20,1),
("A3","SP52400 Kit Moto LT+abraz.",62413.58,109504.60,1),
("A3","SP52642/64 Sobre impermeable L/XL",31202.33,54744.50,1),
("A3","SP Funda Phone Case iPhone17",40119.83,70390.20,1),
("A3","SP Funda Extrema iPhone17",80248.58,140796.10,1),
("A3","SP Vidrio pantalla",17826.08,31275.90,1),
("A3","Midland K10 delivery",47005.92,82471.90,1),
("A4","Midland BT Mini Simple",122411.25,214770.50,1),
("A4","Midland BTR 1 Simple",201298.50,353178.20,1),
("A4","Midland BTR 1 Doble",367233.75,644311.60,1),
("A4","Midland R1 Mesh Simple",248494.84,435984.20,1),
("A4","Midland H5 Pro camara",152061.98,266792.70,1),
("A4","NOCO GB20",177185.03,310871.10,1),
("A4","NOCO GB40",221505.73,388631.80,2),
("A4","Midland Powerbank Air Compresor",64082.81,112433.30,1),
("A5","Muc-Off MO-625 Kit x2",28460.09,49933.20,2),
("A5","Muc-Off MO-20802 Kit x3 visor",22300.82,39126.80,1),
("A5","Muc-Off MO-21069 Kit x3 cadena",44601.64,78253.60,2),
("A5","Muc-Off MO-20803 Kit x4 casco",44601.64,78253.60,2),
("A5","Muc-Off MO-636 Kit x4 Essentials",59468.85,104338.10,3),
("A5","Muc-Off MO-21197 Kit x8 lavado",80537.81,141303.60,3),
("A5","Muc-Off MO-285 Valija x10",148714.60,260919.80,4),
("A6","KIT Service Wave (F300+HN21+ChainLube)",6179.18+4865.06+6683.78,34000,2),
("A7","Chaoyang 2.50-17 H909",27772.64,37030.19,3),
("A7","Chaoyang 2.75-18 H909",38388.05,51184.07,3),
("A7","Chaoyang 90/90-17 H909",45753.71,61004.95,3),
]
def calc(may,pv,t):
    costo=may*1.21
    com=pv*COM; fijo=FIJO if pv<33000 else 0; env=ENV[t] if pv>=33000 else 0
    meli=(com+fijo+env)*(1+IVA)
    neto=pv-meli-costo
    return costo,meli,pv-meli,neto,neto/pv,neto/costo
def precio_obj(may,t,obj=0.20):
    lo,hi=1,5e6
    for _ in range(100):
        m=(lo+hi)/2; c=calc(may,m,t)
        if c[4]<obj: lo=m
        else: hi=m
    return hi
import csv,sys
rows=[]
print(f"{'Grp':3} {'Producto':38} {'Venta':>9} {'Costo':>9} {'MELI':>8} {'Cobrás':>9} {'Ganancia':>9} {'%venta':>6} {'%costo':>6} {'P.20%':>9}")
for g,n,may,pv,t in P:
    c,m,cob,neto,pm,pc=calc(may,pv,t); po=precio_obj(may,t)
    rows.append([g,n,round(pv),round(c),round(m),round(cob),round(neto),f"{pm*100:.1f}",f"{pc*100:.1f}",round(po),t])
    print(f"{g:3} {n:38} {pv:9,.0f} {c:9,.0f} {m:8,.0f} {cob:9,.0f} {neto:9,.0f} {pm*100:6.1f} {pc*100:6.1f} {po:9,.0f}")
with open(sys.argv[1],'w',newline='') as f:
    w=csv.writer(f); w.writerow(["grupo","producto","precio_venta","costo_con_iva","cobra_meli_con_iva","te_deposita","ganancia_neta","margen_%_venta","retorno_%_costo","precio_para_20%_neto","tramo_peso"]); w.writerows(rows)
