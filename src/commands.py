import csv
import math
from src.arts import Art
from src.fileSys.filesReader import *

from pathlib import Path
current_path = str(Path(__file__).parent.resolve()) + "/../"

COMMANDS = {}
COOKIE = ""
CLS = False
PATH = ""

AUDIO_PATH = ""
AUDIO_VOLUME = ""
AUDIO_LOOP = ""
AUDIO_STATE = ""
AUDIO_PLAYBACK = ""
MODE = ""


def processPrompt(prompt, kwargs=None):
    if kwargs is None:
        kwargs = {}

    output = {"resultText": "", "cookie": "", "cls": "", "path": kwargs["path"],
              "audioPath": "", "audioVolume": "", "audioLoop": "", "audioState": "", "audioPlayback": "",
              "mode": ""}

    if len(prompt.replace(" ", "")) == 0:
        return output
    prompt = prompt.lower().split()

    cmd = prompt[0]
    args = prompt[1:]

    global COOKIE, CLS, PATH, AUDIO_PATH, AUDIO_VOLUME, AUDIO_LOOP, AUDIO_STATE, AUDIO_PLAYBACK, MODE

    PATH = kwargs["path"]
    output["resultText"] = promptOutput(cmd, args, kwargs)
    output["cookie"] = COOKIE
    output["cls"] = CLS
    output["path"] = PATH
    output["audioPath"] = AUDIO_PATH
    output["audioVolume"] = AUDIO_VOLUME
    output["audioLoop"] = AUDIO_LOOP
    output["audioState"] = AUDIO_STATE
    output["audioPlayback"] = AUDIO_PLAYBACK
    output["mode"] = MODE

    COOKIE = ""
    CLS = False
    PATH = ""
    AUDIO_PATH = ""
    AUDIO_VOLUME = ""
    AUDIO_LOOP = ""
    AUDIO_STATE = ""
    MODE = ""
    AUDIO_PLAYBACK = ""

    return output


def promptOutput(cmd, args=None, kwargs=None):
    if kwargs is None:
        kwargs = {}
    if args is None:
        args = []

    if cmd == "help":
        return cmd_help(args, kwargs)
    elif cmd == "echo":
        return cmd_echo(args, kwargs)
    elif cmd == "skipintro":
        return cmd_skipintro(args, kwargs)
    elif cmd == "color":
        return cmd_color(args, kwargs)
    elif cmd == "cls":
        return cmd_cls(args, kwargs)
    elif cmd == "info":
        return cmd_info(args, kwargs)
    elif cmd == "ls":
        return cmd_ls(args, kwargs)
    elif cmd == "cd":
        return cmd_cd(args, kwargs)
    elif cmd == "cat":
        return cmd_cat(args, kwargs)
    elif cmd == "audio":
        return cmd_audio(args, kwargs)
    elif cmd == "app":
        return cmd_app(args, kwargs)

    return f"\"{cmd}\" is not recognized as an internal or external command, operable program or batch file"


def updateCommands():
    with open(current_path + "src/commandsInfo.csv") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            COMMANDS[row["COMMAND"]] = (row["SYNTAX"],
                                        row["HELP"].replace("~n", "\n").replace("~t", "\t"),
                                        row["DETAILED_HELP"].replace("~n", "\n").replace("~t", "\t"))


def cmd_help(args=None, kwargs=None):
    if kwargs is None:
        kwargs = {}
    if args is None:
        args = []
    if not args:
        text = "\nBasic help page:"
        for cmd in COMMANDS.keys():
            if cmd[0] == "$":
                continue
            text += f"\n{cmd}\t{COMMANDS[cmd][0]}\t{COMMANDS[cmd][1]}".replace("\\t", "\t").replace("\\n", "\n")
        text += "\n"
        return text
    if args[0] not in COMMANDS.keys():
        return f"This is a help message...\n\nThere is no help for you, bro\n\n" \
               f"Use \"help\" without arguments to get basic info\n"

    cmd = args[0]
    text = f"COMMAND:\n" \
           f"\t{cmd}\n\n" \
           f"SYNTAX:\n" \
           f"\t{COMMANDS[cmd][0]}\n\n" \
           f"DESCRIPTION:\n" \
           f"\t{COMMANDS[cmd][2]}\n"
    text = text.replace("\\t", "\t").replace("\\n", "\n")

    return text


