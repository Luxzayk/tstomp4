# Convertir TS a MP4

Script de Python para convertir por lotes archivos de video `.ts` a `.mp4`
usando [FFmpeg](https://ffmpeg.org/).

El script realiza una conversión rápida porque copia los streams de video y
audio sin recodificarlos. También agrega la opción `faststart` para facilitar
la reproducción progresiva de los archivos MP4.

## Requisitos

- Python 3.8 o superior.
- FFmpeg instalado y disponible en el `PATH` del sistema.

Para comprobar que FFmpeg está disponible, ejecuta:

```powershellll
ffmpeg -version
```

Si el comando no se reconoce, instala FFmpeg y agrega la carpeta que contiene
`ffmpeg.exe` al `PATH`.

## Configuración

Abre [`convertir_ts_mp4.py`](./convertir_ts_mp4.py) y modifica estas variables:

```python
CARPETA = Path(r"C:\ruta\a\tus\videos")
INCLUIR_SUBCARPETAS = True
```

- `CARPETA`: carpeta donde se encuentran los archivos `.ts`.
- `INCLUIR_SUBCARPETAS`:
  - `True`: busca archivos `.ts` en la carpeta y en todas sus subcarpetas.
  - `False`: busca únicamente en la carpeta indicada.

Se recomienda utilizar una cadena `raw` (`r"..."`) en las rutas de Windows
para evitar problemas con las barras invertidas.

## Uso

Desde PowerShell, sitúate en la carpeta del proyecto y ejecuta:

```powershell
python .\convertir_ts_mp4.py
```

El programa:

1. Verifica que la carpeta configurada exista.
2. Busca los archivos con extensión `.ts`.
3. Crea un archivo `.mp4` con el mismo nombre y en la misma ubicación.
4. Omite los MP4 que ya existan; no sobrescribe archivos.
5. Muestra el progreso y el resultado de cada archivo.

Ejemplo:

```text
Videos encontrados: 2

[1/2] Procesando: video-01.ts
[OK] video-01.ts -> video-01.mp4

[2/2] Procesando: video-02.ts
[OMITIDO] Ya existe: video-02.mp4

Proceso finalizado.
```

## Cómo funciona la conversión

El comando de FFmpeg utilizado equivale a:

```text
ffmpeg -hide_banner -loglevel error -i archivo.ts ^
  -map 0:v? -map 0:a? -c copy -bsf:a aac_adtstoasc ^
  -movflags +faststart -n archivo.mp4
```

- `-c copy` evita la recodificación y conserva la calidad original.
- `-map 0:v?` y `-map 0:a?` incluyen video y audio cuando están disponibles.
- `-bsf:a aac_adtstoasc` adapta audio AAC de MPEG-TS al contenedor MP4.
- `-movflags +faststart` mueve los metadatos necesarios al inicio del archivo.
- `-n` evita sobrescribir archivos existentes.

Como no se recodifica el contenido, el proceso normalmente es rápido. Sin
embargo, la conversión puede fallar si los codecs contenidos en el archivo
`.ts` no son compatibles con el contenedor MP4.

## Notas y solución de problemas

### La carpeta no existe

Comprueba el valor de `CARPETA` y verifica que la ruta sea correcta. En
Windows puedes usar una ruta absoluta, por ejemplo:

```python
CARPETA = Path(r"D:\Videos\Grabaciones")
```

### No se encontraron archivos `.ts`

Verifica que los archivos tengan realmente la extensión `.ts`. Si están dentro
de subcarpetas, asegúrate de que `INCLUIR_SUBCARPETAS` sea `True`.

### FFmpeg no está instalado o no está en el `PATH`

Instala FFmpeg, agrega su carpeta `bin` al `PATH` y abre una nueva terminal.
Después vuelve a comprobarlo con `ffmpeg -version`.

### La conversión falla

Ejecuta FFmpeg manualmente sobre uno de los archivos para obtener más
información:

```powershell
ffmpeg -i "C:\ruta\a\video.ts" -c copy "C:\ruta\a\video.mp4"
```

Al usar `-c copy`, algunos codecs o combinaciones de streams pueden no ser
válidos dentro de un contenedor MP4. En ese caso sería necesario recodificar
el archivo con los codecs apropiados.

## Estructura del proyecto

```text
tstomp4/
├── convertir_ts_mp4.py
└── README.md
```

## Licencia

No se ha especificado una licencia para este proyecto.
