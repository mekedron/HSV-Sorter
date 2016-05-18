#from distutils.core import setup
import os, sys, shutil, time, operator, math, string, random, colorsys
from PIL import Image

config = {
    'extensions': ['.png', '.jpg', '.jpeg', '.gif'],
    'thumbSize': [1, 1],
    'bufferCleaner': ' ' * 100
}
def generateId(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def askSomething(q):
    r = input(q+' (y(es) or something)?: ')
    return ((r == 'yes') or (r == 'y'))

def selectPath(ne = False):
    p = ''
    check = True
    while check: #magic
        p = input('Please type a valid path: ').strip('"')
        isDir = (os.path.isdir(p) and (p != ''))
        check = (isDir == ne)
    else:
        p = os.path.abspath(p)
        print('Selected path: \''+p+'\'')
    return p
    
def selectLimited(a, r = 'Your select is: '):
    s = ''
    c = True
    
    while c:
        s = input(r).strip()
        try:
            a.index(s)
            c = False
        except Exception:
            c = True
    return s

def main(config):
    #print('Args: '+str(sys.argv));
    startupPath = ''
    if (len(sys.argv) > 1):
        if (os.path.isdir(sys.argv[1].strip('"'))):
            startupPath = os.path.abspath(sys.argv[1].strip('"'))
    if (startupPath == ''):
        startupPath = selectPath()
    usingPath = startupPath
    filesList = os.listdir(usingPath)
    for file in filesList:
        if (not(file.lower().endswith(tuple(config['extensions'])))):
            filesList.remove(file)
    '''
    if (askSomething('Do you want to copy the directory')):
        print('Type a path that not exist!')
        usingPath = selectPath(True)
        os.makedirs(usingPath)
        print('Current path: '+usingPath+'\nThe directory was created (^).')
        for file in filesList:
            print('+Copying '+file)
            shutil.copyfile(os.path.join(startupPath, file), os.path.join(usingPath, file))
    '''
    print(
        'Please, select sorting mode what do you want.\n'\
        ' 1  - H V S\n'\
        ' 2  - H S V\n'\
        ' 3  - V S H\n'\
        ' 4  - V H S\n'\
        ' 5  - S H V\n'\
        ' 6  - S V H\n'\
        ' 7  - H V\n'\
        ' 8  - H S\n'\
        ' 9  - V H\n'\
        ' 10 - V S\n'\
        ' 11 - S H\n'\
        ' 12 - S V\n'\
        ' 13 - H\n'\
        ' 14 - V\n'\
        ' 15 - S'
    )
    pSort = selectLimited(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15'])
    print(
        'Please, select interpolation.\n'\
        ' 1  - NEAREST (use nearest neighbour)\n'\
        ' 2  - BILINEAR (linear interpolation in a 2x2 environment)\n'\
        ' 3  - BICUBIC (cubic spline interpolation in a 4x4 environment)\n'\
        ' 4  - ANTIALIAS (a high-quality downsampling filter)'\
    )
    pInterpolation = selectLimited(['1', '2', '3', '4'])
    pInterpolation = int(pInterpolation) - 1
    filesColor = {}
    for file in filesList:
        im = Image.open(os.path.join(usingPath, file))
        #im.thumbnail(config['thumbSize'], Image.NEAREST)
        im.thumbnail(config['thumbSize'], pInterpolation)
        #imageColors = (im.getcolors(im.size[0]*im.size[1])[0][1])
        imageColors = (im.getcolors(im.size[0]*im.size[1])[0][1])
        #imageColor = '%02x%02x%02x' % tuple([ imageColors[0], imageColors[1], imageColors[2] ])
        try:
            imageColor = colorsys.rgb_to_hsv(
                imageColors[0],
                imageColors[1],
                imageColors[2]
            )
            h = str(math.floor(imageColor[0]*100)).zfill(3)
            v = str(math.floor(imageColor[1]*100)).zfill(3)
            s = str(imageColor[2]).zfill(3)
            if (pSort == "1"):
                imageColor = [h, v, s]
            elif (pSort == "2"):
                imageColor = [h, s, v]
            elif (pSort == "3"):
                imageColor = [v, s, h]
            elif (pSort == "4"):
                imageColor = [v, h, s]
            elif (pSort == "5"):
                imageColor = [s, h, v]
            elif (pSort == "6"):
                imageColor = [s, v, h]
            elif (pSort == "7"):
                imageColor = [h, v]
            elif (pSort == "8"):
                imageColor = [h, s]
            elif (pSort == "9"):
                imageColor = [v, h]
            elif (pSort == "10"):
                imageColor = [v, s]
            elif (pSort == "11"):
                imageColor = [s, h]
            elif (pSort == "12"):
                imageColor = [s, v]
            elif (pSort == "13"):
                imageColor = [h]
            elif (pSort == "14"):
                imageColor = [v]
            else:
                imageColor = [s]
            s = "".join(imageColor)
            print('Color of '+file+' is '+s)
            im.close()
            filesColor[file] = s
        except Exception:
            print(' Skipping...')
    filesColor = sorted(filesColor.items(), key=operator.itemgetter(1))
    j = 0;
    for i in filesColor:
        j+=1;
        ext = i[0].split('.')[-1]
        #newName = i[1]+'.'+str(j)+'.'+ext;
        newName = str(j)+'.'+generateId()+'.'+ext;
        print('+Renaming \''+i[0]+'\' to \''+newName+'\'')
        #print('Copying'+('.'*j), end="\r")
        try:
            os.rename(
                os.path.join(usingPath, i[0]),
                os.path.join(usingPath, newName)
            )
        except Exception:
            print(' Skipping...')
            #print('Skipping'+('.'*j), end="\r")
    input('Done.'+config['bufferCleaner'])
main(config)