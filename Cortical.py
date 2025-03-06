# -*- coding: utf-8 -*-
"""
------------------------------------------------------------------------------
# Cortical

Crea , calcula porosidad, malla y resuelve (solo conductividad efectiva) de un modelo

* usa FENICSX en modo real (solo conductividad)
* necesita en la misam carpeta: 1-Genera_Modelo.py
                                2-Porosidad.py
                                3-Mallado.py
                                4-Solve.py


@author: mjcervantes (Version Feb_2025)



------------------------------------------------------------------------------
"""


from Genera_Modelo import generar_modelo
from Porosidad import calcular_porosidad
from Mallado import generar_mallado
from Solve import resolver_modelo




nombre ="Modelo_0"
densidad = 23#10-25

# 1- Generar el modelo
generar_modelo(nombre, densidad)


# 2- Calcular la porosidad
porosidad = calcular_porosidad(nombre)

# 3-  Generar el mallado
generar_mallado(nombre)

# # 4- Resolver el modelo
conductividad = resolver_modelo(nombre)/1e-3


#%%
print("--------------resultados----------------------------------")
print(f"Porosidad: {(100*porosidad):.2f} %")
print(f"Conductividad efectiva (mS/m): {conductividad:.2f}")

