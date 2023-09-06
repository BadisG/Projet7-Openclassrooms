import subprocess

# Chemin relatif pour accéder à api.py et dashboard.py
scripts_directory = "./Ghoubali_Badis_2_dossier_code_082023/Scripts"

# Exécutez api.py avec python
subprocess.Popen(["python", f"{scripts_directory}/api.py"])

# Exécutez dashboard.py avec streamlit
subprocess.Popen(["streamlit", "run", f"{scripts_directory}/dashboard.py", "--server.port", "8000"])

