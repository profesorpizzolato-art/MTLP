# 1. Crear el archivo __init__.py si no existe
touch modules/__init__.py

# 2. Forzar que Git registre toda la carpeta 'modules' ignorando reglas previas de cache
git rm -r --cached modules
git add -f modules/
git add app.py

# 3. Confirmar los cambios
git commit -m "Fix: Corrección de rutas de importación y carga forzada de la carpeta modules"

# 4. Subir a GitHub
git push origin main