def cmd_echo(args=None, kwargs=None):
    if kwargs is None:
        kwargs = {}
    if args is None:
        args = []
    if not args:
        return ""
    return " ".join(args)


def cmd_skipintro(args=None, kwargs=None):
    if kwargs is None:
        kwargs = {}
    if args is None:
        args = []
    if not args or (args[0] not in ("true", "false")):
        return f"Wrong syntax. Use \"skipintro true\" or \"skipintro false\""

    global COOKIE
    if args[0] == "true":
        COOKIE += "skipIntro=true;"
        return f"skipintro is true now\nIntro will be skipped everytime you reload page"
    COOKIE += "skipIntro=false;"
    return f"skipintro is false now\nIntro will NOT be skipped everytime you reload page"


def cmd_color(args=None, kwargs=None):
    if kwargs is None:
        kwargs = {}
    if args is None:
        args = []
    global COOKIE

    if not args:
        COOKIE += "color=0"
        return f""

    if str(args[0]).isdigit():
        if int(args[0]) < 0:
            return f""
        COOKIE += f"color={args[0]};"
        return f""
    return f"Invalid color code \"{args[0]}\""


def cmd_cls(args=None, kwargs=None):
    if kwargs is None:
        kwargs = {}
    if args is None:
        args = []
    global CLS
    CLS = True
    return ""


def cmd_info(args=None, kwargs=None):
    if kwargs is None:
        kwargs = {}
    if args is None:
        args = []

    if not args:
        return Art.frogameIntroduction

    if args[0] == "lyagva":
        return Art.lyagvaIntroduction

    return Art.frogameIntroduction


def cmd_ls(args=None, kwargs=None):
    if kwargs is None:
        kwargs = {}
    if not args:
        args = []

    path = kwargs["path"]
    node = getNode(root, path.split("/"))

    if path == "":
        return "\n".join(
            getNames(getChildrenNodes(root))
        )

    if node is None:
        return "Error, no path found"

    return "\n".join(
        getNames(getChildrenNodes(node))
    )


def combinePath(initialPath, additionalPath):
    if len(initialPath) > 0 and initialPath[-1] != "/":
        initialPath += "/"

    fullPath = initialPath + additionalPath
    fullPath = fullPath.split("/")

    newPath = []
    for item in fullPath:
        if item == "..":
            if len(newPath) >= 1:
                newPath.pop()
        else:
            newPath.append(item)

    stringPath = "/".join(newPath)
    return stringPath


def cmd_cd(args=None, kwargs=None):
    if kwargs is None:
        kwargs = {}
    if not args:
        args = []

    if len(args) < 1:
        return "No path provided"

    stringPath = combinePath(kwargs["path"], args[0])

    global PATH
    PATH = stringPath

    return ""


def cmd_cat(args=None, kwargs=None):
    if kwargs is None:
        kwargs = {}
    if not args:
        args = []

    if len(args) == 0:
        return "No file path provided. Use \"help cat\" to get additional information"

    path = combinePath(kwargs["path"], args[0])
    node = getNode(root, path.split("/"))
    if node is None:
        return "No file found"

    if node.tag == "folder":
        return "Provided path leads to a folder. Use *file* path as an argument to get content of it"

    return getNodeText(node)


def getKwargValue(args, key, default=""):
    if args.count(key) <= 0 or len(args) - 1 <= args.index(key):
        return default
    return args[args.index(key) + 1]


