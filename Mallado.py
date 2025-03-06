# -*- coding: utf-8 -*-
"""
------------------------------------------------------------------------------
# Mallado

* malla el .geo obtenido de Genera_Modelo.py


@author: mjcervantes (Version Feb_2025)



------------------------------------------------------------------------------
"""


def generar_mallado(modelo):
    
    import subprocess
    def run_gmsh(geo_file):
        """Ejecuta Gmsh para mallar un archivo .geo."""
        try:
            subprocess.run(["gmsh", "-3", geo_file], check=True)
           
        except subprocess.CalledProcessError as e:
            print(f"Error al generar la malla para {geo_file}: {e}")
            raise  # Relanza la excepción para manejar el error fuera de la función

    geo_file = str(modelo)+".geo"  # Nombre del archivo .geo
    
    print("-- Generando malla con Gmsh --")
    run_gmsh(geo_file)
    
    print(f"-- Malla de {modelo} generada con exito --")
    return modelo