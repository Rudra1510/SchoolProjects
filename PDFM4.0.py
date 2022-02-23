from PIL import Image
import PyPDF2
import shutil
import os




#Current Folder
Folder = input("Folder [Hit Enter to select current working directory]:")
if Folder=="":
    Folder = os.getcwd()


# Replacing backslashes with forewardslashes, cuz OS issues.
Folder = Folder.replace("\\", "/")
if Folder.endswith("/") == False:
    Folder += "/"
# Defining the Merger function
Merger = PyPDF2.PdfFileMerger()
#Moving the Original Contents of the folder to "Content" folder. - 1
ContentFolder = Folder+"Content"
NewFiles = [ContentFolder + "/" +File for File in os.listdir(Folder)]


def Error(Folder,File):
    ErrorFolder = Folder+"Error"
    if not os.path.isdir(ErrorFolder):
        os.mkdir(ErrorFolder)
    SourceFilePath = f"{Folder}{File}"
    DestinationFilePath = f"{Folder}Error/{File}"
    os.replace(SourceFilePath,DestinationFilePath)


# Reading the files from the folder and appending them to the Merger
Files = [Folder + File for File in os.listdir(Folder)]
#Temp folder for Processing image files to pdf
TempFolder = Folder+"Temp"

#Looping through Files
for File in Files:

    #Incase file is a pdf
    if File.endswith('.pdf'):
        with open(File, "rb") as f:
            Merger.append(PyPDF2.PdfFileReader(f))
    
    #And incase file is not pdf
    elif not File.endswith('.pdf'):

        #If TempFolder doesn't exist this will create it.
        if not os.path.isdir(TempFolder):
            os.mkdir(TempFolder)

        #File name with extension and without extension
        FileNameExt = File.split('/')[-1]
        FileName = ".".join(FileNameExt.split('.')[0:-1])
        
        #Converting File to pdf
        with open(f"{TempFolder}/{FileName}.pdf","wb") as f:
            try:
                # f.write(img2pdf.convert(File))
                f.write(None)
            #For any kind of error it will skip it, and store the file in Error folder.
            except Exception as e:
                print(f"{File}: {type(e).__name__}")
                
                ErrorFolder = Folder+"Error"
                if not os.path.isdir(ErrorFolder):
                    os.mkdir(ErrorFolder)
                SourceFilePath = f"{Folder}{FileNameExt}"
                DestinationFilePath = f"{Folder}Error/{FileNameExt}"
                os.replace(SourceFilePath,DestinationFilePath)

                continue

        #Name of the current file
        File = f"{TempFolder}/{FileName}.pdf"
    
        #Adding it to the Merger instance
        with open(File, "rb") as f:
            Merger.append(PyPDF2.PdfFileReader(f))

# Getting OutputFile name and writing the Merger instance to the OutputFile.
OutputFile = Folder + Folder.split("/")[-2] + ".pdf"
Merger.write(OutputFile)

#Deleting the Temp Folder
if os.path.isdir(TempFolder):
    shutil.rmtree(TempFolder)

#Moving the Original Contents of the folder to "Content" folder. - 2
if not os.path.isdir(ContentFolder):
    os.mkdir(ContentFolder)
for src,dst in zip(Files,NewFiles):
    os.replace(src,dst)

# ---------------------------------------------------------------------------------------------------