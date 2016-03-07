def zext4(string):
    string = str(string)
    return '0'*(4-len(string)) + string

with open("textOfPage.txt") as f:
    newStr = ""
    num = 1
    while num < 364:
        for i in range(4):
            newStr += f.readline()
   
        picline = f.readline()
        if picline.find("File") != -1:
            newStr += picline
        else:
            newStr += picline.rstrip() + " [[File:nch " + zext4(num) + ".png|200px]]\n"
        newStr += f.readline()
        num+=1

    with open("editedText.txt", "w") as g:
        g.write(newStr)
