# Importación de librerías
import json
import random
from Traslate import translate_text # Importa la función translate_text del archivo Translate.py
import colorama
import pyttsx3
from dotenv import load_dotenv
import os

import requests
import argparse


# Crear un objeto ArgumentParser
parser = argparse.ArgumentParser(description="Descripción de tu programa")

parser.add_argument('-Voice', type=int, help='Funcionamiento de voz', required=True)
parser.add_argument('-IA', type=int, help='Funcionamiento con IA', required=True)

args = parser.parse_args()
ModeVoice = args.Voice
ModeIA = args.IA


 # Parsear los argumentos
args = parser.parse_args()



colorama.init()

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

api_key = os.getenv('API_KEY')

print(colorama.Fore.CYAN + "API_KEY: " + api_key)

## 

# Define la clase Character
class Character:
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

statusGoalHeroDecideRescueHostage = False # Variable global para la meta principal
statusGoalKidnappingHostage = False # Variable global para la meta secundaria
statusGoalHeroRewardsInformant = False # Variable global para la meta secundaria
statusGoalHeroFindsInformant = False # Variable global para la meta secundaria
statusGoalHeroLiberatesHostage = False # Variable global para la meta secundaria

Characters = loadSettigs() # Carga los personajes desde el archivo JSON
clear_file("History.txt") # Limpia el contenido del archivo History.txt
# printJSON(Settings)

def storyActionLoves(CharacterThatLoves: Character, CharacterThatIsLoved: Character):
    def Template():
        DictTemplate = {
            "Start": "The ",
            "End": ["loved the ", "had a strong affection for the "]
        }

        # Construir el texto NOTE: Elige una plantilla aleatoria
        Text = f"{DictTemplate['Start']}{CharacterThatLoves.Name} {random.choice(DictTemplate['End'])}{CharacterThatIsLoved.Name}."
        saveFileHistory(Text)

    def Preconditions():
        pass

    def Postconditions():
        CharacterThatLoves.EmotionTowardsOtherCharacter = "Love"
        CharacterThatIsLoved.CharacterWhoIsTheObjectOfTheEmotion = "Love"

    Template()
    Preconditions()
    Postconditions()

    #CharacterThatLoves.print_details()
    #CharacterThatIsLoved.print_details()


def defineCharacter(Characters, Attribute, Value):
    SelectedCharacter = list(filter(lambda Character_: Character_[Attribute] == Value, Characters))
    return random.choice(SelectedCharacter) if SelectedCharacter else None

def locationValidation(Location1, Location2):
    if Location1 == Location2:
        return True
    return False

def storyMakesPrisioner (Hostage: Character, Kidnapping: Character):
    def Template():
        
        # Construir el texto NOTE: Elige una plantilla aleatoria

        Text = f"One morning, {Kidnapping.Name} went to the {Hostage.Location} and abducted the {Hostage.Name}."
        saveFileHistory(Text)

    def Preconditions():
        if not locationValidation(Hostage.Location, Kidnapping.Location):
            print(colorama.Fore.RED + "- Precondiciones no validadas, los personajes no están en el mismo lugar")
            return

    def Postconditions():
        Kidnapping.Location = Hostage.Location
        Hostage.CaptivityStatus = "imprisoned"
        Template()

    Preconditions()
    Postconditions()
    

    #Hostage.print_details()
    #Kidnapping.print_details()

def storyActionTakesCursedCave(Kidnapping: Character, Hostage: Character):
    def Template():
        Text = f"The {Kidnapping.Name} took the {Hostage.Name} to the Cursed Cave."
        saveFileHistory(Text)

    def Preconditions():
        pass

    def Postconditions():
        Kidnapping.Location = "Cursed Cave"
        Hostage.Location = "Cursed Cave"

    Preconditions()
    Postconditions()
    Template()

