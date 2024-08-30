# Importación de librerías
import json # Importa la librería json para trabajar con archivos JSON
import random # Importa la librería random para generar números aleatorios
from Traslate import translate_text # Importa la función translate_text del archivo Translate.py
import colorama # Importa la librería colorama para darle color al texto
import pyttsx3 # Importa la librería pyttsx3 para convertir texto a voz
from dotenv import load_dotenv # Importa la función load_dotenv de la librería dotenv para cargar las variables de entorno
import os # Importa la librería os para acceder a las variables de entorno del sistema
import logging # Importa la librería logging para guardar logs en un archivo de texto
import datetime # Importa la librería datetime para trabajar con fechas y horas

import requests # Importa la librería requests para hacer solicitudes HTTP
import argparse # Importa la librería argparse para crear un objeto ArgumentParser


# Crear el directorio de logs si no existe
log_directory = 'logs'
os.makedirs(log_directory, exist_ok=True)
# Generar un nombre de archivo único basado en la fecha y hora actuales
log_filename = os.path.join(log_directory, datetime.datetime.now().strftime("History_%Y%m%d_%H%M%S.log"))

# Configuración de los logs para guardar la información en un archivo de texto
logging.basicConfig(
    filename=log_filename,
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    encoding='utf-8'
)

logging.info("Inicio de la ejecución del programa History.py")
logging.info("Programa escrito por Williams Chan Pescador")


# Crear un objeto ArgumentParser para manejar los argumentos de la línea de comandos
parser = argparse.ArgumentParser(description="Descripción de tu programa")

# Agregar los argumentos que se pueden pasar al programa
parser.add_argument('-Voice', type=int, help='Funcionamiento de voz', required=True)
parser.add_argument('-IA', type=int, help='Funcionamiento con IA', required=True)

args = parser.parse_args() # Parsear los argumentos
ModeVoice = args.Voice # Obtener el valor del argumento Voice (Para activar o desactivar la voz del narrador)
ModeIA = args.IA # Obtener el valor del argumento IA (Para activar o desactivar la mejora de la historia con IA)

args = parser.parse_args() # Parsear los argumentos

colorama.init() # Inicializa colorama para darle color al texto

#load_dotenv() # Carga las variables de entorno del archivo .env

#api_key = os.getenv('API_KEY') # Obtiene el valor de la variable de entorno API_KEY

#print(colorama.Fore.CYAN + "API_KEY: " + api_key)

## 

# Define la clase del personaje
class Character:
    # Constructor de la clase Character que recibe un diccionario con los atributos del personaje 
    def __init__(self, DictionaryCharacter):
        self.Name = DictionaryCharacter['Name']
        self.Personality = DictionaryCharacter['Personality']
        self.Location = DictionaryCharacter['Location']
        self.Gender = DictionaryCharacter['Gender']
        self.EmotionTowardsOtherCharacter = DictionaryCharacter['EmotionTowardsOtherCharacter']
        self.CharacterWhoIsTheObjectOfTheEmotion = DictionaryCharacter['CharacterWhoIsTheObjectOfTheEmotion']
        self.CaptivityStatus = DictionaryCharacter['CaptivityStatus']
        self.ReliableSourceOfInformation = DictionaryCharacter['ReliableSourceOfInformation']
        self.ObjectThatTheCharacterOwns = DictionaryCharacter['ObjectThatTheCharacterOwns']
        self.LocationThatTheCharacterLearns = DictionaryCharacter['LocationThatTheCharacterLearns']
        self.InstructionsToPerform = DictionaryCharacter['InstructionsToPerform']

    # Método para imprimir los detalles del personaje
    def print_details(self):
        print(f"Name: {self.Name}")
        print(f"Personality: {self.Personality}")
        print(f"Location: {self.Location}")
        print(f"Gender: {self.Gender}")
        print(f"Emotion Towards Other Character: {self.EmotionTowardsOtherCharacter}")
        print(f"Character Who Is The Object Of The Emotion: {self.CharacterWhoIsTheObjectOfTheEmotion}")
        print(f"Captivity Status: {self.CaptivityStatus}")
        print(f"Reliable Source Of Information: {self.ReliableSourceOfInformation}")
        print(f"Object That The Character Owns: {self.ObjectThatTheCharacterOwns}")
        print(f"Location That The Character Learns: {self.LocationThatTheCharacterLearns}")
        print(f"Instructions To Perform: {self.InstructionsToPerform}")

# Limpiar el contenido de un archivo
def clear_file(file_path):
    # Abre el archivo en modo de escritura para vaciar su contenido
    with open(file_path, 'w') as file:
        pass  # No se necesita hacer nada aquí, solo abrir el archivo en modo de escritura lo vacía

# Guardar el historial de texto en un archivo
def saveFileHistory(Text):
    with open("History.txt", "a") as file:
        file.write(f"{Text} \n")

# Imprimir un diccionario en formato JSON
def printJSON(data):
    print(json.dumps(data, indent=4, ensure_ascii=False))

