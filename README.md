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

## 🚀 Cómo ejecutar los experimentos

Cada conjunto de pruebas corresponde a una instancia de diferente complejidad:

| Script | Descripción | Parámetros principales |
|--------|--------------|------------------------|
| `run_simple.py` | Instancia simple (10 partículas, 100 iteraciones) | Rápida convergencia inicial |
| `run_medium.py` | Instancia media (15 partículas, 500 iteraciones) | Mayor estabilidad |
| `run_hard.py` | Instancia dura (20 partículas, 1000 iteraciones) | Evaluación más exigente |
| `run_variant.py` | Variante AE-BOA (20 partículas, 1000 iteraciones) | Exploración adaptativa |

### 🧠 Ejemplo de ejecución

```bash
python run_hard.py
```
Los resultados se almacenan automáticamente en la carpeta `results/`, incluyendo los archivos `.csv` con estadísticas y las figuras generadas.

## 📊 Cómo generar las figuras del reporte

Una vez finalizada la ejecución de un script, las figuras se crean de forma automática y se guardan en el subdirectorio correspondiente dentro de `results/`:

| Figura | Descripción | Archivo generado |
|---------|--------------|------------------|
| Boxplot | Distribución del mejor fitness en múltiples ejecuciones | `Boxplot_simple.png`, `Boxplot_media.png`, `Boxplot_dura.png` |
| Convergencia | Evolución del mejor fitness por iteración | `Convergencia_simple.png`, `Convergencia_media.png`, `Convergencia_dura.png` |
| QMetric | Evaluación de calidad por iteración | `QMetric_simple.png`, `QMetric_media.png`, `QMetric_dura.png` |

### 🧩 Regenerar figuras manualmente

Si deseas regenerar las figuras de forma manual, ejecuta:

```bash
python plot_results.py
```

## 📂 Descripción de los archivos principales

| Archivo / Carpeta | Contenido |
|--------------------|-----------|
| `run_simple.py` | Ejecución del BOA en instancia simple |
| `run_medium.py` | Ejecución del BOA en instancia media |
| `run_hard.py` | Ejecución del BOA en instancia dura |
| `run_variant.py` | Ejecución de la variante AE-BOA |
| `boa_core.py` | Implementación del algoritmo base del Bobcat Optimization Algorithm |
| `variant_module.py` | Módulos adicionales (mutación adaptativa, factor α(t)) |
| `results/` | Carpeta con resultados estadísticos y figuras |
| `requirements.txt` | Lista completa de dependencias y versiones |
| `README.md` | Descripción general del proyecto |

---

## 📈 Resultados esperados

- **BOA original:** Convergencia rápida pero tendencia al estancamiento en óptimos locales.  
- **AE-BOA:** Búsqueda más diversa, oscilación controlada del fitness y mejora en la exploración globa

---

## 🧾 Créditos y atribución

Este repositorio reproduce y amplía los experimentos descritos en el artículo:

> **Fabián Alexis Vidal Torres**  
> *Implementación del Algoritmo Bioinspirado Bobcat para un Problema de Optimización en un contexto de Asignación de Hubs*  
> Escuela de Ingeniería Informática, Universidad de Valparaíso, Chile.

La reproducción fue realizada con fines educativos y de análisis comparativo, respetando la autoría intelectual del trabajo original.
