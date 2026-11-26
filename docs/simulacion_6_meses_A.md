# Simulación 6 meses (dic-26 → may-27) — Productos A al precio recomendado

> ⚠️ **Es un modelo de escenarios, no un pronóstico.** No se pudo correr MiroFish: esta máquina no tiene GPU, y MiroFish simula opinión en redes sociales, no ventas. Se usó la misma idea: compradores simulados con perfiles, más Monte Carlo con 1.000 corridas por escenario. Los supuestos están en `simulacion_6_meses_A.py`. **El dato que más cambia el resultado es el precio real de la competencia, que no conocemos.**

## Supuestos
- **Precio:** el "recomendado" (~10% neto) de `precios_minimos_productos_A.csv`. Tarifas de Mercado Libre iguales a las de `calc_ganancia_meli.py`.
- **Vendedor nuevo:** arranca con ~45% de visibilidad y confianza. Llega al 100% recién cerca de las 60 ventas.
- **Visitas:** entre 130 y 320 por mes para cada publicación, según el grupo. Mercado Libre muestra menos las publicaciones más caras que la competencia (factor (precio de mercado / tu precio)²).
- **Perfiles de comprador:**

  | Perfil | Compra si tu precio está hasta… sobre el de mercado |
  |---|---|
  | Cazador de precio | +3% |
  | Confianza en la marca | +12% (y le pesa mucho tu reputación) |
  | Regalo | +20% (pesa mucho en diciembre en A3, A4 y A5) |
  | Urgente | +25% (baterías, cubiertas, service) |

- **Estacionalidad:**
  - Diciembre: regalos (A4 ×2,6). Las publicaciones arrancan a mitad de mes y el corte de regalos es ~18/12.
  - Enero y febrero: viajes (A3).
  - Mayo: Hot Sale y frío (baterías).
- **Otros costos:** 3% de devoluciones. Mercado Ads en diciembre para A4 y A5 (+50% de visitas, 6% de lo vendido).
- **No incluye:** inflación, cambios de tarifas, quiebres de stock ni impuestos fuera de Mercado Libre.

## Resultado

| Escenario | Unidades (p10–med–p90) | Facturación (med.) | **Ganancia neta 6 meses (p10–med–p90)** |
|---|---|---:|---|
| **Base:** la competencia vende al sugerido de Presmar | 716 – **852** – 995 | $179,8 M | $13,1 M – **$15,9 M** – $18,4 M |
| **Competencia agresiva:** vende 10% por debajo del sugerido | 310 – **428** – 564 | $108,4 M | $6,5 M – **$9,4 M** – $12,7 M |

Ventas por mes (mediana, escenario base): dic 95 · ene 179 · feb 146 · mar 123 · abr 122 · may 186.

### Por grupo (mediana, escenario base)
| Grupo | Unidades | Facturación | Ganancia | Qué pasó |
|---|---:|---:|---:|---|
| **A4** Midland / NOCO / H5 | 445 | $150,0 M | **$13,0 M (82%)** | Sostiene el negocio. Precio por debajo del mercado, pico en dic y en mayo (Hot Sale) |
| A3 SP Connect / K10 | 149 | $14,9 M | $1,4 M | Vende moderado. Funda Extrema y SP52400 son las mejores |
| A5 Muc-Off | 75 | $11,9 M | $1,0 M | Solo los kits grandes (Valija x10, x8) |
| A2 Baterías | 61 | $4,2 M | $0,4 M | Solo Motobatt MTZ7S, Kronwell PSTX7L y PS12V7-3B. El resto no vende |
| A1 Trabas | 0 | 0 | 0 | Precio 13–27% sobre el mercado: casi nadie compra |
| A6 Kit service | 0 | 0 | 0 | $45.900 contra un mercado de ~$34.000 |
| A7 Chaoyang | 0 | 0 | 0 | Precio 39–59% sobre el mercado |

Detalle por producto y por mes: `simulacion_6m_base.csv` y `simulacion_6m_agresiva.csv`.

## Lecturas
1. **A4 da ~80% de la ganancia** en los dos escenarios. Cada producto A4 vende ~55–60 unidades en 6 meses (~10 por mes) en el escenario base.
2. **Los productos que tuvieron que subir de precio para no perder (A1, A2 chicas, A6, A7) casi no venden.** Ganan solo en las corridas en que la competencia, por azar, ya vendía caro. Confirma que no sirven para Mercado Libre con el costo actual.
3. **Enero y mayo venden más que diciembre.** Diciembre se pierde en parte porque una cuenta nueva arranca con poca visibilidad y el corte de regalos llega rápido. **Publicar lo antes posible es lo que más rinde.**
4. **Capital de trabajo:** vender ~445 unidades de A4 implica comprar ~$100 M en mercadería en 6 meses, en rotación. Esto no lo limita el modelo, así que el resultado real va a depender de cuánto stock puedas financiar.
5. **Riesgo principal:** si la competencia ya vende 10% más barato, la ganancia cae ~40%, pero sigue positiva gracias a A4.

## Cómo hacerla real
Apenas publiques, `consultar_visitas` y `consultar_ventas` del conector de Mercado Libre dan las visitas y la conversión reales. Con eso se recalibra este modelo cada mes (`VIS` y la probabilidad de compra en `PERF`).