def goalKidnappingHostage(Hostage , Characters):
    def Preconditions():
        # SYS:

        # Instanciar secuestrador - Character-Kidnappins

        global Kidnapping

        if Kidnapping != None:
            print(colorama.Fore.GREEN + "- Precondiciones validadas, el secuestrador existe")
            return
        
        print(colorama.Fore.RED + "- Precondiciones no validadas, el secuestrador no existe")

        Kidnapping = defineCharacter(Characters, "Personality", "horrendous")
        Kidnapping = Character(Kidnapping)

        print(colorama.Fore.GREEN + "- - - Secuestrador definido: " + Kidnapping.Name)

    def Plan():
        global statusGoalKidnappingHostage
        # ACT:
        print(colorama.Fore.YELLOW + "- Planificar secuestro")
        storyMakesPrisioner(Hostage, Kidnapping)
        storyActionTakesCursedCave(Kidnapping, Hostage)
        statusGoalKidnappingHostage = True


    Preconditions()
    Plan()

def storyActionMovesToTheSameLocation(CharacterThatMoves: Character, CharacterStatic: Character):
    def Template():
        Text = f"The {CharacterThatMoves.Name} went to talk to the {CharacterStatic.Name} to ask for help."
        saveFileHistory(Text)

    def Preconditions():
        pass

    def Postconditions():
        CharacterThatMoves.Location = CharacterStatic.Location

    Preconditions()
    Postconditions()
    Template()

def storyActionAskForMagicGrass(Hero: Character, Informant: Character):
    def Template():
        Text = f"The {Informant.Name} agreed to provide the information in exchange for a cluster of magic grass than only grows in the sacred lake.\nThe {Hero.Name} went in search of the plant but the guardian of the lake barred { "Her" if Hero.Gender == "female" else "Him" } from entering.\nThe {Hero.Name} sang an ancestral song of supplication and the guardian of the lake allowed { "Her" if Hero.Gender == "female" else "Him" } to enter.\nThe {Hero.Name} took a bunch of magic grass.\nThe {Hero.Name} returned with the {Informant.Name}."
        saveFileHistory(Text)

    def Preconditions():
        if Informant.ObjectThatTheCharacterOwns != "magic grass":
            print(colorama.Fore.RED + "- Precondiciones no validadas, el informante no tiene la hierba mágica")
            return
    
    def Postconditions():
        Hero.ObjectThatTheCharacterOwns = "magic grass"

    Preconditions()
    Postconditions()
    Template()

def storyActionGivesReward(Hero: Character, Informant: Character):
    def Template():
        Text = f"The {Hero.Name} handed to the {Informant.Name} the {Hero.ObjectThatTheCharacterOwns}."
        saveFileHistory(Text)

    def Preconditions():
        pass
        
    def Postconditions():
        Informant.ObjectThatTheCharacterOwns = Hero.ObjectThatTheCharacterOwns
        Hero.ObjectThatTheCharacterOwns = "none"

    Preconditions()
    Template()
    Postconditions()
    

def goalHeroRewardsInformant():
    global Hero
    global Informant

    def Preconditions():
        global Informant

        if Informant.Name == "sorcerer":
            storyActionAskForMagicGrass(Hero, Informant)
            return
        elif Informant.Name == "soothsayer":
            print(colorama.Fore.GREEN + "- Precondiciones validadas, el informante es el adivino")
            return
        elif Informant.Name == "priest":
            print(colorama.Fore.GREEN + "- Precondiciones validadas, el informante es el sacerdote")
            return
        else:
            print(colorama.Fore.RED + "- Precondiciones no validadas, el informante no es el hechicero, el adivino o el sacerdote")
            return
        
    def Plan():
        global Hero
        global Informant
        global statusGoalHeroRewardsInformant

        storyActionGivesReward(Hero, Informant)
        statusGoalHeroRewardsInformant = True

    
    Preconditions()
    Plan()

def storyActionGetsTheLocationOfTheHostageFrom(Hero: Character, Informant: Character, Hostage: Character):
    def Template():
        Text = f"The {Informant.Name} revealed to the {Hero.Name} the {Hostage.Name}'s location."
        saveFileHistory(Text)

    def Preconditions():
        pass

    def Postconditions():
        Hero.LocationThatTheCharacterLearns = Hostage.Location

    Preconditions()
    Template()
    Postconditions()
    
