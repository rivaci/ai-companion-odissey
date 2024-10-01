import traceback

def generate_error():
    try:
        raise ValueError("Ceci est une fausse erreur pour voir la stacktrace.")
    except Exception as e:
        print("Une erreur s'est produite :")
        traceback.print_exc()  # Affiche la stacktrace sans interrompre le programme

generate_error()

# Le reste du code continue à s'exécuter normalement
print("Le programme continue après l'erreur.")
