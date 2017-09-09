import re

def typeNameFromProperty(property):
    primitive = typeNameString(property.type)
    if primitive != None:
        return primitive

    if property.type == "array":
        elementName = typeNameString(property.itemType)
        return "Array<" + elementName + ">"

def typeNameFromParameter(parameter):
    primitive = typeNameString(parameter.type)

    if primitive == None:
        return "???????????????"

    return primitive

def typeNameString(typeName):
    if typeName == "integer":
        return "Int"
    elif typeName == "string":
        return "String"
    elif typeName == "boolean":
        return "Bool"
    elif typeName == "array":
        return None
    elif typeName == "file":
        return "File is not supported"
    elif typeName == None:
        return None
    else:
        print(typeName)
        m = re.search(r"#/definitions/(.*)", typeName)
        return m.group(1)

def makeCamelCase(snakeCaseString):
    return re.sub("_(.)",lambda x:x.group(1).upper(), snakeCaseString)

def makePascalCase(snakeCaseString):
    camelCase = makeCamelCase(snakeCaseString)
    return camelCase[0].upper() + camelCase[1:]