def storyActionGetsInstructionsToRescueHostageFrom (Hero: Character, Informant: Character, Hostage: Character, Kidnapping: Character):
    def Template():
        Text = f"The {Informant.Name} gave to the {Hero.Name} a spell to put the {Kidnapping.Name} to sleep."
        saveFileHistory(Text)

    def Preconditions():
        
        if Hostage.CaptivityStatus == "imprisoned":
            print(colorama.Fore.GREEN + "- Precondiciones validadas, el rehén está prisionero")
            return
        
    def Postconditions():
        Hero.InstructionsToPerform = "performs the rescue plan The spell"
    
    Preconditions()
    Template()
    
    Postconditions()

def goalHeroFindsInformant ():
    global Hero

    def Preconditions():
        # SYS: * 
        global Informant

        if Informant != None:
            print(colorama.Fore.GREEN + "- Precondiciones validadas, el informante existe")
            return

        print(colorama.Fore.RED + "- Precondiciones no validadas, el informante no existe")

        Informant = defineCharacter(Characters, "ReliableSourceOfInformation", "yes")
        Informant = Character(Informant)

        print(colorama.Fore.GREEN + "- - - Informante definido: " + Informant.Name)

        # ACT:
        storyActionMovesToTheSameLocation(Hero, Informant)

        
        if Informant.Personality == "mean" or Informant.Personality == "horrendous":
            # GOAL:
            print(colorama.Fore.YELLOW + "- ")
            Informant.print_details()
            goalHeroRewardsInformant()

    def Plan():
        global Hero
        global Informant
        global Hostage
        global Kidnapping
        global statusGoalHeroFindsInformant
        # ACT:
        storyActionGetsTheLocationOfTheHostageFrom(Hero, Informant, Hostage)
        # ACT:
        storyActionGetsInstructionsToRescueHostageFrom(Hero, Informant, Hostage, Kidnapping)

        statusGoalHeroFindsInformant = True



    Preconditions()
    Plan()	

def storyActionMovesTheLocationThatTheCharacterLearns(CharacterThatChangesPostion: Character):
    def Template():
        Text = f"Wasting no time, the {CharacterThatChangesPostion.Name} went to the {CharacterThatChangesPostion.LocationThatTheCharacterLearns}."
        saveFileHistory(Text)

    def Preconditions():
        pass

    def Postconditions():
        CharacterThatChangesPostion.Location = CharacterThatChangesPostion.LocationThatTheCharacterLearns

    Preconditions()
    Template()
    Postconditions()

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
        global Hostage
        if Hostage.CaptivityStatus == "imprisoned" : 
            print(colorama.Fore.GREEN + "- Precondiciones validadas, el rehén está prisionero")
            return

    def Postconditions():
        global Hostage
        Hostage.CaptivityStatus = "free"

    Preconditions()
    
    Postconditions()
    Template()
    
def storyActionExecuteInstructionsToPerform(CharacterExecuter: Character):
    def Preconditions():
        pass

    def Postconditions():
        print ("Intructions: " + CharacterExecuter.InstructionsToPerform)
        storyActionPerformsTheRescuePlanTheSpell()

    Preconditions()
    Postconditions()
    
def goalHeroLiberatesHostage ():
    global Hero
    global Hostage
    global Kidnapping

    def Preconditions():
        # GOAL:
        # The hero finds an informant that provides the location of the Hostage and the instructions to rescue him.
        goalHeroFindsInformant()
        pass

    def Plan():
        global Hero
        global statusGoalHeroLiberatesHostage

        # ACT:
        storyActionMovesTheLocationThatTheCharacterLearns(Hero)

        # ACT:
        storyActionExecuteInstructionsToPerform(Hero)

        statusGoalHeroLiberatesHostage = True



    Preconditions()
    Plan()


