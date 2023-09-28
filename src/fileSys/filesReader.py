import xml.etree.ElementTree as ET
from src.artConverter import convertToPython

from pathlib import Path
current_path = str(Path(__file__).parent.resolve()) + "/../../"


tree = ET.parse(current_path + "src/fileSys/fileSys.xml")
root = tree.getroot()


def getNode(root, path):
    if root is None:
        return None

    if len(path) == 0:
        return root

    if len(path) == 1:
        return root.find(f"./*[@name='{path[0]}']")
    
    return getNode(root.find(f"./*[@name='{path[0]}']"), path[1:])


def getChildrenNodes(root, path=None):
    if path is None:
        path = []
    
    if path != "":
        root = getNode(root, path)

    if root is None:
        return []
    
    return root.findall("./")


def getNames(nodes):
    return [i.get("name") for i in nodes]


def getNodeText(node):
    content = node.get("content")
    if content is None:
        text = node.text
    else:
        text = convertToPython(f"arts/{content}")
    text = text.replace("\\n", "\n").replace("\\t", "\t")
    return text


if __name__ == "__main__":
    print(getChildrenNodes(root, "folder_1".split("/")))