def cmd_audio(args=None, kwargs=None):
    if kwargs is None:
        kwargs = {}
    if not args:
        args = []

    if len(args) == 0:
        return "No arguments provided. Use \"help audio\" to get additional information"

    output = []

    if args.count("-load"):
        output.append(audioLoad(
            combinePath(kwargs["path"], getKwargValue(args, "-load", ""))
        ))
    elif args.count("-l"):
        output.append(audioLoad(
            combinePath(kwargs["path"], getKwargValue(args, "-l", ""))
        ))

    if args.count("-volume"):
        output.append(audioVolume(getKwargValue(args, "-volume", "0.1")))
    elif args.count("-vol"):
        output.append(audioVolume(getKwargValue(args, "-vol", "0.1")))
    elif args.count("-v"):
        output.append(audioVolume(getKwargValue(args, "-v", "0.1")))

    if args.count("-loop"):
        output.append(audioLoop(getKwargValue(args, "-loop", "false")))

    if args.count("-info"):
        output.append(audioInfo(kwargs))

    if args.count("-play"):
        output.append(audioPlay())
    if args.count("-pause"):
        output.append(audioPause())
    if args.count("-stop"):
        output.append(audioStop())
    
    if args.count("-set"):
        output.append(audioSet(getKwargValue(args, "-set", "0"), kwargs))
    if args.count("-move"):
        output.append(audioMove(getKwargValue(args, "-move", "0"), kwargs))

    output = [i for i in output if i != ""]
    return "\n".join(output)


def audioLoad(path):
    node = getNode(root, path.split("/"))

    if node is None:
        return "No file found"

    audioPath = node.get("src")

    if audioPath is None:
        return "Specified file is not an audio"

    global AUDIO_PATH
    AUDIO_PATH = audioPath

    return ""


def audioVolume(volume):
    try:
        float(volume)
    except ValueError:
        return "Specified value is not a number"

    volume = float(volume)
    volume = min(max(0.0, volume), 1.0)

    global AUDIO_VOLUME
    AUDIO_VOLUME = str(volume)
    return ""


def audioLoop(value):
    global AUDIO_LOOP
    if value not in ("true", "false"):
        value = "false"

    AUDIO_LOOP = value
    return ""


def audioInfo(kwargs):
    src = kwargs["audioSrc"]
    try:
        duration = float(kwargs["audioDuration"])
        if math.isnan(duration):
            duration = 0
    except ValueError:
        duration = 0

    try:
        playback = float(kwargs["audioPlayback"])
    except ValueError:
        playback = 0

    return "Audio Duration\t" + f"{math.floor(duration) // 60}:{math.floor(duration) % 60}" + \
           "\nAudio Playback\t" + f"{math.floor(playback) // 60}:{math.floor(playback) % 60}" + \
           "\nAudio Source\t" + str(src)


def audioPlay():
    global AUDIO_STATE
    AUDIO_STATE = "play"
    return ""


def audioPause():
    global AUDIO_STATE
    AUDIO_STATE = "pause"
    return ""


def audioStop():
    global AUDIO_STATE
    AUDIO_STATE = "stop"
    return ""


def audioSet(timecode, kwargs):
    try:
        duration = float(kwargs["audioDuration"])
        if math.isnan(duration):
            duration = 0
    except ValueError:
        duration = 0
    
    try:
        timecode = float(timecode)
        if math.isnan(timecode):
            timecode = 0
    except ValueError:
        timecode = 0
    
    if timecode >= duration:
        timecode = 0
    
    global AUDIO_PLAYBACK
    AUDIO_PLAYBACK = str(timecode)
    return ""


def audioMove(timecode, kwargs):
    try:
        duration = float(kwargs["audioDuration"])
        if math.isnan(duration):
            duration = 0
    except ValueError:
        duration = 0
    
    try:
        playback = float(kwargs["audioPlayback"])
    except ValueError:
        playback = 0
    
    try:
        timecode = float(timecode)
        if math.isnan(timecode):
            timecode = 0
    except ValueError:
        timecode = 0
    
    timecode += playback
    
    if timecode >= duration:
        timecode = 0
    
    global AUDIO_PLAYBACK
    AUDIO_PLAYBACK = str(timecode)
    return ""


def cmd_app(args=None, kwargs=None):
    if kwargs is None:
        kwargs = {}
    if not args:
        args = []
    
    if len(args) == 0:
        return "No filepath provided"

    path = combinePath(kwargs["path"], args[0])
    node = getNode(root, path.split("/"))

    if node is None:
        return "No file found"

    appPath = node.get("app")
    if appPath is None:
        return "Specified file is not an app"

    global MODE
    MODE = appPath
    return ""
