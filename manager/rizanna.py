import os
print("Hello!") 
print("Please introduce yourself, what is your name?")
name = str(input())
path = os.getcwd()

def intro():
    print(name+""",  To work with the file, press 1
    To work with directory,press 2""")

def filework():
    print("""If you want to
             delete file,press 1
             rename file,press 2
             add content to file,press 3
             rewrite content of this file,press 4
             """ )
    answer = int(input())

        #DeleteFile
    if answer == 1: 
        DeleteFile = input('Write the name of the file you want to delete:')
        if os.path.exists(DeleteFile):
            os.remove(DeleteFile)
            print('File was deleted successfully')
        else:
            print('ERROR,NO SUCH FILE')

        #RenameFile
    elif answer == 2: 
        RenameFile = input('Write the name of file you want to rename:')
        if os.path.exists(RenameFile):
            print('Rename the file')
            NewName = input()
            os.rename(RenameFile,NewName)
            print('File was renamed successfully')
        else:
            print('ERROR.NO SUCH FILE')

        #AddContent
    elif answer == 3:
        NewContent = input('Write the name of the file you want to add content:')
        if os.path.exists(NewContent):
            b = open(NewContent, 'a')
            NewContent = str(input('What do you want to add?'))
            b.write(NewContent)
            b.close()
            print('Content was added')
        else:
            print('ERROR,NO SUCH FILE')

        #RewriteContentofFile
    elif answer == 4: 
        FileName = input('Write the name of file to rewrite content:')
        if os.path.exists(FileName):
            c=open(FileName,'w')
            ReWrite = input('What do you want to rewrite?')
            c.write(ReWrite)
            c.close()
            print('Content was rewritten successfully')
        else:
            print('ERROR,NO SUCH FILE')

def directory():
        print("""If you want to
                 rename directory,press 1
                 print number of files,press 2
                 print number of directories,press 3
                 list content of the directory,press 4
                 add file to this directory,press 5
                 add new directory,press 6""")

        choise = int(input())

            #RenameDirectory
        if choise == 1:  
            RenameDir = input('Write the name of directory you want to rename:')
            if os.path.exists(RenameDir):
                NewDirName = input('Rename the directory:')
                os.rename(RenameDir,NewDirName)
                print('Directory was renamed successfully')
            else:
                print('ERROR')

            #NumberofFiles
        elif choise == 2: 
            num = 0
            for f in os.listdir():
                NumofFiles = os.path.join(f)
                if os.path.isdir(NumofFiles):
                    num+=1
            print("Number of files: ",num)

            #NumberofDirectories
        elif choise == 3: 
            num = 0
            for f in os.listdir():
                NumofDir = os.path.join(f)
                if os.path.isdir(NumofDir):
                    num+=1
            print("Number of directories: ",num)

            #ListContentoftheDir
        elif choise == 4: 
            print(os.listdir())

            #AddFiletoDirectory
        elif choise == 5: 
                FileAdd = input('Write the name for new file:')
                AddFile = open(FileAdd + '.txt', 'w')
                print('File was successfully added to this directory')
            
            #AddNewDirectory
        elif choise == 6: 
             DirAdd = input('Write the name for new directory: ')
             os.mkdir(DirAdd)
             print('Directory was added')
             
programm = True
while programm:
    intro()
    point = int(input())
    if point == 1:
        print('I am your file manager')
        filework()
    elif point == 2:
        print('I am your directory manager')
        directory()

    














