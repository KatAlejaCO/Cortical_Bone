# -*- coding: utf-8 -*-
"""
------------------------------------------------------------------------------
# FEniCSX - Solve de CONDUCTIVIDAD basico de una muestra con FENICSX

FENICSX en modo real (solo conductividad)



***muestra de pruebas


*cubica muestra: modelo_muestra_3c_ejez.msh (sacada de la muestra 3c_cuadrado_1 obtenidos de la muestra 3c_C) 
                 Conductividad efectiva (S/m): 0.09986227146355321



*** dato 
***Con sigma_bone =20e-3 #[S/m] y sigma_medula = 301e-3  #[S/m]

@author: mjcervantes (Version Feb_2025)



------------------------------------------------------------------------------
"""



def  resolver_modelo(modelo):
    
    from mpi4py import MPI
    
    import ufl
    
    from dolfinx import mesh
    from dolfinx import fem
    from dolfinx import default_scalar_type
    from dolfinx.io import gmshio
    from dolfinx.fem.petsc import LinearProblem
    from dolfinx import io
    
    import numpy as np
    from pathlib import Path
    
    #%% Modificable
    
    
    #------------------------------------------------
    
    #-Cubo
    nombre_archivo = str(modelo)
    
    ele = 1.0e-3  # Largo en [mm]
    
    Area = ele*ele  #[mm]
    volumen_cilindro = Area*ele #[mm]
    
    #--------------------------------------------------
    
    
    #Conductividades
    
    sigma_b = 0.8e-6 #[S/m] #Conductividad colageno wet (Marzec et al 2008)
    sigma_m = 600e-3#301e-3  #[S/m]  #Conductividad marrow
    
   
    #Frecuencia
    
    fr = 100E3  #[Hz]
    
    #Fuente, Temperatura variable
    
    U0 = 40.0
    Ug = 0.0
    
    #%% No modificable
    
    
    #-Abro archivo con gmshio y creo el mesh los dominios y los bordes
    
    msh, cell_tags, facet_tags = gmshio.read_from_msh(nombre_archivo+'.msh', MPI.COMM_WORLD, 0, gdim=3)
    
    #-Create facet to cell connectivity required to determine boundary facets
    
    tdim = msh.topology.dim
    fdim = tdim - 1
    msh.topology.create_connectivity(fdim, tdim)
    
    
    #-Defino condiciones de contorno
    
    #defino electrodos 
    #x[0]=eje x,x[1]=eje y ,x[2]=eje z 
    
    V = fem.functionspace(msh, ("P", 1))
    
    
    
    def elec_activo(x):
        return np.isclose(x[2], ele/2)
    
    def elec_pasivo(x):
        return np.isclose(x[2], -ele/2)
    
    
    boundary_activo = mesh.locate_entities_boundary(msh, fdim, elec_activo)
    boundary_pasivo = mesh.locate_entities_boundary(msh, fdim, elec_pasivo)
    
    
    
    bcu_electrode_activo = fem.dirichletbc(default_scalar_type(U0),  fem.locate_dofs_topological(V, fdim, boundary_activo), V)
    bcu_electrode_pasivo = fem.dirichletbc(default_scalar_type(Ug),  fem.locate_dofs_topological(V, fdim, boundary_pasivo), V)
    
    #-Defino conductividades en los dominios
    # (600=Cortical, 500 = marrow) )
    
    Q = fem.functionspace(msh, ("DG", 0))
    
    sigma = fem.Function(Q)
    sigma1 = cell_tags.find(600)
    sigma.x.array[sigma1] = np.full_like(sigma1, sigma_b, dtype=default_scalar_type)
    sigma2 = cell_tags.find(500)
    sigma.x.array[sigma2] = np.full_like(sigma2, sigma_m, dtype=default_scalar_type)
    
    
    ##-- Define variational problem => Tensión en todos los puntos
    
    
    u = ufl.TrialFunction(V)
    v = ufl.TestFunction(V)
    f = fem.Constant(msh, default_scalar_type(0))
    
    a = ufl.inner(sigma*ufl.grad(u), ufl.grad(v)) * ufl.dx
    L = f * v * ufl.dx
    
    problem = LinearProblem(a, L, bcs= [bcu_electrode_activo,bcu_electrode_pasivo], petsc_options={"ksp_type": "cg", "pc_type": "hypre","ksp_rtol ": 1e-10 , "ksp_atol ": 1e-15})
    
    uh = problem.solve()
    
    
    #-Save xdmf con Tensión en todos los puntos, conductividades
    
    results_folder = Path("results")
    results_folder.mkdir(exist_ok=True, parents=True)
    filename = results_folder / "tension"
    #with io.VTXWriter(domain.comm, filename.with_suffix(".bp"), [uh]) as vtx:
        #vtx.write(0.0)
    with io.XDMFFile(msh.comm, filename.with_suffix(".xdmf"), "w") as xdmf:
        xdmf.write_mesh(msh)
        xdmf.write_function(uh)
    
    filename2 = results_folder / "conductividad"
    with io.XDMFFile(msh.comm, filename2.with_suffix(".xdmf"), "w") as xdmf:
        xdmf.write_mesh(msh)
        xdmf.write_function(sigma)
    
    
    ##-- Define variational problem => Densidad de potencia
    
    
    sar = ufl.TrialFunction(V)
    uu = ufl.TestFunction(V)
    aa = sar*uu*ufl.dx
    LL = uu*sigma*ufl.inner(ufl.grad(uh), ufl.grad(uh))*ufl.dx
    
    problemsar = LinearProblem(aa, LL, petsc_options={"ksp_type": "cg", "pc_type": "hypre","ksp_rtol ": 1e-10 , "ksp_atol ": 1e-15})
    
    sarh = problemsar.solve() #densidad de potencia
    
    power = fem.assemble_scalar(fem.form(sarh*ufl.dx))
    
    resistance = (U0)**2/power
    
    
    #print('----------------------------------------------------')
    # print('--Solve--')
    # print(f'Potencia: {power:.2f}')
    # print(f'Impedancia: {resistance:.2f}') #[kilo ohms?]
    
    Sigma_eff = (ele/(resistance*Area))
    
    #print('Conductividad efectiva (S/m):',ele/1000/(resistance*1000*Area/1000**2))
    # print(f'Conductividad efectiva (mS/m): {Sigma_eff:.2f}')
    
    
    
    return Sigma_eff 
    
