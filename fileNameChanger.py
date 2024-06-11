'''
This program will change names & extensions of files in a folder. It will also add a number at the end of the New File name.

valid example of existing name: 'American.Dad.S19E21.Echoes.1080p.DDP.5.1.H.265.-2020.mkv'

^names have to be in 'S01E01' format and have to appear before other numbers in name.

example of invalid name: '2020.American.S19E21.Echoes.Ect' or '2012-American.Dad.E21.Echoes.Ect'

If you want to sort by just Episode-Number make sure there are NO OTHER NUMBERS in each title and episodeNumbering = True

valid examples of episode numbering: 'American.Dad.E22' ,'FamilyGuy-Best.Episode.ever.E10' , 'SimpsonsE01BartIsCool'

example newName = 'E'

Output: E01 ,E02

directory = "Source-LocalFolderName"
newDirectory = "Destination-LocalFolderName"
newName = "S04E" : Name at begining of file. This will generate S04E01, S04E02, S04E03, ect.
extension = ".mp4" : Assign extension, default = '' ,is auto.
overwrite = True : Checks if folder exists. It will not overwrite existing files!
dictionary = "stringOfStuffToRemove" : Removes whatever is in the string, default should be all alphabet + symbols. By default removes everything but numbers.
episodeNumbering = False : Only change to True if you are sorting by episode number only, E01, e02, E03 ect.
'''

directory = "Welcome to Wrexham (2022) Season 1 S01"
newDirectory = "Welcome to Wrexham 2022 S1"
newName = "S01E"
extension = ""
overwrite = False
episodeNumbering = True
dictionary = '£$()_-.&ABCDEFGHIJKLMNOPQRSTUVXWYZabcdefghijklmnopqrstuvwxyz '

import os
x = 0
def sortItOut(e):
    try:
        aa = e.translate({ord(i): None for i in dictionary})
        
        if int(aa) < 100:
            aa = '01' + aa
    except:
        pass
    print(aa[:4])
    if aa[:4] == None:
        pass
    return (aa[:4])
def removeFolder():
    os.rmdir(newDirectory)
def addFolder():
    if not os.path.exists(newDirectory):
        if os.path.exists(directory):           
            os.makedirs(newDirectory)
    elif not overwrite:
        print("Is the source directory valid?")
        print("As well as ensure the new directory does not exist first or set overwrite = True.")
        exit()
    else:
        print("Overwrite mode. Double check your source and destination!")
close = False
while True:
    addFolder()
    
    folderCheck = os.listdir(directory)
    temp = directory
    print(folderCheck)
    for name in folderCheck:
        temp = os.path.join(directory, name)
        #print(temp)
        if not os.path.isfile(temp):
            print("Folders present in, '"+directory+"' Please remove folders from the source directory.")
            close = True
    if close == True:
        removeFolder()
        break
    try:    
        listFiles = os.listdir(directory)
        #print(listFiles)
    except FileNotFoundError:
        print(directory+": Source directory not found.")
        break
    #listFiles.remove('')
    try:
        
        listFiles.sort(key = sortItOut)
    except ValueError:        
        print("Probably an error with the sorting function. If used. (Ignore if folders are present)")
    except FileNotFoundError:
        print(directory + " Source directory not found.")
        break
    tempList = list(listFiles)
    tempList.sort(key = sortItOut)
    newTempList = []
    bogus = 0
    checkBogus = 0
    close = False
    for stuff in tempList:
        aaa = stuff.translate({ord(i): None for i in dictionary})
        print(aaa[:4])
        checkBogus = int(aaa[:2])
        if checkBogus > 1 and checkBogus < 10 and not episodeNumbering:
            close = True
            print("Episode Numbering Error, E"+str(aaa[:2]))
            print("Set episodeNumbering to True if you are sorting by Episode number only!")
            break
        if bogus != 0:
            if bogus != int(aaa[:2]):
                print("Miss matched seasons : Season: "+str(bogus)+" , Season: "+aaa[:2])
                close = True
                break
        bogus = int(aaa[:2])
        print(bogus)
    if close == True:
        print("Exiting program.")
        removeFolder()
        break
    else:
        print("File names all good!")
    count = 0
    
    for filename in listFiles:
        print(filename)
        a = os.path.join(directory, filename)
        name = ""
        if os.path.isfile(a):
            x += 1            
            if extension == "" :
                extension = os.path.splitext(a)[1]
            if x < 10:
                tempName = newName+"0"+str(x)+extension 
            else:
                tempName = newName+str(x)+extension
            b = os.path.join(newDirectory, (tempName))            
            os.rename( a , b )
            
        else:
            count += 1
    print("Files moved to: "+newDirectory)   
    if count > 0:
        print(str(count),"(Ignored) folders present.")    
    print("Done!")    
    break