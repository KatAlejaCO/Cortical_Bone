# Cortical bone
## Descripción
Este script en Python está diseñado para modelar, generar mallas y resolver problemas relacionados con la conductividad efectiva y la porosidad de un modelo de hueso cortical. A continuación, te explico las principales secciones del código:

---

### **1. Propósito del script**
El script genera un modelo geométrico de hueso cortical con osteones, canales de Havers y canales de Volkmann. Utiliza herramientas como **Gmsh** para crear geometrías y mallas, y **FEniCSx** para resolver problemas de conductividad eléctrica en el modelo.

---

### **2. Estructura del código**

#### **Importaciones**
El script importa varias bibliotecas:
- **os, subprocess**: Para manejar archivos y ejecutar comandos externos.
- **numpy, scipy, matplotlib**: Para cálculos matemáticos y visualización.
- **networkx**: Para modelar conexiones entre nodos.
- **gmsh**: Para generar geometrías y mallas.
- **dolfinx**: Para resolver problemas de elementos finitos.

---

#### **Clases de parámetros**
Define parámetros geométricos y eléctricos:
- **SAMPLE_parameters**: Tamaño del cubo y densidad de osteones.
- **OSTEON_parameters, HAVERSIAN_CANALS_parameters, VOLKMANNS_CANALS_parameters**: Diámetros y ángulos de los osteones y canales.
- **DIELECTRIC_parameters**: Conductividades eléctricas de la matriz ósea y la médula ósea.
- **Seed**: Semilla para generar números aleatorios reproducibles.

---

#### **Funciones principales**

1. **`generate_model(name, folder)`**
   - Genera un modelo geométrico con osteones y canales.
   - **Subfunciones**:
     - `generate_random_nodes`: Genera nodos aleatorios en un área con una distancia mínima entre ellos.
     - `connection`: Conecta nodos cercanos para modelar canales de Volkmann.
     - `generate_vertical`: Genera cilindros verticales (osteones y canales de Havers).
     - `generate_horizontal`: Genera cilindros horizontales (canales de Volkmann).
   - **Salida**: Un archivo `.geo` con la geometría en formato Gmsh.

---

2. **`calculate_porosity(name, folder)`**
   - Calcula la porosidad del modelo.
   - Usa **Gmsh** para obtener los volúmenes de las regiones (hueso y poros).
   - **Fórmula**:  
     \[
     \text{Porosidad} = \frac{\text{Volumen de los poros}}{\text{Volumen total}}
     \]

---

3. **`generate_mesh(name, folder)`**
   - Genera una malla 3D a partir del archivo `.geo` usando **Gmsh**.
   - Verifica que el archivo `.msh` se haya generado correctamente.

---

4. **`solve_model_z(name, folder)` y `solve_model_x(name, folder)`**
   - Resuelven problemas de conductividad efectiva en las direcciones **z** y **x** respectivamente.
   - **Pasos**:
     1. Carga la malla generada con **Gmsh**.
     2. Define las condiciones de contorno (electrodos en las caras del cubo).
     3. Asigna conductividades a las regiones (hueso y médula).
     4. Resuelve el problema de elementos finitos para calcular:
        - **Tensión eléctrica** en todos los puntos.
        - **Densidad de potencia**.
        - **Conductividad efectiva** usando la fórmula:
          \[
          \sigma_{\text{efectiva}} = \frac{\text{Largo del cubo}}{\text{Resistencia} \cdot \text{Área}}
          \]

---

### **3. Flujo general del script**
1. **Generación del modelo**:
   - Se crean nodos aleatorios y se conectan para formar osteones y canales.
   - Se genera un archivo `.geo` con la geometría.

2. **Cálculo de porosidad**:
   - Se calcula el volumen de los poros y del hueso para determinar la porosidad.

3. **Generación de la malla**:
   - Se genera una malla 3D a partir del archivo `.geo`.

4. **Resolución del modelo**:
   - Se resuelve el problema de conductividad en las direcciones **z** y **x**.
   - Se obtienen resultados como la conductividad efectiva y se guardan en archivos.

---

### **4. Herramientas utilizadas**
- **Gmsh**: Para generar geometrías y mallas.
- **FEniCSx**: Para resolver problemas de elementos finitos.
- **Matplotlib**: Para visualizar el modelo.
- **NetworkX**: Para modelar conexiones entre nodos.

---

### **5. Resultados esperados**
- **Archivos generados**:
  - `.geo`: Geometría del modelo.
  - `.msh`: Malla del modelo.
  - `.xdmf`: Resultados de tensión y conductividad.
- **Cálculos**:
  - Porosidad del modelo.
  - Conductividad efectiva en las direcciones **z** y **x**.

