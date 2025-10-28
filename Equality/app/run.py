"""
Script de inicio rápido para el Panel BI.
Verifica dependencias y lanza la aplicación Streamlit.
"""

import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Verifica que la versión de Python sea compatible."""
    if sys.version_info < (3, 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True


def check_dependencies():
    """Verifica que las dependencias estén instaladas."""
    required_packages = [
        'streamlit',
        'pandas',
        'numpy',
        'plotly',
        'scipy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NO INSTALADO")
            missing_packages.append(package)
    
    if missing_packages:
        print("\n⚠️  Faltan dependencias. Instalando...")
        try:
            subprocess.check_call([
                sys.executable, 
                "-m", 
                "pip", 
                "install", 
                "-r", 
                "requirements.txt"
            ])
            print("✅ Dependencias instaladas correctamente")
            return True
        except subprocess.CalledProcessError:
            print("❌ Error al instalar dependencias")
            print("   Ejecuta manualmente: pip install -r requirements.txt")
            return False
    
    return True


def check_data_file():
    """Verifica que el archivo de datos exista."""
    data_file = Path(__file__).parent.parent / "data" / "ESS11.csv"
    
    if data_file.exists():
        print(f"✅ Archivo de datos encontrado: {data_file}")
        return True
    else:
        print(f"❌ Archivo de datos NO encontrado: {data_file}")
        print("   Asegúrate de que ESS11.csv esté en la carpeta 'data'")
        return False


def launch_app():
    """Lanza la aplicación Streamlit."""
    print("\n🚀 Iniciando Panel BI...")
    print("   La aplicación se abrirá en tu navegador")
    print("   URL: http://localhost:8501")
    print("\n   Presiona Ctrl+C para detener el servidor\n")
    
    app_file = Path(__file__).parent / "app.py"
    
    try:
        subprocess.run([
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(app_file)
        ])
    except KeyboardInterrupt:
        print("\n\n✅ Servidor detenido")
    except Exception as e:
        print(f"\n❌ Error al iniciar la aplicación: {e}")


def main():
    """Función principal."""
    print("=" * 60)
    print("Panel BI - Igualdad en Europa (ESS11)")
    print("Verificación de sistema")
    print("=" * 60)
    print()
    
    # Verificaciones
    if not check_python_version():
        return
    
    print()
    if not check_dependencies():
        return
    
    print()
    if not check_data_file():
        print("\n⚠️  Continuar sin datos puede causar errores")
        response = input("¿Deseas continuar de todas formas? (s/n): ")
        if response.lower() != 's':
            return
    
    print()
    print("=" * 60)
    
    # Lanzar aplicación
    launch_app()


if __name__ == "__main__":
    main()
