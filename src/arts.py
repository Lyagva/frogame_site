from src.artConverter import *
from pathlib import Path


# Type file paths according to app.py
class Art:
    current_path = str(Path(__file__).parent.resolve()) + "/../"
    frogameIntroduction = convertToPython(current_path + "arts/frogameIntroduction.txt")
    frogameLogo = convertToPython(current_path + "arts/frogameLogo.txt")
    lyagvaIntroduction = convertToPython(current_path + "arts/lyagvaIntroduction.txt")
