# Proyecto de Gestión de Recetas con Asistente Virtual (LangChain + Gemini + RAG)

Este proyecto tiene como objetivo crear una plataforma web donde los usuarios puedan cargar sus recetas en formato PDF, hacer consultas en lenguaje natural, y recibir recomendaciones basadas en sus preferencias y consultas anteriores. Utiliza tecnologías como **LangChain**, el modelo **Gemini**, y la metodología **RAG** (Retrieval-Augmented Generation) para ofrecer una experiencia personalizada e intuitiva.

## Estructura General del Proyecto

### 1. Frontend y Diseño de la Interfaz (UI/UX)
**Responsable:** Miembro 1  
**Objetivo:** Crear una interfaz intuitiva y amigable donde los usuarios puedan cargar sus recetas, ver sugerencias y consultar el historial de interacciones.

#### Tareas:
- Diseñar la interfaz utilizando **HTML/CSS** y frameworks como **Bootstrap** para formularios y carga de archivos PDF.
- Implementar una sección donde los usuarios puedan ver sus recetas recomendadas y el historial de consultas.
- Crear un diseño claro y funcional para que los usuarios puedan visualizar y modificar los documentos cargados.
- Asegurarse de que la interfaz sea **responsiva** para ofrecer una experiencia fluida en dispositivos móviles y de escritorio.

### 2. Integración del Asistente Virtual (Backend + LangChain + Gemini + RAG)
**Responsable:** Miembro 2  
**Objetivo:** Implementar un asistente virtual que procese los documentos PDF y consultas en lenguaje natural, proporcionando recomendaciones personalizadas.

#### Tareas:
- Configurar **LangChain** para interactuar con el modelo **Gemini** usando la metodología **RAG**:
- Procesar los archivos PDF y convertirlos en **embeddings** para búsqueda semántica:
  - Implementar funciones en **Python** para convertir los PDFs en embeddings y almacenarlos en la base de vectores.
  - Utilizar herramientas como **FAISS** para gestionar los embeddings.
- Asegurar que el asistente recuerde consultas pasadas utilizando la **memoria conversacional** de LangChain para mejorar las respuestas basadas en interacciones anteriores.

### 3. Base de Datos y Gestión de Documentos
**Responsable:** Miembro 1
**Objetivo:** Gestionar tanto la base de datos de recetas como la base de vectores para facilitar la búsqueda semántica y las recomendaciones.

#### Tareas:
- Configurar una base de datos **SQLite** para almacenar la información de usuarios, recetas y su historial de consultas.
- Implementar la estructura de la **base de vectores** para almacenar los embeddings de los documentos cargados.
- Crear funciones **CRUD** para gestionar los documentos y que el asistente acceda a las recetas a través de consultas semánticas.
- Relacionar las consultas de los usuarios con los embeddings almacenados para mejorar la precisión en las recomendaciones.

### 4. Flujo de Usuario, Memoria y Optimización del Proyecto
**Responsable:** Tú  
**Objetivo:** Integrar todos los componentes del proyecto (frontend, backend, base de datos, memoria) y garantizar una experiencia de usuario fluida y eficiente.

#### Tareas:
- Supervisar la integración del **frontend**, el asistente con RAG, la base de datos y la base de vectores.
- Asegurarte de que el flujo de usuario sea intuitivo: cargar recetas en PDF, realizar consultas y recibir recomendaciones relevantes.
- Implementar la **memoria** en el asistente usando **LangChain’s Memory** para mejorar las respuestas personalizadas.
- Optimizar la interacción entre los **embeddings** y las consultas en lenguaje natural, asegurando que el modelo utilice el contexto relevante.

## Plan de Etapas del Proyecto

### Martes: Configuración Inicial
- Todos los miembros deben configurar el entorno de desarrollo, instalando **Flask**, **LangChain**, el modelo **Gemini**, y la base de vectores (**FAISS** o **Weaviate**).
- Definir el flujo de usuario y la estructura de la interfaz, incluyendo la carga de documentos PDF.

### Miercoles: Progreso Individual
- **Miembro 1**: Prototipo del frontend con formularios para cargar PDFs.
- **Miembro 2**: Implementar la conversión de PDFs en embeddings usando LangChain.
- **Miembro 3**: Configurar la base de vectores para almacenar y gestionar los embeddings de las recetas.

### Jueves: Integración y Pruebas Iniciales
- Integrar el backend (asistente + embeddings) con el frontend, permitiendo que los documentos cargados puedan ser utilizados en consultas.
- Implementar una **memoria básica** en el asistente para recordar interacciones pasadas.

### Viernes: Pulido y Optimización
- Completar pruebas de usuario: cargar documentos, realizar consultas, recibir respuestas.
- Optimizar la interfaz y mejorar el flujo de usuario. Asegurar que las recomendaciones basadas en los PDFs sean precisas y útiles.

## Tecnologías y Herramientas Utilizadas
- **Flask**: Para la creación de la aplicación web.
- **LangChain**: Para la gestión de interacciones y la integración con el modelo Gemini.
- **Gemini**: Modelo de lenguaje para la generación de respuestas.
- **RAG** (Retrieval-Augmented Generation): Para mejorar las respuestas del modelo usando documentos cargados por los usuarios.
- **FAISS** o **CHROMA**: Para gestionar los embeddings de los documentos PDF.
- **SQLite**: Para almacenar recetas, usuarios y el historial de consultas.
- **Bootstrap**: Para el diseño de una interfaz responsiva y amigable.