def goalHeroDecideRescueHostage(Characters):
    def InitTextHistory():
        global Hero
        global Hostage
        Selection = random.choice(["LocationHero", "PersonalityHero"])

        if Selection == "LocationHero":
            TextLocationHero = f"The {Hero.Name} was at the {Hero.Location}"
            saveFileHistory(TextLocationHero)
            TextPersonalityHostage = f"and The {Hostage.Name} was a {Hostage.Personality} person."
            saveFileHistory(TextPersonalityHostage)
        elif Selection == "PersonalityHero":
            TextPersonalityHero = f"The {Hero.Name} was a {Hero.Personality} person"
            saveFileHistory(TextPersonalityHero)
            TextLocationHostage = f"and The {Hostage.Name} was at the {Hostage.Location}."
            saveFileHistory(TextLocationHostage)

    def Preconditions():
        # SYS:
        global Hero
        global Hostage

        print(colorama.Fore.YELLOW +  "- Validar precondiciones ")

        if Hero != None and Hostage != None:
            print(colorama.Fore.GREEN + "Precondiciones validadas, los personajes existen")
            return
        
        print (colorama.Fore.RED + "- - Precondiciones no validadas, los personajes no existen")
        # *Character-Hero is 
        Hero = defineCharacter(Characters,"Personality", "brave")
        Hero = Character(Hero)
        print (colorama.Fore.GREEN + "- - - Heroe definido: " + Hero.Name)

        # *Character-Hostage is
        Hostage = defineCharacter(Characters,"Personality", "friendly")
        Hostage = Character(Hostage)
        print (colorama.Fore.GREEN + "- - - Rehen definido: " + Hostage.Name)

        InitTextHistory()

        # ACT:
        storyActionLoves(Hero, Hostage)

        # GOAL:
        goalKidnappingHostage(Hostage, Characters)


        


    def Plan():
        # Plan:
        # GOAL: The Hero liberates the Hostage
        global statusGoalHeroDecideRescueHostage
        global statusGoalKidnappingHostage
        
        if statusGoalKidnappingHostage == True:
            print(colorama.Fore.YELLOW + "- Planificar rescate")
            goalHeroLiberatesHostage()
            statusGoalHeroDecideRescueHostage = True

        pass

    print (colorama.Fore.RED + "* Instanciar meta principal")
    Preconditions()
    Plan()


goalHeroDecideRescueHostage(Characters)

def read_file(file_path):
    # Abre el archivo en modo de lectura
    with open(file_path, 'r') as file:
        # Lee todo el contenido del archivo
        content = file.read()
    return content

# Llama a la función para leer el contenido del archivo
file_content = read_file("History.txt")
print(colorama.Fore.MAGENTA + "\n Historia en Ingles: ")
print(file_content )

Text_Translate = translate_text(file_content)
print(colorama.Fore.GREEN + "\n Historia en Español:")
print(Text_Translate)

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

def UpgradeIA(Text):

    global api_key
    print(api_key)
    url = "https://llama-3.p.rapidapi.com/llama3"
    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": "llama-3.p.rapidapi.com",
        "x-rapidapi-key": api_key
    }

    Text_History = "Mejora el siguiente texto manteniendo la historia intacta, pero optimizando la fluidez para evitar la repetición innecesaria de personajes. Reemplaza o reformula oraciones para que los personajes no se mencionen tantas veces seguidas, sin agregar nuevos elementos ni alterar el contenido original IMPORTANTE: SOLO DAME LA NUEVA HISTORIA, NO AGREGUES NADA MÁS: " + Text 
    data = {
        "prompt": Text_History,
        "system_prompt": "Eres un mejorador de historias"
    }

    response = requests.post(url, headers=headers, json=data)

    return response.json()['msg']

##print(response.json())


NewHistory = Text_Translate


#engine.runAndWait()
#goalKidnappingHostage("Hostage", Characters)

print(statusGoalHeroDecideRescueHostage)

if ModeIA == 1:
    print("Modo de IA encendida")
    NewHistory = UpgradeIA(NewHistory)
    print(colorama.Fore.CYAN + "\n Historia Mejorada: ")
    print(NewHistory)
else:
    print("Modo de IA apagada")

if ModeVoice == 1:
    print("Modo de voz encendida")
    VoiceText(NewHistory)
else:
    print("Modo de voz apagada")