# Cargar los personajes desde un archivo JSON
def loadSettigs():
    try:
        with open("Characters.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

Hero = None # Variable global para el héroe
Hostage = None # Variable global para el rehén
Kidnapping = None # Variable global para el secuestrador
Informant = None # Variable global para el informante
Guardian = None # Variable global para el guardián

statusGoalHeroDecideRescueHostage = False # Variable global para la meta conductora
statusGoalKidnappingHostage = False # Variable global para la meta secundaria
statusGoalHeroRewardsInformant = False # Variable global para la meta secundaria
statusGoalHeroFindsInformant = False # Variable global para la meta secundaria
statusGoalHeroLiberatesHostage = False # Variable global para la meta secundaria



Characters = loadSettigs() # Carga los personajes desde el archivo JSON
logging.info("Personajes instanciados correctamente")
clear_file("History.txt") # Limpia el contenido del archivo History.txt

# Función imprimir los detalles de los personajes 
def printCharacters():
    for Character_ in Characters:
        Character(Character_).print_details()

# Función para obtener los detalles de los personajes en lugar de imprimirlos
def getCharactersDetails():
    details = []
    for Character_ in Characters:
        char = Character(Character_)
        details.append(f"\nName: {char.Name}\n"
                       f"Personality: {char.Personality}\n"
                       f"Location: {char.Location}\n"
                       f"Gender: {char.Gender}\n"
                       f"Emotion Towards Other Character: {char.EmotionTowardsOtherCharacter}\n"
                       f"Character Who Is The Object Of The Emotion: {char.CharacterWhoIsTheObjectOfTheEmotion}\n"
                       f"Captivity Status: {char.CaptivityStatus}\n"
                       f"Reliable Source Of Information: {char.ReliableSourceOfInformation}\n"
                       f"Object That The Character Owns: {char.ObjectThatTheCharacterOwns}\n"
                       f"Location That The Character Learns: {char.LocationThatTheCharacterLearns}\n"
                       f"Instructions To Perform: {char.InstructionsToPerform}\n")
    return "\n".join(details)

#print(colorama.Fore.CYAN + "Personajes: ")
#printCharacters() # Imprime los detalles de los personajes
logging.info("Personajes: ")
logging.info(getCharactersDetails())



# Función para realizar la acción de la historia "Loves"
def storyActionLoves(CharacterThatLoves: Character, CharacterThatIsLoved: Character):
    # Plantilla de la acción "Loves"
    def Template():
        DictTemplate = {
            "Start": "The ",
            "End": ["loved the ", "had a strong affection for the "]
        }

        # Construir el texto NOTE: Elige una plantilla aleatoria
        Text = f"{DictTemplate['Start']}{CharacterThatLoves.Name} {random.choice(DictTemplate['End'])}{CharacterThatIsLoved.Name}."
        saveFileHistory(Text) # Guarda el texto en el archivo History.txt
        logging.info("Texto de la historia: " + Text)

    # Precondiciones de la acción "Loves"
    def Preconditions():
        logging.info("Sin precondiciones de la acción Loves")
        pass

    # Postcondiciones de la acción "Loves"
    def Postconditions():
        logging.info("Validar postcondiciones de la acción Loves")
        logging.info("Personaje que ama: " + CharacterThatLoves.Name)
        logging.info("Personaje que es amado: " + CharacterThatIsLoved.Name)
        CharacterThatLoves.EmotionTowardsOtherCharacter = "Love"
        CharacterThatIsLoved.CharacterWhoIsTheObjectOfTheEmotion = "Loved"
        logging.info("Emoción del personaje que ama: " + CharacterThatLoves.EmotionTowardsOtherCharacter)
        logging.info("Personaje que es amado: " + CharacterThatIsLoved.CharacterWhoIsTheObjectOfTheEmotion)

    Preconditions() # Llama a las precondiciones de la acción "Loves"
    Template() # Llama a la plantilla de la acción "Loves"
    Postconditions() # Llama a las postcondiciones de la acción "Loves"
    logging.info("Postcondiciones validadas de la acción Loves")

    #CharacterThatLoves.print_details()
    #CharacterThatIsLoved.print_details()

# Función para definir un personaje según un atributo y un valor
def defineCharacter(Characters, Attribute, Value):
    SelectedCharacter = list(filter(lambda Character_: Character_[Attribute] == Value, Characters))
    return random.choice(SelectedCharacter) if SelectedCharacter else None

# Función para validar si dos personajes están en la misma ubicación o no
def locationValidation(Location1, Location2):
    if Location1 == Location2:
        return True
    return False

# Función para realizar la acción de la historia "MakesPrisioner"
def storyMakesPrisioner (Hostage: Character, Kidnapping: Character):
    def Template():
        Text = f"One morning, {Kidnapping.Name} went to the {Hostage.Location} and abducted the {Hostage.Name}."
        saveFileHistory(Text) # Guarda el texto en el archivo History.txt
        logging.info("Texto de la historia: " + Text)

    def Preconditions():
        logging.info("Validar precondiciones de la acción Hace prisionero")
        # Validar si los personajes están en la misma ubicación o no
        if not locationValidation(Hostage.Location, Kidnapping.Location):
            #print(colorama.Fore.RED + "- Precondiciones, los personajes no están en el mismo lugar")
            logging.info("Precondiciones validadas, los personajes no están en el mismo lugar")
            return

    def Postconditions():
        logging.info("Postcondiciones de la acción Hace prisionero")
        Kidnapping.Location = Hostage.Location
        Hostage.CaptivityStatus = "imprisoned"
        logging.info("Ubicación del secuestrador: " + Kidnapping.Location)
        logging.info("Estado de cautiverio del rehén: " + Hostage.CaptivityStatus)
        Template()

    Preconditions()
    logging.info("Precondiciones validadas de la acción Hace prisionero")
    Postconditions()
    

    
# Función para realizar la acción de la historia "TakesCursedCave"
def storyActionTakesCursedCave(Kidnapping: Character, Hostage: Character):
    def Template():
        Text = f"The {Kidnapping.Name} took the {Hostage.Name} to the Cursed Cave."
        saveFileHistory(Text)
        logging.info("Texto de la historia: " + Text)

    def Preconditions():
        logging.info("Sin precondiciones de la acción Lleva la cueva maldita")
        pass

    def Postconditions():
        logging.info("Validar postcondiciones de la acción Lleva la cueva maldita")
        Kidnapping.Location = "Cursed Cave"
        Hostage.Location = "Cursed Cave"
        logging.info("Ubicación del secuestrador: " + Kidnapping.Location)
        logging.info("Ubicación del rehén: " + Hostage.Location)


    Preconditions()
    Postconditions()
    Template()

# Función para realizar la meta de la historia "KidnappingHostage"
def goalKidnappingHostage(Hostage , Characters):
    def Preconditions():
        # SYS:

        # Instanciar secuestrador - Character-Kidnappins

        global Kidnapping

        if Kidnapping != None:
            #print(colorama.Fore.GREEN + "- Precondiciones validadas, el secuestrador existe")
            logging.info("Precondiciones validadas, el secuestrador existe")
            return
        
        #print(colorama.Fore.RED + "- Precondiciones no validadas, el secuestrador no existe")

        global Guardian
        logging.info("\t Precondición Instanciar personajes - Character-Guardian")
        Guardian = defineCharacter(Characters, "Location", "sacred lake")
        Guardian = Character(Guardian)
        logging.info("\tGuardian definido: " + Guardian.Name)

        #print(colorama.Fore.RED + "- Guardian definido: " + Guardian.Name)
        
        # Remover el guardián de los personajes
        Characters.remove(Guardian.__dict__)


        Kidnapping = defineCharacter(Characters, "Personality", "horrendous")
        Kidnapping = Character(Kidnapping)
        logging.info("\t Precondición Instanciar personajes - Character-Kidnapping")
        logging.info("\tSecuestrador definido: " + Kidnapping.Name)

        #print(colorama.Fore.GREEN + "- - - Secuestrador definido: " + Kidnapping.Name)

        logging.info("Precondiciones validadas, el secuestrador existe y el guardián también")

    def Plan():
        global statusGoalKidnappingHostage
        logging.info("Planificación de la meta de la historia: Secuestrar al rehén")
        # ACT:
        #print(colorama.Fore.YELLOW + "- Planificar secuestro")
        logging.info("\t Acción del plan: Hacer prisionero")
        storyMakesPrisioner(Hostage, Kidnapping)
        # ACT:
        logging.info("\t Acción del plan: Lleva la cueva maldita")
        storyActionTakesCursedCave(Kidnapping, Hostage)
        statusGoalKidnappingHostage = True



    Preconditions()
    Plan()
    logging.info("Meta de la historia completada: Secuestrar al rehén")

# Función para realizar la acción de la historia "MovesToTheSameLocation"
def storyActionMovesToTheSameLocation(CharacterThatMoves: Character, CharacterStatic: Character):
    def Template():
        Text = f"The {CharacterThatMoves.Name} went to talk to the {CharacterStatic.Name} to ask for help."
        saveFileHistory(Text)
        logging.info("Texto de la historia: " + Text)

    def Preconditions():
        logging.info("Sin precondiciones de la acción Moverse a la misma ubicación")
        pass

    def Postconditions():
        logging.info("Postcondiciones de la acción Moverse a la misma ubicación")
        CharacterThatMoves.Location = CharacterStatic.Location
        logging.info("Ubicación del personaje que se mueve: " + CharacterThatMoves.Location)


    Preconditions()
    Postconditions()
    Template()

# NOTA SI EL PERSONAJE SECUESTRADOR ES EL GUARDIAN DEL LAGO EN LOS TEMPLATES DE IR CON EL INFORMANTE PARA CONSEGUIR LO QUE PIDE
# EL QUE CUBRE LO DESEADO ES EL GUARDIAN DEL LAGO POR DEFAULT.

# Función para realizar la acción de la historia "AskForMagicGrass"
def storyActionAskForMagicGrass(Hero: Character, Informant: Character):
    def Template():
        Text = f"The {Informant.Name} agreed to provide the information in exchange for a cluster of magic grass than only grows in the sacred lake.\nThe {Hero.Name} went in search of the plant but the guardian of the lake barred { "Her" if Hero.Gender == "female" else "Him" } from entering.\nThe {Hero.Name} sang an ancestral song of supplication and the guardian of the lake allowed { "Her" if Hero.Gender == "female" else "Him" } to enter.\nThe {Hero.Name} took a bunch of magic grass.\nThe {Hero.Name} returned with the {Informant.Name}."
        saveFileHistory(Text)
        logging.info("Texto de la historia: " + Text)

    def Preconditions():
        if Informant.ObjectThatTheCharacterOwns != "magic grass":
            #print(colorama.Fore.RED + "- Precondiciones no validadas, el informante no tiene la hierba mágica")
            logging.info("Precondiciones, el informante no tiene la hierba mágica")
            return
    
    def Postconditions():
        logging.info("Postcondiciones de la acción Pide hierba mágica")
        Hero.ObjectThatTheCharacterOwns = "magic grass"
        logging.info("Objeto que posee el héroe: " + Hero.ObjectThatTheCharacterOwns)

    Preconditions()
    logging.info("Precondiciones validadas de la acción Pide hierba mágica")
    Postconditions()
    Template()

# Función para realizar la acción de la historia "AskForForetellingBones"
def storyActionAskForForetellingBones(Hero: Character, Informant: Character):
    def Template():
        Text = f"The {Informant.Name} agreed to provide the information in exchange for a cluster of foretelling bones.\nThe {Hero.Name} went in search of the bones but the guardian of the forest barred { "Her" if Hero.Gender == "female " else "Him" } from entering.\nThe {Hero.Name} sang an ancestral song of supplication and the guardian of the forest allowed {"Her" if Hero.Gender == "female " else "Him" } to enter.\nThe {Hero.Name} took a bunch of foretelling bones.\nThe {Hero.Name} returned with the {Informant.Name}."
        saveFileHistory(Text)
        logging.info("Texto de la historia: " + Text)

    def Preconditions():
        if Informant.ObjectThatTheCharacterOwns != "foretelling bones":
            #print(colorama.Fore.RED + "- Precondiciones no validadas, el informante no tiene la hierba mágica")
            logging.info("Precondiciones, el informante no tiene la hierba mágica")
            return

    def Postconditions():
        logging.info("Postcondiciones de la acción Pide huesos de adivinación")
        Hero.ObjectThatTheCharacterOwns = "foretelling bones"
        logging.info("Objeto que posee el héroe: " + Hero.ObjectThatTheCharacterOwns)

    Preconditions()
    logging.info("Precondiciones validadas de la acción Pide huesos de adivinación")
    Postconditions()
    Template()

def storyActionAskForVeneratedBook(Hero: Character, Informant: Character):
    def Template():
        Text = f"The {Informant.Name} agreed to provide the information in exchange for a venerated book.\nThe {Hero.Name} went in search of the book but the guardian of the temple barred { "Her" if Hero.Gender == "female" else "Him" } from entering.\nThe {Hero.Name} sang an ancestral song of supplication and the guardian of the temple allowed {"Her" if Hero.Gender == "female" else "Him" } to enter.\nThe {Hero.Name} took the venerated book.\nThe {Hero.Name} returned with the {Informant.Name}."
        saveFileHistory(Text)
        logging.info("Texto de la historia: " + Text)

    def Preconditions():
        if Informant.ObjectThatTheCharacterOwns != "venerated book":
            #print(colorama.Fore.RED + "- Precondiciones no validadas, el informante no tiene el libro venerado")
            logging.info("Precondiciones, el informante no tiene el libro venerado")
            return
        
    def Postconditions():
        logging.info("Postcondiciones de la acción Pide libro venerado")
        Hero.ObjectThatTheCharacterOwns = "venerated book"
        logging.info("Objeto que posee el héroe: " + Hero.ObjectThatTheCharacterOwns)

    Preconditions()
    logging.info("Precondiciones validadas de la acción Pide libro venerado")
    Postconditions()
    Template()

def storyActionAskForMagicSword(Hero: Character, Informant: Character):
    def Template():
        Text = f"The {Informant.Name} agreed to provide the information in exchange for a magic sword.\nThe {Hero.Name} went in search of the sword but the guardian of the mountain barred { "Her" if Hero.Gender == "female" else "Him" } from entering.\nThe {Hero.Name} sang an ancestral song of supplication and the guardian of the mountain allowed {"Her" if Hero.Gender == "female" else "Him" } to enter.\nThe {Hero.Name} took the magic sword.\nThe {Hero.Name} returned with the {Informant.Name}."
        saveFileHistory(Text)
        logging.info("Texto de la historia: " + Text)

    def Preconditions():
        if Informant.ObjectThatTheCharacterOwns != "magic sword":
            #print(colorama.Fore.RED + "- Precondiciones no validadas, el informante no tiene la espada mágica")
            logging.info("Precondiciones, el informante no tiene la espada mágica")
            return
        
    def Postconditions():
        logging.info("Postcondiciones de la acción Pide espada mágica")
        Hero.ObjectThatTheCharacterOwns = "magic sword"
        logging.info("Objeto que posee el héroe: " + Hero.ObjectThatTheCharacterOwns)

    Preconditions()
    logging.info("Precondiciones validadas de la acción Pide espada mágica")
    Postconditions()
    Template()

# Función para realizar la acción de la historia "GivesReward"
def storyActionGivesReward(Hero: Character, Informant: Character):
    def Template():
        Text = f"The {Hero.Name} handed to the {Informant.Name} the {Hero.ObjectThatTheCharacterOwns}."
        saveFileHistory(Text)
        logging.info("Texto de la historia: " + Text)


    def Preconditions():
        logging.info("Sin precondiciones de la acción Da recompensa")
        pass
        
    def Postconditions():
        logging.info("Postcondiciones de la acción Da recompensa")
        Informant.ObjectThatTheCharacterOwns = Hero.ObjectThatTheCharacterOwns
        Hero.ObjectThatTheCharacterOwns = "none"
        logging.info("Objeto que posee el informante: " + Informant.ObjectThatTheCharacterOwns)
        logging.info("Objeto que posee el héroe: " + Hero.ObjectThatTheCharacterOwns)

    Preconditions()
    Template()
    Postconditions()

    
# Función para realizar la meta de la historia "HeroRewardsInformant"
def goalHeroRewardsInformant(Hero: Character, Informant: Character):
    #global Hero
    #global Informant
    def Preconditions():
        logging.info("Validar precondiciones de la meta de la historia: Heroe recompensa al informante")
        # SYS:

        if Informant.Name == "sorcerer":
            logging.info("Precondiciones validadas, el informante es el hechicero")
            #print(colorama.Fore.GREEN + "- Precondiciones validadas, el informante es el hechicero")
            storyActionAskForMagicGrass(Hero, Informant)
            return
        elif Informant.Name == "soothsayer":
            logging.info("Precondiciones validadas, el informante es el adivino")
            #print(colorama.Fore.GREEN + "- Precondiciones validadas, el informante es el adivino")
            storyActionAskForForetellingBones(Hero, Informant)
            return
        elif Informant.Name == "priest": # NOTA EL PERSONAJE SACERDOTE NUNCA CUMPLE CON LAS CONDICIONES
            logging.info("Precondiciones validadas, el informante es el sacerdote")
            #print(colorama.Fore.GREEN + "- Precondiciones validadas, el informante es el sacerdote")
            storyActionAskForVeneratedBook(Hero, Informant)
            return
        elif Informant.Name == "old mysterious lady":
            logging.info("Precondiciones validadas, el informante es la vieja misteriosa")
            print(colorama.Fore.GREEN + "- Precondiciones validadas, el informante no es el hechicero, adivino o sacerdote")
            storyActionAskForMagicSword(Hero, Informant)
            return
        
        
    def Plan():
        #global Hero
        #global Informant

        logging.info("Planificación de la meta de la historia: Heroe recompensa al informante")
        global statusGoalHeroRewardsInformant

        storyActionGivesReward(Hero, Informant)
        statusGoalHeroRewardsInformant = True

    
    Preconditions()
    Plan()
    logging.info("Meta de la historia completada: Heroe recompensa al informante")

# Función para realizar la acción de la historia "GetsTheLocationOfTheHostageFrom"
def storyActionGetsTheLocationOfTheHostageFrom(Hero: Character, Informant: Character, Hostage: Character):
    def Template():
        Text = f"The {Informant.Name} revealed to the {Hero.Name} the {Hostage.Name}'s location."
        saveFileHistory(Text)
        logging.info("Texto de la historia: " + Text)

    def Preconditions():
        logging.info("Sin precondiciones de la acción Obtiene la ubicación del rehén")
        pass

    def Postconditions():
        logging.info("Postcondiciones de la acción Obtiene la ubicación del rehén")
        Hero.LocationThatTheCharacterLearns = Hostage.Location
        logging.info("Ubicación que el personaje aprende: " + Hero.LocationThatTheCharacterLearns)

    Preconditions()
    Template()
    Postconditions()
    
# Función para realizar la acción de la historia "GetsInstructionsToRescueHostageFrom"
def storyActionGetsInstructionsToRescueHostageFrom (Hero: Character, Informant: Character, Hostage: Character, Kidnapping: Character):
    def Template():
        Text = f"The {Informant.Name} gave to the {Hero.Name} a spell to put the {Kidnapping.Name} to sleep."
        saveFileHistory(Text)
        logging.info("Texto de la historia: " + Text)

    def Preconditions():
        logging.info("Validar precondiciones de la acción Obtiene instrucciones para rescatar al rehén")
        if Hostage.CaptivityStatus == "imprisoned":
            #print(colorama.Fore.GREEN + "- Precondiciones validadas, el rehén está prisionero")
            logging.info("Precondiciones validadas, el rehén está prisionero")
            return
        
    def Postconditions():
        logging.info("Postcondiciones de la acción Obtiene instrucciones para rescatar al rehén")
        Hero.InstructionsToPerform = "performs the rescue plan The spell"
    
    Preconditions()
    Template()
    
    Postconditions()

# Función para realizar la meta de la historia "HeroFindsInformant"
def goalHeroFindsInformant ():
    global Hero

    def Preconditions():
        # SYS: * 
        global Informant
        global Hostage

        logging.info("Validar precondiciones de la meta de la historia: Heroe encuentra al informante")

        if Informant != None:
            #print(colorama.Fore.GREEN + "- Precondiciones validadas, el informante existe")
            logging.info("Precondiciones validadas, el informante existe")
            return

        #print(colorama.Fore.RED + "- Precondiciones no validadas, el informante no existe")
        

        Informant = defineCharacter(Characters, "ReliableSourceOfInformation", "yes")

        Informant = Character(Informant)
        logging.info("Informante definido: " + Informant.Name)

        # NOTA EL INFORMANTE NO PUEDE SER EL REHEN (LA VIEJA MISTERIOSA PUEDE APAECER COMO INFORMANTE Y REHEN)
        """if Informant.Name == Hostage.Name:
            print(colorama.Fore.RED + "- - - El informante no puede ser el rehén")
            Informant = defineCharacter(Characters, "ReliableSourceOfInformation", "yes")

            Informant = Character(Informant)"""
    

        #print(colorama.Fore.GREEN + "- - - Informante definido: " + Informant.Name)

        # Eliminar al informante de los personajes
        Characters.remove(Informant.__dict__)

        # ACT:
        logging.info("Precondión de la acción: Moverse a la misma ubicación")
        storyActionMovesToTheSameLocation(Hero, Informant)

        # NOTA: SE AGREGO FIENDLY PARA QUE EL SACERDOTE TAMBIEN LANZE LA ACCION DE DAR RECOMPENSA
        if Informant.Personality == "mean" or Informant.Personality == "horrendous" or Informant.Personality == "friendly":
            # GOAL:
            #print(colorama.Fore.YELLOW + "- ")
            #Informant.print_details()
            logging.info("Meta: Recompensar al informante, la meta actual se pone en pausa")
            goalHeroRewardsInformant(Hero, Informant)

    def Plan():

        global Hero
        global Informant
        global Hostage
        global Kidnapping
        global statusGoalHeroFindsInformant
        logging.info("Planificación de la meta de la historia: Heroe encuentra al informante")
        # ACT:
        storyActionGetsTheLocationOfTheHostageFrom(Hero, Informant, Hostage)
        # ACT:
        logging.info("Acción del plan: Obtiene instrucciones para rescatar al rehén")
        storyActionGetsInstructionsToRescueHostageFrom(Hero, Informant, Hostage, Kidnapping)

        statusGoalHeroFindsInformant = True



    Preconditions()
    Plan()	
    logging.info("Meta de la historia completada: Heroe encuentra al informante")

# Función para realizar la acción de la historia "MovesTheLocationThatTheCharacterLearns"
def storyActionMovesTheLocationThatTheCharacterLearns(CharacterThatChangesPostion: Character):
    def Template():
        Text = f"Wasting no time, the {CharacterThatChangesPostion.Name} went to the {CharacterThatChangesPostion.LocationThatTheCharacterLearns}."
        saveFileHistory(Text)
        logging.info("Texto de la historia: " + Text)

    def Preconditions():
        logging.info("Sin precondiciones de la acción Mueve la ubicación que el personaje aprende")
        pass

    def Postconditions():
        logging.info("Postcondiciones de la acción Mueve la ubicación que el personaje aprende")
        CharacterThatChangesPostion.Location = CharacterThatChangesPostion.LocationThatTheCharacterLearns
        logging.info("Ubicación del personaje: " + CharacterThatChangesPostion.Location)


    Preconditions()
    Template()
    Postconditions()

# Función para realizar la acción de la historia "PerformsTheRescuePlanTheSpell"
def storyActionPerformsTheRescuePlanTheSpell():
    global Hero
    global Kidnapping
    global Hostage

    def Template():
        global Hero
        global Kidnapping
        global Hostage

        Text = f"The {Hero.Name} invoked the spell and the {Kidnapping.Name} fell into a deep sleep.\n The {Hero.Name} released the {Hostage.Name}."
        saveFileHistory(Text)

    def Preconditions():
        logging.info("Validar precondiciones de la acción Realiza el plan de rescate El hechizo")
        global Hostage
        if Hostage.CaptivityStatus == "imprisoned" : 
            #print(colorama.Fore.GREEN + "- Precondiciones validadas, el rehén está prisionero")
            logging.info("Precondiciones validadas, el rehén está prisionero")
            return

    def Postconditions():
        logging.info("Postcondiciones de la acción Realiza el plan de rescate El hechizo")
        global Hostage
        Hostage.CaptivityStatus = "free"
        logging.info("Estado de cautiverio del rehén: " + Hostage.CaptivityStatus)

    Preconditions()
    
    Postconditions()
    Template()
    
# Función para realizar la acción de la historia "ExecuteInstructionsToPerform"
def storyActionExecuteInstructionsToPerform(CharacterExecuter: Character):
    def Preconditions():
        logging.info("Sin precondiciones de la acción Ejecuta instrucciones para realizar")
        pass

    def Postconditions():
        logging.info("Postcondiciones de la acción Ejecuta instrucciones para realizar")
        #print ("Intructions: " + CharacterExecuter.InstructionsToPerform)
        storyActionPerformsTheRescuePlanTheSpell()

    Preconditions()
    Postconditions()
    
# Función para realizar la meta de la historia "HeroLiberatesHostage"
def goalHeroLiberatesHostage ():
    global Hero
    global Hostage
    global Kidnapping

    def Preconditions():
        # GOAL:
        # The hero finds an informant that provides the location of the Hostage and the instructions to rescue him.
        logging.info("Validar precondiciones de la meta de la historia: Heroe libera al rehen")
        logging.info("Meta: El heroe encuentra un informante que proporciona la ubicación del rehen y las instrucciones para rescatarlo")
        logging.info("La meta: Heroe libera al rehen se pone en pausa hasta que se cumpla la meta: El heroe encuentra un informante que proporciona la ubicación del rehen y las instrucciones para rescatarlo")
        goalHeroFindsInformant()
        pass

    def Plan():

        global Hero
        global statusGoalHeroLiberatesHostage

        # ACT:
        logging.info("Planificación de la meta de la historia: Heroe libera al rehen")
        storyActionMovesTheLocationThatTheCharacterLearns(Hero)

        # ACT:
        logging.info("Acción del plan: Ejecuta instrucciones para realizar")
        storyActionExecuteInstructionsToPerform(Hero)

        statusGoalHeroLiberatesHostage = True



    Preconditions()
    Plan()
    logging.info("Meta de la historia completada: Heroe libera al rehen")

# Función para realizar la meta conductora de la historia "HeroDecideRescueHostage"
def goalHeroDecideRescueHostage(Characters):

    logging.info("Meta conductora de la historia: Heroe decide rescatar al rehen")

    def InitTextHistory():
        global Hero
        global Hostage
        Selection = random.choice(["LocationHero", "PersonalityHero"])

        if Selection == "LocationHero":
            TextLocationHero = f"The {Hero.Name} was at the {Hero.Location}"
            saveFileHistory(TextLocationHero)
            logging.info("Texto de la historia: " + TextLocationHero)
            TextPersonalityHostage = f"and The {Hostage.Name} was a {Hostage.Personality} person."
            saveFileHistory(TextPersonalityHostage)
            logging.info("Texto de la historia: " + TextPersonalityHostage)
        elif Selection == "PersonalityHero":
            TextPersonalityHero = f"The {Hero.Name} was a {Hero.Personality} person"
            saveFileHistory(TextPersonalityHero)
            logging.info("Texto de la historia: " + TextPersonalityHero)
            TextLocationHostage = f"and The {Hostage.Name} was at the {Hostage.Location}."
            saveFileHistory(TextLocationHostage)
            logging.info("Texto de la historia: " + TextLocationHostage)

    def Preconditions():
        # SYS:
        global Hero
        global Hostage

        logging.info("Validar precondiciones: ")
        logging.info(f"\t Precondición Instanciar personajes - Character-Hero y Character-Hostage")
        #print(colorama.Fore.YELLOW +  "- Validar precondiciones ")

        if Hero != None and Hostage != None:
            #print(colorama.Fore.GREEN + "Precondiciones validadas, los personajes existen")
            logging.info("Precondiciones validadas, los personajes existen")
            return
        
        #print (colorama.Fore.RED + "- - Precondiciones no validadas, los personajes no existen")
        # *Character-Hero is 
        Hero = defineCharacter(Characters,"Personality", "brave")
        Hero = Character(Hero)
        #print (colorama.Fore.GREEN + "- - - Heroe definido: " + Hero.Name)

        # *Character-Hostage is
        Hostage = defineCharacter(Characters,"Personality", "friendly")
        Hostage = Character(Hostage)
        #print (colorama.Fore.GREEN + "- - - Rehen definido: " + Hostage.Name)

        logging.info("Personajes instanciados correctamente")
        logging.info("Heroe: " + Hero.Name)
        logging.info("Rehen: " + Hostage.Name)

        # Eliminar al rehén de los personajes
        Characters.remove(Hostage.__dict__)

        logging.info("Se incializa el texto de la historia")


        InitTextHistory()

        # ACT Character hero loves Character hostage:
        logging.info(f"\tPrecondición: Acción de la historia: Loves")
        storyActionLoves(Hero, Hostage)

        # GOAL KidnappingHostage:
        logging.info(f"\tPrecondición: Meta: Secuestrar al Rehén, la meta conductora se pone en pausa")
        goalKidnappingHostage(Hostage, Characters)

    def Plan():
        # Plan:
        # GOAL: The Hero liberates the Hostage
        logging.info("Planificación de la meta de la historia: El heroe decide rescatar al rehen")
        global statusGoalHeroDecideRescueHostage
        global statusGoalKidnappingHostage
        
        if statusGoalKidnappingHostage == True:
            #print(colorama.Fore.YELLOW + "- Planificar rescate")

            goalHeroLiberatesHostage()
            statusGoalHeroDecideRescueHostage = True
            logging.info("Meta de la historia completada: El heroe decide rescatar al rehen")

        pass

    #print (colorama.Fore.RED + "* Instanciar meta principal")
    Preconditions()
    logging.info("Precondiciones validadas de la meta conductora El heroe decide rescatar al rehen")
    Plan()
    logging.info("Meta conductora de la historia completada: El heroe decide rescatar al rehen")
    

# Llama a la función para realizar la meta conductora de la historia "HeroDecideRescueHostage"
goalHeroDecideRescueHostage(Characters)

# Función para leer el contenido de un archivo de texto 
def read_file(file_path):
    # Abre el archivo en modo de lectura
    with open(file_path, 'r') as file:
        # Lee todo el contenido del archivo
        content = file.read()
    return content

file_content = read_file("History.txt") # Lee el contenido del archivo History.txt
#print(colorama.Fore.MAGENTA + "\n Historia en Ingles: ")
#print(file_content ) # Imprime el contenido del archivo History.txt
logging.info("Texto de la historia en Ingles " + file_content)

Text_Translate = translate_text(file_content) # Traduce el contenido del archivo History.txt al español
#print(colorama.Fore.GREEN + "\n Historia en Español:")
#print(Text_Translate) # Imprime la traducción de la historia
logging.info("Texto de la historia en Español " + Text_Translate)

# Función para convertir texto a voz con el motor de texto a voz pyttsx3
def VoiceText(Text):
    # Inicializar el motor de texto a voz
    engine = pyttsx3.init()

    # Configurar la velocidad de habla
    engine.setProperty('rate', 150)  # 150 palabras por minuto

    # Configurar el volumen de la voz
    engine.setProperty('volume', 1.0)  # Máximo volumen

    # Configurar la voz (0 es masculina, 1 es femenina)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Cambia a voices[1].id para voz femenina

    # Convertir el texto a voz
    engine.say(Text)

    engine.runAndWait()

# Función para mejorar la historia con IA usando la API de Llama3
def UpgradeIA(Text):

        # URL del servidor de LM Studio
    url = "http://localhost:1234/v1/chat/completions"

    # Encabezados de la solicitud
    headers = {
        "Content-Type": "application/json"
    }

    Text_History = "Mejora el siguiente texto manteniendo la historia intacta, pero optimizando la fluidez para evitar la repetición innecesaria de personajes. Reemplaza o reformula oraciones para que los personajes no se mencionen tantas veces seguidas, sin agregar nuevos elementos ni alterar el contenido original es decir no alterar la historia, tampoco pierdas el contexto y su idea IMPORTANTE: SOLO DAME LA NUEVA HISTORIA, NO AGREGUES NADA MÁS: " + Text 

    # Cuerpo de la solicitud
    data = {
        "model": "lmstudio-community/gemma-2-2b-it-GGUF/gemma-2-2b-it-Q4_K_M.gguf",
        "messages": [
            {"role": "system", "content": "Eres un mejorador de historias."},
            {"role": "user", "content": Text_History},
        ],
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }

    # Realizar la solicitud POST
    response = requests.post(url, headers=headers, json=data)

    # Mostrar el resultado
    if response.status_code == 200:
        completion = response.json()
        return completion['choices'][0]['message']['content']
    else:
        print(f"Error: {response.status_code}")
        return "Error"


##print(response.json())


NewHistory = Text_Translate # Guarda la historia traducida al español en una nueva variable NewHistory


#print(statusGoalHeroDecideRescueHostage) # Imprime el estado de la meta conductora

# Imprime los modos de funcionamiento de la IA y la voz del narrador
if ModeIA == 1: # Si el modo de IA está activado
    
    logging.info("Modo de IA encendida")
    NewHistory = UpgradeIA(NewHistory)
    #print(colorama.Fore.CYAN + "\n Historia Mejorada: ")
    #print(colorama.Fore.CYAN + "\n Historia Mejorada: " + NewHistory) # Imprime la historia mejorada
    #print(NewHistory)
    logging.info("Texto de la historia mejorada " + NewHistory)

else:
    #print("\nModo de IA apagada")
    logging.info("Modo de IA apagada")
    #print("\nTexto de la historia: ")
    #print(NewHistory)
    #logging.info("Texto de la historia " + NewHistory)

if ModeVoice == 1: # Si el modo de voz está activado
    logging.info("Modo de voz encendida")
    #print("\nModo de voz encendida")
    #VoiceText(NewHistory)
    #print(colorama.Fore.CYAN + "\nTexto de la historia: ")
    print(NewHistory)
    logging.info("Texto de la historia " + NewHistory)

else:
    #print("\nModo de voz apagada")
    logging.info("Modo de voz apagada")
    #print("\nTexto de la historia: ")
    print(NewHistory)



