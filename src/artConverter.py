def convertToPython(filename="arts/lyagvaIntroduction.txt"):
    result = ""
    try:
        with open(filename, mode="r", encoding="UTF-8") as file:
            for line in file.readlines():
                result += line.replace("\\t", "\t")
    except FileNotFoundError as e:
        print(e)
        return ""
    return f"{result}"


def convertToJs(filename="arts/lyagvaIntroduction.txt"):
    result = ""
    with open(filename, mode="r", encoding="UTF-8") as file:
        for line in file.readlines():
            result += line.replace("\n", "") + "\\n"
    return f"\"{result}\""


if __name__ == "__main__":
    print(convertToJs("../arts/lyagvaIntroduction.txt"))
