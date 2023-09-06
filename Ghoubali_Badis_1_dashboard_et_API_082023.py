import subprocess
import os

# Chemin relatif pour accéder à api.py et dashboard.py
scripts_directory = "./Ghoubali_Badis_2_dossier_code_082023/Scripts"

# Obtenez les variables d'environnement actuelles
env = os.environ.copy()

# Modifiez la variable d'environnement PORT
env["PORT"] = "5000"

# Exécutez api.py avec python avec la nouvelle variable d'environnement
subprocess.Popen(["python", f"{scripts_directory}/api.py"], env=env)

# Exécutez dashboard.py avec streamlit
subprocess.Popen(["streamlit", "run", f"{scripts_directory}/dashboard.py", "--server.port", "8000"], env=env)


