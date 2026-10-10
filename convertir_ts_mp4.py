
import subprocess
from pathlib import Path

# CAMBIA ESTA RUTA por la carpeta donde estan tus videos
CARPETA = Path(r"C:\ruta")

# True: busca tambien dentro de las subcarpetas
INCLUIR_SUBCARPETAS = True


def convertir(archivo_ts):
    salida = archivo_ts.with_suffix(".mp4")

    # No sobrescribir videos MP4 existentes
    if salida.exists():
        print(f"[OMITIDO] Ya existe: {salida.name}")
        return

    comando = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel", "error",
        "-i", str(archivo_ts),
        "-map", "0:v?",
        "-map", "0:a?",
        "-c", "copy",
        "-bsf:a", "aac_adtstoasc",
        "-movflags", "+faststart",
        "-n",
        str(salida)
    ]

    try:
        resultado = subprocess.run(comando)

        if resultado.returncode == 0:
            print(f"[OK] {archivo_ts.name} -> {salida.name}")
        else:
            print(f"[ERROR] No se pudo convertir: {archivo_ts.name}")
            # Eliminar salida incompleta, si se creo
            if salida.exists() and salida.stat().st_size == 0:
                salida.unlink()

    except FileNotFoundError:
        print("[ERROR] FFmpeg no esta instalado o no esta en el PATH.")
        raise


def main():
    if not CARPETA.is_dir():
        print(f"La carpeta no existe: {CARPETA}")
        return

    patron = "**/*" if INCLUIR_SUBCARPETAS else "*"
    archivos = [
        p for p in CARPETA.glob(patron)
        if p.is_file() and p.suffix.lower() == ".ts"
    ]

    if not archivos:
        print("No se encontraron archivos .ts.")
        return

    print(f"Videos encontrados: {len(archivos)}\n")

    for i, archivo in enumerate(archivos, 1):
        print(f"\n[{i}/{len(archivos)}] Procesando: {archivo.name}")
        convertir(archivo)

    print("\nProceso finalizado.")


if __name__ == "__main__":
    main()
