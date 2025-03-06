# -*- coding: utf-8 -*-
"""
------------------------------------------------------------------------------
# Genera modelos cubicos de hueso cortical

-------------------------------------------------------------------------
"""


def generar_modelo(nombre,density ):

    
    import numpy as np
    import networkx as nx
    import matplotlib.pyplot as plt
    import random
    from scipy.stats import qmc
    from scipy.spatial import distance_matrix
    import random
    import math
    
    
    
#%%  
    
      
    
    # ------ Sample
    cube_size = 1.0 #lado (mm)
    density =25

    # ----- Osteon  (mm)
    Ost_d_min = 0.1
    Ost_d_max = 0.25

    #
    # Diameters Haversian canals (mm)
    Hav_d_min = 0.04#0.05
    Hav_d_max = 0.09#0.1
    # Inclination angle Haversian canals
    Hav_a_min = 0
    Hav_a_max = 15

    # ------ Volkmanns canals
    # Diameters Volkmanns canals (mm)
    Volk_d_min = 0.04#0.05
    Volk_d_max = 0.05#0.08
    # Inclination angle Volkmanns canals
    Volk_a_min = 0
    Volk_a_max = 15
    # Distance Volkmanns canals (mm)
    #Volk_dist_min = 0.5
    #Volk_dist_max = 0.15
    




    
    #%% No Modificables
    
    
    
    def generate_random_nodes(num_nodes, area_size, min_distance):
        nodes = []
    
        l_bounds = [-area_size/2]
        u_bounds = [area_size/2]
        sampler = qmc.Sobol(2, scramble=True)
        X = sampler.random_base2(22)
        X = qmc.scale(X, l_bounds, u_bounds)
    
    
        i= -1
        while len(nodes) < num_nodes:
    
            i=i+1
    
            # Generar coordenadas aleatorias para un nodo
            x = float(X[i][0])
            y =float(X[i][1])
    
    
            # Verificar si el nodo se solapa con algún nodo existente
            is_overlapping = False
            for (nx, ny) in nodes:
                distance = math.sqrt((x - nx) ** 2 + (y - ny) ** 2)
                if min_distance > distance:
                    is_overlapping = True
                    break
    
                # Si no se solapa, añadir el nodo a la lista
            if not is_overlapping:
    
    
                nodes.append((x, y))
    
        return nodes
    
    
    
    def connection(nodes):
        nodes=np.array(nodes)
        pos=nodes
        distancias = distance_matrix(pos,pos)
    # Conectar cada cilindro con el más cercano y, si ya tiene una conexión, con el siguiente más cercano
        conexion =[]
    
        for i in range(len(nodes)):
    
            distancias = distance_matrix(pos, pos)
            # Ordenar distancias y obtener los índices de los cilindros más cercanos
            indices_cercanos = np.argsort(distancias[i])
    
            # Intentar conectar con el más cercano
            conectado = False
            for j in indices_cercanos[1:]:  # Empezar desde 1 para evitar conectar consigo mismo
                if not G.has_edge(i, j):
                    G.add_edge(i, j)
    
                    conexion.append((i,j))
                    conectado = True
                    break
        return  conexion
    
    
    
    def find_coord(center, dx,dy, z_n):
    
        x = center[0]
        y = center[1]
        z = center[2]
    
    
        x_z = x+math.tan(math.asin(dx))*(z_n-z)
        y_z = y+math.tan(math.asin(dy))*(z_n-z)
        return x_z, y_z
    
    def generate_vertical(nodes):
    
          sampler = qmc.Sobol(1, scramble=True)
          R = sampler.random_base2(14)
          R_O = qmc.scale(R, Ost_d_min/2, Ost_d_max/2)
          R_H = qmc.scale(R, Hav_d_min/2, Hav_d_max/2)
    
          ang_x = random.uniform(-Hav_a_max, Hav_a_max)
          ang_y = random.uniform(-Hav_a_max, Hav_a_max)
    
          Cyl=[]
          k=0
          for  (nx, ny) in nodes:
              ang_x = random.uniform(-Hav_a_max, Hav_a_max)
              ang_y = random.uniform(-Hav_a_max, Hav_a_max)
              nz = -cube_size/2
    
              Cyl.append(((nx, ny,nz),math.sin(math.pi*ang_x/180)*cube_size,math.sin(math.pi*ang_y/180)*cube_size,math.cos(math.pi*ang_x/180)*math.cos(math.pi*ang_y/180)*cube_size,R_O[k][0], R_H[k][0]))
              k=1+k
          return Cyl
    
    
    def generate_horizontal(node, conexion):
    
    
    
        z = random.uniform(-cube_size/4, cube_size/4)
        radius_Volk = random.uniform(Volk_d_min/2, Volk_d_max/2)
    
        ang_z = random.uniform(-Volk_a_max, Volk_a_max)
    
        Cyl_H=[]
    
        for  (ni, nj) in conexion:
    
    
            cyl_1 = cyl_V[ni]
            cyl_2 =cyl_V[nj]
    
    
    
            nx_1,ny_1 = find_coord(cyl_1[0], cyl_1[1],cyl_1[2], z)
            nx_2,ny_2 = find_coord(cyl_2[0], cyl_2[1],cyl_2[2], z)
    
            Cyl_H.append(((nx_1, ny_1,z),nx_2-nx_1,ny_2-ny_1,math.sin(ang_z*math.pi/180),radius_Volk))
    
        return  Cyl_H
    
    
    
    
    #%%
    # Parámetros
    
    area_size = cube_size**2
    num_nodes =density * area_size
    min_distance = (Ost_d_max+Ost_d_min)/2 # Distancia mínima entre nodos
    
    
    #%%
    
    # # Crear un grafo para representar las conexiones
    G = nx.Graph()
    nodes = generate_random_nodes(num_nodes, area_size, min_distance)
    # Generar nodos
    for i in range (int(num_nodes)):
        G.add_node(i, pos=nodes)
    pos=nodes
    
    conexion = connection(nodes)
    
    cyl_V = generate_vertical(nodes)
    cyl_H =generate_horizontal(nodes, conexion)
    
    
    #%% plot vertical
    
    fig, axs = plt.subplots(figsize=(8, 8))
    # Dibujar el grafo usando las posiciones especificadas
    nx.draw(G, pos, node_size=1, node_color='lightblue')
    #plt.show()
    # #%%
    # # Visualizar nodos
    
    for i in range(len(nodes)):
        x = nodes[i][0]
        y = nodes[i][1]
        radius_Ost = cyl_V[i][4]
    
        # circle=plt.Circle((x,y),radius_Ost, color='b')
        # axs.add_patch(circle)
        radius_Hav = cyl_V[i][5]
        circle2=plt.Circle((x,y),radius_Hav,color='r')
        axs.add_patch(circle2)
    
        axs.plot(x, y, 'ko', markersize=10)  # Nodos azules
        axs.text(x, y, str(i), fontsize=12, ha='right')  # Etiqueta con el índice del nodo
    
    axs.set_xlim(-area_size/2, area_size/2)
    axs.set_ylim(-area_size/2, area_size/2)
    axs.grid(True)
    plt.show()
    
    # Calcular la matriz de distancias
    #%% #%% Genereter Gmsh Script  (.geo)
    
    gmsh_script_introduction = """//                                Cube with cylindrical inclusions\n
    //----------------------------------------------------------------------------------------------------------------------------
    \n\n//Geometry\n\n
    
    SetFactory("OpenCASCADE");\n"""
    
    gmsh_script_environment = """\n\n// Environment\n\n"""
    gmsh_script_environment +="Box(1)"+" = {{{}, {}, {}, {}, {}, {}}};\n".format(-cube_size/2,-cube_size/2,-cube_size/2,cube_size,cube_size,cube_size)
    
    
    gmsh_script_inclusion ="""\n\n// Inclusions\n\n"""
    
    # # Osteons-Havers Canals
    
    
    #l=0
    for i, (center,dx,dy,dz,radius_O, radius_H,) in enumerate(cyl_V):
    
    
        # gmsh_script_inclusion += "Cylinder({}) = {{{}, {}, {}, Sin({})*{}, Sin({})*{},Cos({})*Cos({})*{}, {}}};\n".format(i+l, center[0], center[1], 0,ang_dx, cube_size, ang_dy, cube_size,ang_dx, ang_dy, cube_size, radius_O)
    
        gmsh_script_inclusion += "Cylinder({}) = {{{}, {}, {},{}, {}, {},{}}} ;\n".format(i+2, center[0], center[1], center[2],dx,dy,dz, radius_H)
    
       # l=l+1
    #j=l
    
    # Volkmann Canals
    
    for  j, (center,dx,dy,dz,radius_V) in enumerate(cyl_H):
    
    
        # # Volkmann Canals
    
        gmsh_script_inclusion += "Cylinder({}) = {{{}, {}, {},{}, {}, {},{}}} ;\n".format(j+3+i, center[0], center[1], center[2],dx,dy,dz, radius_V)
    
    
    
    k=j+3+i
    
    
    # Boolean Operation
    gmsh_script_Bool = """\n\n// Boolean Operation\n\n"""
    gmsh_script_Bool += "volUnion() = BooleanUnion{Volume{2:"+"{}".format(i+2)+"}; Delete;}{Volume{"+"{}".format(i+2+1)+":"+"{}".format(k)+"}; Delete;};\n"
    gmsh_script_Bool += "g() = BooleanIntersection{ Volume{volUnion()};Delete; }{ Volume{1};  };\n"
    gmsh_script_Bool += "f() = BooleanDifference{ Volume{1}; Delete;  }{ Volume{g()};};\n"
    
    # Physical Volume
    n=500
    gmsh_script_physical = """\n\n//Physical Volume\n\n"""
    gmsh_script_physical += "Physical Volume({})".format(n)+"={g()}"+";\n"
    gmsh_script_physical +="Physical Volume({})".format(n+100)+"={f()};\n"
    
    
    # # Physical Surface
    # n=10
    gmsh_script_physical_s = """\n\n//Dummy Physical Surface\n\n"""
    gmsh_script_physical_s += "Physical Surface(10)={160};\n"
    gmsh_script_physical_s += "Physical Surface(20)={163};\n"
    
    # Characteristic Length
    gmsh_script_characteristic = "q() = PointsOf{Volume{g()}; }; Characteristic Length{q()} = "+"{}".format(Volk_d_min/2)+";\n"
    gmsh_script_characteristic += "Coherence;\n"
    gmsh_script_characteristic += "\nMesh.CharacteristicLengthMax = {}".format(Hav_d_min/2)+";\n"
    #Escala
    gmsh_script_characteristic += "\nMesh.ScalingFactor = {}".format(1e-3)+";"

    #%%
    #%% # generate .geo
    nombre = str(nombre)
    
    with open(f"{nombre}.geo", "w") as f:
    
        f.write(gmsh_script_introduction)
        f.write(gmsh_script_environment)
        f.write(gmsh_script_inclusion)
        # f.write(gmsh_script_plane_s)
        f.write(gmsh_script_Bool)
        f.write(gmsh_script_physical)
        f.write(gmsh_script_physical_s)
        f.write(gmsh_script_characteristic)
    
    print(f"--{nombre} generado con éxito-- \n")

    return nombre

# 
