# FinRadar Panamá S.A.

## Descripción del proyecto

FinRadar Panamá S.A. es un proyecto de la asignatura de Programación II en el que vamos a trabajar con transacciones financieras para analizar sus datos e identificar posibles casos de fraude.

La idea es generar datos de prueba, guardarlos en MongoDB y desarrollar herramientas que nos permitan revisar las transacciones y detectar movimientos sospechosos.

## Tecnologías utilizadas

- Python
- MongoDB
- GitHub
- Jira

## Organización del proyecto

- `config/`: archivos de configuración.
- `domain/`: clases y datos que representan las transacciones y los clientes.
- `repositories/`: funciones para guardar y consultar información.
- `analysis/`: código para analizar las transacciones.
- `services/`: procesos que conectan las diferentes partes del sistema.
- `utils/`: funciones de apoyo para el proyecto.

## Instalación

Para instalar las librerías necesarias, ejecutamos el siguiente comando:

`pip install -r requirements.txt`

## Datos del proyecto

Los datos de prueba se generarán mediante un script y se utilizarán para realizar los análisis. Los archivos CSV y las exportaciones se mantendrán fuera del repositorio de GitHub.

## Fase actual

Fase 1: datos y dominio.