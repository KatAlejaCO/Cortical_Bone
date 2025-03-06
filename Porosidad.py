## -*- coding: utf-8 -*-
"""
------------------------------------------------------------------------------
# Calcula porosidad

Se necesita en la msima carpeta el archivo .geo salida de Genera_Modelo.py 


version (feb 2025)
-------------------------------------------------------------------------
"""

def calcular_porosidad (modelo):
    import sys
    import gmsh
    
    # Inicializar y cargar el archivo .geo
    gmsh.initialize()

    geo_file = str(modelo)+".geo"
    gmsh.open(geo_file)

    # Sincronizar la geometría
    gmsh.model.occ.synchronize()
    
    #print("--Contando poros--")
    

    
    hueso_tag = gmsh.model.getEntitiesForPhysicalGroup(3, 600)
    poros_tags = gmsh.model.getEntitiesForPhysicalGroup(3, 500)
    
    # volumen total del hueso
    vol_hueso = sum(gmsh.model.occ.getMass(3, tag) for tag in hueso_tag)
    
    # volumen de los poros
    vol_poros = sum(gmsh.model.occ.getMass(3, tag) for tag in poros_tags)
    
    # volumen total (hueso + poros)
    vol_total = vol_hueso + vol_poros
    #print(vol_total)
    # porosidad
    phi = (vol_poros / vol_total)
    
    #print(f"--Porosidad de {modelo}  = {phi:.4f}--\n")
     # Imprime solo con dos decimales
    
    # # Finalizar Gmsh
    gmsh.finalize()

    return phi 
