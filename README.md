# Capacitated Hub Location Problem — BOA & AE-BOA

## 📘 Descripción del proyecto
Este proyecto reproduce y amplía un algoritmo bioinspirado tipo **Bobcat Optimization Algorithm (BOA)** aplicado al **problema de localización de hubs con capacidad limitada y distancia máxima (Capacitated Hub Location Problem, CHLP)**.  
El objetivo es comparar el rendimiento del **BOA original** con una **variante adaptativa (AE-BOA)** que introduce mecanismos dinámicos de exploración y mutación para mejorar la convergencia y evitar estancamiento prematuro.

El repositorio incluye:
- Reproducción completa de los experimentos del artículo original.  
- Implementación de la variante AE-BOA.  
- Análisis estadístico (media, desviación estándar, QMetric).  
- Figuras de convergencia, boxplots y métricas de calidad.  

---

## ⚙️ Instrucciones de instalación

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/tu_usuario/CHLP-BOA-AEBOA.git
cd CHLP-BOA-AEBOA
```

### 2️⃣ Crear y activar un entorno virtual (opcional pero recomendado)
```bash
python -m venv venv
source venv/bin/activate    # En Linux / macOS
venv\Scripts\activate       # En Windows
```

### 3️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

## 🧩 Dependencias principales

| Paquete | Versión recomendada | Uso principal |
|----------|--------------------|---------------|
| Python | ≥ 3.10 | Entorno base |
| NumPy | 1.26+ | Operaciones numéricas y manejo de vectores |
| Matplotlib | 3.8+ | Gráficas (convergencia, boxplots, QMetric) |
| pandas | 2.2+ | Estadísticos descriptivos y manejo de resultados |
| tqdm | 4.66+ | Barras de progreso durante las iteraciones |
| random / math | nativo | Operaciones estocásticas y funciones básicas |

> Todas las versiones exactas están listadas en `requirements.txt`.

