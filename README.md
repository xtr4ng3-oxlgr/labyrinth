# LABYRINTH
![Build](https://github.com/xtr4ng3-oxlgr/labyrinth/actions/workflows/build.yml/badge.svg)
<img width="1672" height="941" alt="labyrinth" src="https://github.com/user-attachments/assets/783856e5-a770-46d1-9fc7-cf7056ccb8da" />

**LABYRINTH** es un generador local de laboratorios defensivos orientado a formación técnica, revisión de incidentes, análisis de logs, manejo seguro de datos sensibles y preparación de proyectos antes de publicarlos.

La herramienta crea casos sintéticos y seguros en carpetas locales. Cada laboratorio incluye artefactos, objetivo, pistas, solución y reportes opcionales.

---

## Propósito

LABYRINTH está diseñado para aprendizaje, práctica y demostración técnica. Permite crear ejercicios reproducibles sin depender de sistemas reales, datos privados, objetivos externos ni entornos activos.

Puede utilizarse para practicar:

- revisión de archivos descargados;
- manejo de datos sensibles;
- preparación de paquetes antes de publicación;
- reconstrucción de líneas temporales;
- revisión de entradas de inicio;
- redacción segura de paquetes de soporte;
- análisis guiado de incidentes simulados.

---

## Características

- Generador local de laboratorios por consola.
- Matriz de escenarios integrada.
- Creación automática de artefactos sintéticos.
- Sistema de pistas progresivas.
- Soluciones incluidas para cada caso.
- Reportes HTML y JSON.
- Exportación de laboratorios en archivo ZIP.
- Escenarios definidos en JSON.
- Estructura modular y ampliable.
- Scripts de ejecución para Windows.
- Script de compilación portable.
- Componentes auxiliares opcionales para extensión educativa.

---

## Escenarios incluidos

```text
suspicious-download
leaked-env
release-hygiene
incident-timeline
startup-entry
support-redaction
```

Cada escenario se encuentra dentro de la carpeta `scenarios/` y puede modificarse, extenderse o reemplazarse.

---

## Instalación

Ejecutar una vez:

```bat
INSTALAR_DEPENDENCIAS.bat
```

O instalar manualmente:

```bash
python -m pip install -r requirements.txt
```

---

## Uso rápido

Abrir la consola interactiva:

```bat
ABRIR_LABYRINTH.bat
```

Desde el menú principal se puede:

```text
[1] Crear laboratorio
[2] Ver matriz de escenarios
[3] Abrir panel de laboratorio local
[4] Solicitar pista
[5] Ver solución
[6] Generar reporte
[7] Exportar laboratorio
[8] Ver guía de uso
[0] Salir
```

---

## Uso por comandos

Listar escenarios disponibles:

```bash
python labyrinth.py list
```

Crear un laboratorio:

```bash
python labyrinth.py create suspicious-download
```

Abrir el panel de un laboratorio:

```bash
python labyrinth.py dashboard "labs/suspicious-download-20260625_120000"
```

Solicitar una pista:

```bash
python labyrinth.py hint "labs/suspicious-download-20260625_120000" --level 1
```

Ver la solución:

```bash
python labyrinth.py solution "labs/suspicious-download-20260625_120000"
```

Generar reporte:

```bash
python labyrinth.py report "labs/suspicious-download-20260625_120000"
```

Exportar laboratorio:

```bash
python labyrinth.py export "labs/suspicious-download-20260625_120000"
```

---

## Estructura del proyecto

```text
labyrinth/
├─ labyrinth.py
├─ src/labyrinth/
├─ scenarios/
├─ docs/
├─ powershell/
├─ native/
├─ build_windows/
├─ assets/
├─ examples/
├─ README.md
├─ SECURITY.md
├─ CONTRIBUTING.md
└─ LICENSE
```

---

## Formato de escenario

Cada escenario se define mediante un archivo `scenario.json`.

Campos principales:

```text
id
name
difficulty
category
objective
brief
artifacts
hints
solution
success_criteria
```

Los artefactos se generan localmente dentro de una carpeta nueva en `labs/`.

---

## Crear nuevos escenarios

Para crear un escenario nuevo:

```text
1. Crear una carpeta dentro de scenarios/
2. Agregar un archivo scenario.json
3. Definir objetivo, artefactos, pistas y solución
4. Ejecutar python labyrinth.py list
5. Crear el laboratorio con python labyrinth.py create <id>
```

Ejemplo de estructura:

```text
scenarios/my-scenario/
└─ scenario.json
```

Los artefactos deben ser seguros y sintéticos. No deben incluir credenciales reales, datos personales reales ni instrucciones que requieran interactuar con sistemas externos.

---

## Modelo de seguridad

LABYRINTH no requiere incidentes reales ni datos sensibles reales.

La herramienta:

- no modifica configuraciones del sistema operativo;
- no ejecuta artefactos generados;
- no se conecta a objetivos externos;
- no recopila información privada;
- no sube archivos;
- no utiliza datos reales;
- no realiza acciones destructivas.

Todos los casos incluidos son locales, sintéticos y seguros para análisis educativo.

---

## Reportes

LABYRINTH puede generar reportes en:

```text
HTML
JSON
```

Los reportes se guardan en la carpeta:

```text
reports/
```

---

## Compilar versión portable

Para generar una versión portable en Windows:

```bat
build_windows\1_COMPILAR_EXE_PORTABLE.bat
```

La salida queda en:

```text
CLIENTE_PORTABLE/
```

---

## Casos de uso

LABYRINTH puede ser útil para:

- estudiantes de ciberseguridad defensiva;
- técnicos de soporte;
- administradores de sistemas;
- analistas junior;
- instructores;
- creadores de laboratorios;
- prácticas de revisión de logs;
- prácticas de manejo seguro de información;
- demostraciones técnicas en portfolio.

---

## Limitaciones

LABYRINTH es una plataforma de entrenamiento local. No reemplaza entornos profesionales de laboratorio, herramientas de análisis avanzadas ni formación especializada.

No realiza análisis automático de sistemas reales.  
No clasifica amenazas reales.  
No ejecuta muestras.  
No consulta servicios externos.  
No debe utilizarse con datos privados reales.

---

# Licencia

<img width="300" height="159" alt="xtr4ng3" src="https://github.com/user-attachments/assets/58e55498-1173-4447-9429-ffc2c6913a92" />

**xtr4ng3**

MIT.
