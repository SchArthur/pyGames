def loadFile(path):
    file = open(path, 'r')

    content = file.readlines()

    file.close()
    
    return content