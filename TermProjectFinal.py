from __future__ import division
from visual import *
from visual.controls import *
import random
import string

class ShapeMaker(object):
    def init(self, rows,cols,height):
        self.rows = rows
        if(cols==0): self.cols = rows
        else: self.cols = cols
        if(height ==0):self.h = rows
        else: self.h = height
        #if height and cols equals 0, we are dealing with a cube
        self.grid1 = self.rows*self.cols
        self.grid2 = self.rows*self.h
        self.grid3 = self.cols*self.h
        #grids are the number of faces in front/back, left/right and top/Bottom
        l, b, h, offset = 0.98, 0.98, 0.05, 3
        self.textPos = self.rows/2 + offset
        self.sizes = [(l,b,h), (l,b,h),(h,l,b), (h,l,b), (l,h,b), (l,h,b)]
        #these dimensions give the lenght, breath and width of individual
        #boxes in all 6 directions
        self.sideColors = [color.red,color.orange, color.green,color.blue,
                             color.yellow,color.white]
        #front, back, right, left, top, bottom
        self.showKeys = True
        self.solutionMode = False
        self.shuffleMode = False
        self.solveMode = False
        self.keysPressed = [] #initiates list of keysPressed for rotation

    def getFace(self,rows, cols=0, height = 0):
        #creates only the front face for the user
        self.clearAll()
        self.preStart=False
        self.init(rows, cols, height)
        rows, cols, h  = self.rows, self.cols, self.h
        rowSize, colSize, hSize = rows/2, cols/2, h/2
        dirRows, dirCols = self.getDivs(rows), self.getDivs(cols)
        for a in dirCols:
            for b in dirRows:
                box(color=self.sideColors[0], pos = (a,b,hSize),
                          size = (.98,.98,.05))
        rate(5) #after a short period, turns the front face into a cube-oid
        self.getCube()

                
    def getCube(self):
        self.clearAll()
        self.init(self.rows, self.cols,self.h)
        self.frontBack, self.rightLeft, self.topBottom, self.boxes=[],[],[],[]
        rows, cols, h = self.rows, self.cols, self.h
        rowSize, colSize, hSize = rows/2, cols/2, h/2
        dirRows, dirCols = self.getDivs(rows), self.getDivs(cols)
        dirHs = self.getDivs(h)
        frontBack,leftRight,topBottom = [0,1], [2,3], [4,5]
        #the above represents the indeces of the faces for pos, color & size
        self.addSides(frontBack, dirCols, dirRows, hSize)
        self.addSides(leftRight, dirHs, dirRows, colSize)
        self.addSides(topBottom, dirCols, dirHs, rowSize)
        self.frontBack = self.boxes[:self.grid1*2]
        offset1 = self.grid1*2
        self.rightLeft = self.boxes[offset1: offset1+self.grid2*2]
        offset2 = offset1+self.grid2*2
        #gives starting index of top/bottom in self.boxes
        self.topBottom = self.boxes[offset2:]
        #we now have list of the parallel faces
        if self.preStart!=True:
            #this ensures that keys aren't drawn in instructions mode
            self.drawRotationKeys()
            self.getRotateKey() #allows user to make rotations
            
    def addSides(self, sidesIndex, dir1, dir2, size):
        #gets indeces, rows and cols for each face, creates them and adds them
        #to list of boxes
        for i in sidesIndex:
            for a in dir1:
                #for front face a would be horizontal box starting indeces 
                for b in dir2:
                    #for front face b is vertical box starting indeces 
                    positions = [(a,b,size), (a,b,-size), (size,b,-a),
                                 (-size, b,-a), (a,size,-b), (a,-size,-b)]
                    makeBox = box(color=self.sideColors[i], pos = positions[i],
                            size= self.sizes[i])
                    self.boxes.append((makeBox, self.sideColors[i]))
        
    def drawRotationKeys(self):
        #draws the rotation keys that need to be pressed by the user.
        dirRows = self.getDivs(self.rows)
        dirCols = self.getDivs(self.cols)
        offset = .25
        i=0
        for a in dirRows:
            #draws left and right keys to rotate rows
            xmin, xmax = min(dirCols)-1 -offset,max(dirCols) + 1
            text(pos=(xmin,a-offset,self.h/2), text = string.ascii_lowercase[i],
                 color=color.white, height=0.5)
            text(pos=(xmax,a-offset,self.h/2),text=string.ascii_uppercase[i],
                 color=color.white, height=0.5)
            i+=1
        self.drawTopKeys(i)

    def drawTopKeys(self,i):
        #draws top and bottom keys for vertical rotations
        dirRows = self.getDivs(self.rows)
        dirCols, dirHs = self.getDivs(self.cols), self.getDivs(self.h)
        offset = .25
        for a in dirCols:
            xmin, xmax = min(dirRows)-1-offset,max(dirRows) + 1
            text(pos=(a-offset,xmax,self.h/2), text = string.ascii_lowercase[i],
                 color=color.white, height=0.5)
            text(pos=(a-offset, xmin,self.h/2),text=string.ascii_uppercase[i],
                 color=color.white, height=0.5)
            i+=1
        for a in dirHs:
            x1, x2 = self.cols/2, -self.cols/2
            text(pos=(x1,xmin,-a-offset),text=string.ascii_lowercase[i],
                 color=color.white, height=0.5, axis=(0,0,-1))
            text(pos=(x1,xmax,-a-offset),text=string.ascii_uppercase[i],
                 color=color.white, height=0.5, axis =(0,0,-1))
            text(pos=(x2,xmin,-a-offset),text=string.ascii_uppercase[i],
                 color=color.white, height=0.5, axis=(0,0,1))
            text(pos=(x2,xmax,-a-offset),text=string.ascii_lowercase[i],
                 color=color.white, height=0.5, axis = (0,0,1))
            i+=1

    def removeKeys(self):
        #user can press a buttom to remove the rotation key instructions
        if(self.preStart==False):
            self.showKeys = False
            for object in scene.objects:
                if type(object)!=box:
                    object.visible=False
            if(self.solutionMode==True):
                (pos, axis, wrongpos) = self.textPosition()
                text(text=("Press %s" % self.solutionKey), align = "center",
                     pos=pos,color=color.white, axis = axis)

    def showKey(self):
        #redraws the rotation keys
        if self.preStart==False:
            self.drawRotationKeys()
            self.showKeys = True
                        
    def getDivs(self,measure):
        divisions = []
        size = measure/2
        if(measure%2==0):
            #if rows/cols/h's are even then the positions of seperate squares on
            #each face have intial (non specified x,y,z) positions as [-.5,.5] 
            half = size - 0.5
            x = -half
            while half>=x:
                divisions.append(x)
                x+=1
        elif(measure%2==1):
            #if rows/col/h's are odd then the positions of seperate squares on
            #each face have intial (non specified x,y,z) positions as [-1,0,1] 
            divisions = range(int(-size),int(size)+1)
        return divisions

    @classmethod
    def testGetDivs(cls):
        print "testing getDivs()...",
        assert(ShapeMaker().getDivs(2)== [-0.5,0.5])
        assert(ShapeMaker().getDivs(3)==[-1,0,1])
        assert(ShapeMaker().getDivs(4)==[-1.5,-0.5,0.5, 1.5])
        assert(ShapeMaker().getDivs(5)==[-2,-1,0,1,2])
        print "passed!"
    
    def getRotateKey(self):
        #waits for the user to press a valid key for rotation
        while True:
            key = scene.kb.getkey()
            self.keyNumber = ord(key.lower())-ord('a')
            if(self.checkValidKeyPress()):
                self.keysPressed.append(key)
                #adds key to list of pressed keys used to get solution later
                break
        self.rotate(key)

    def checkValidKeyPress(self):
        #retuns True only if it is possible to use keyPressed to obtain
        #rotation frame
        possibleKeys= self.rows+self.cols+self.h
        if(0<=self.keyNumber<possibleKeys):
            return True
        else:
            return False
        
    @classmethod
    def testCheckValidKeyPress(cls):
        print "testing checkValidKeyPress()...",
        ShapeMaker.rows = ShapeMaker.cols = ShapeMaker.h = 3
        ShapeMaker.keyNumber = 5
        assert(ShapeMaker().checkValidKeyPress()==True)
        ShapeMaker.keyNumber = 10
        assert(ShapeMaker().checkValidKeyPress()==False)
        ShapeMaker.rows = 4
        ShapeMaker.cols = 5
        ShapeMaker.h = 3
        ShapeMaker.keyNumber =0
        assert(ShapeMaker().checkValidKeyPress()==True)
        ShapeMaker.keyNumber = 12
        assert(ShapeMaker().checkValidKeyPress()==False)
        print "passed!"
        
    def rotate(self, key):
        #rotates squares by obtaining rotation frame based on key pressed
        mps = 15
        self.keyNumber = ord(key.lower())-ord('a')
        self.angle= self.getAngle(key)
        if (self.keyNumber<self.rows):
            axis = (0,1,0)
            rotationframe = self.horizontalRotFrame()
        elif(self.rows<=self.keyNumber<self.rows+self.cols):
            axis = (1,0,0)
            rotationframe = self.frontVerticalRotFrame()
        else:
            axis = (0,0,1)
            rotationframe = self.sideVerticalRotFrame()
        for r in arange(0,self.angle,self.angle/mps):
            rate(mps)
            rotationframe.rotate(angle = self.angle/mps, axis=axis)
        self.newColors = self.updateBoxes() #updates the list of boxes
        self.makeNewCube()

    def getAngle(self,key):
        if(self.rows==self.cols==self.h):
            #90 degree rotations in cubes
            if(key.isupper()): self.angle = pi/2
            else: self.angle = -pi/2
        else:
            #180 degree rotations in cuboids
            if(key.isupper()): self.angle = pi
            else: self.angle = -pi
        return self.angle

    @classmethod
    def testGetAngle(cls):
        print "testing getAngles()...",
        ShapeMaker.rows = ShapeMaker.cols = ShapeMaker.h = 3
        assert(ShapeMaker().getAngle('a')==-pi/2)
        assert(ShapeMaker().getAngle('D')==pi/2)
        ShapeMaker.rows = 4
        ShapeMaker.cols = 5
        ShapeMaker.h = 3
        assert(ShapeMaker().getAngle('d')==-pi)
        assert(ShapeMaker().getAngle('G')==pi)
        print "passed!"
        
    def makeNewCube(self):
        #this list makes the cubes based on the list of colors of all boxes
        #obtained after rotation
        self.clearAll()
        self.frontBack, self.rightLeft, self.topBottom,self.boxes=[],[],[],[]
        rowSize, colSize, hSize = self.rows/2, self.cols/2, self.h/2
        dirRows, dirCols = self.getDivs(self.rows), self.getDivs(self.cols)
        dirHs = self.getDivs(self.h)
        frontBack,leftRight,topBottom = [0,1], [2,3], [4,5]
        fbColorI, rlColorI, tbColorI =0,2*self.grid1, 2*(self.grid1+self.grid2)
        #the above represents the indeces of the faces for pos, color & size
        self.addNewSides(frontBack, dirCols, dirRows, hSize, fbColorI)
        self.addNewSides(leftRight, dirHs, dirRows, colSize, rlColorI)
        self.addNewSides(topBottom, dirCols, dirHs, rowSize, tbColorI)
        self.frontBack = self.boxes[:self.grid1*2]
        offset1 = self.grid1*2
        self.rightLeft = self.boxes[offset1: offset1+self.grid2*2]
        offset2 = offset1+self.grid2*2 #gives starting index of top/bottom
        self.topBottom = self.boxes[offset2:]
        self.checkForWin()
        #we now have list of the parallel faces
        if(self.shuffleMode!=True and self.showKeys==True):
            self.drawRotationKeys()
        if(self.shuffleMode!=True and self.solutionMode!=True):
            self.getRotateKey()

    def addNewSides(self, sidesIndex, dir1, dir2, size, colorI):
        #takes the list of colors in account based on the indeces of the boxes
        index = colorI
        for i in sidesIndex:
            for a in dir1:
                for b in dir2:
                    positions = [(a,b,size), (a,b,-size), (size,b,-a),
                                 (-size, b,-a), (a,size,-b), (a,-size,-b)]
                    makeBox = box(color=self.newColors[index],
                                  pos = positions[i], size= self.sizes[i])
                    self.boxes.append((makeBox, self.newColors[index]))
                    index+=1
        #if the cube is not in shuffle mode, obtains another key for rotation
        #from the user

    def checkForWin(self):
        #checks if the user has solved the cube 
        if(self.preStart==False):
            if (self.win()):
                pos, axis, wrgPos = self.textPosition()
                text(text="YOU SOLVED IT!",pos = pos, axis=axis,
                     align = "center")
                self.keysPressed = []
                
    def win(self):
        # rubix cube is solved if all 6 faces have only one color of boxes
        for i in xrange(0,len(self.frontBack),self.grid1):
            for index in xrange(i,i+self.grid1-1):
                #check colors of front and back faces
                if self.newColors[index]!=self.newColors[index+1]:
                    return False
        offset = self.grid1*2
        for i in xrange(offset,offset+len(self.rightLeft),self.grid2):
            for index in xrange(i,i+self.grid2-1):
                #checks colors of right and left faces
                if self.newColors[index]!=self.newColors[index+1]:
                    return False
        offset2 = offset+self.grid2*2
        for i in xrange(offset2,offset2+len(self.topBottom),self.grid3):
            for index in xrange(i,i+self.grid3-1):
                #checks colors of top and bottom
                if self.newColors[index]!=self.newColors[index+1]:
                    return False
        return True
                   
    def clearAll(self):
        #clears the screen
        for object in scene.objects:
            object.visible=False
            del object

    #There are different fucntions to get the rotations frames since the 
    #orientation of boxes in non-parallel faces is different
    def horizontalRotFrame(self):
        self.colors, rotationframe = [], frame()
        self.faces = self.frontBack+self.rightLeft
        for i in xrange(self.keyNumber, len(self.frontBack), self.rows):
            #adds rotating boxes of front and back faces
            self.colors.append(self.frontBack[i])
            #makes a list of color of rotating boxes
            self.frontBack[i][0].frame = rotationframe
            #puts rotated boxes in the same rotation frame
        for i in xrange(self.keyNumber, len(self.rightLeft), self.rows):
            #adds rotating boxes of left anf right 
            self.colors.append(self.rightLeft[i])
            self.rightLeft[i][0].frame = rotationframe
        if(self.keyNumber==0): #bottom row rotates bottom face as well
            bottom = self.topBottom[self.grid3:]
            for cube in bottom:
                cube[0].frame = rotationframe
            self.faces += bottom
        elif(self.keyNumber==self.rows-1):#top row rotates top face as well
            top = self.topBottom[:self.grid3]
            for cube in top:
                cube[0].frame = rotationframe
            self.faces += top
        return rotationframe

    def frontVerticalRotFrame(self):
        self.colors,rotationframe, colNumber=[],frame(),self.keyNumber-self.rows
        self.faces = self.frontBack+self.topBottom
        startN1, startN2 = colNumber*self.rows, colNumber*self.h
        #the starting index number of topbottom and frontback are different
        for i in xrange(startN1, len(self.frontBack), self.grid1):
            #adds rotating boxes of front and back faces
            for colBox in xrange(i,i+self.rows):
                self.colors.append(self.frontBack[colBox])
                self.frontBack[colBox][0].frame = rotationframe
        for i in xrange(startN2, len(self.topBottom), self.grid3):
            #adds rotating boxes of top and bottom faces
            for colBox in xrange(i,i+self.h):
                self.colors.append(self.topBottom[colBox])
                self.topBottom[colBox][0].frame = rotationframe
        if(colNumber==0): #leftmost column inclubdes left face as well
            left = self.rightLeft[self.grid2:]
            for cube in left: cube[0].frame = rotationframe
            self.faces +=left
        elif(colNumber==self.cols-1):
            #rightmost column inclubdes left face as well
            right = self.rightLeft[:self.grid2]
            for cube in right: cube[0].frame = rotationframe
            self.faces+=right
        return rotationframe
        
    def sideVerticalRotFrame(self):
        self.colors,rotationframe=[],frame()
        colNumber = self.keyNumber-self.rows-self.cols
        #ranges from 0 to self.h-1
        startingNumber = colNumber*self.rows
        self.faces = self.rightLeft+self.topBottom
        for i in xrange(startingNumber, len(self.rightLeft), self.grid2):
            #gets the rotating boxes of right and left faces
            for colBox in xrange(i,i+self.rows):
                self.colors.append(self.rightLeft[colBox])
                self.rightLeft[colBox][0].frame = rotationframe
        for i in xrange(colNumber, len(self.topBottom), self.h):
            #gets rotating boxes of top and bottom faces
            self.colors.append(self.topBottom[i])
            self.topBottom[i][0].frame = rotationframe
        if(colNumber==0): #leftmost column includes back face as well
            front = self.frontBack[:self.grid1]
            for cube in front: cube[0].frame = rotationframe
            self.faces += front
        elif(colNumber==self.h-1):
            #rightmost column inclubdes front face as well
            back = self.frontBack[self.grid1:]
            for cube in back: cube[0].frame = rotationframe
            self.faces += back
        return rotationframe
    
    def updateBoxes(self):
        #returns list of order of color of boxes for all faces based on rotation
        updatedList, newColor = [], []
        changingSet = set()
        newFaces = self.newFaces()
        for box in newFaces:
            #creates a set of boxes that were changed along with newColor list
            changingSet.add(box[0])
            newColor.append(box[1])
        if(self.includesSide()):
            #goes through this only if a side face is included in rotation
            self.getSideFrame(changingSet, newColor)
            newColor = self.modifyNewColor(newColor)
        i = 0
        for box in self.boxes:
        #obtains newList of boxe colors by changing all those that were rotated
        #and appending original ones for those that weren't
            if box[0] in changingSet:
                updatedList.append(newColor[i])
                i+=1 
            else:
               updatedList.append(box[1])
        return updatedList
    
    def includesSide(self):
        #checks to see if a side was rotated along with the main rotation
        if (self.keyNumber<self.rows):
            if(self.keyNumber==0 or self.keyNumber==self.rows-1):
                return True
        elif(self.rows<=self.keyNumber<self.rows+self.cols):
            colNumber = (self.keyNumber-self.rows)
            if(colNumber==0 or colNumber==self.cols-1):
                return True
        else:
            colNumber = self.keyNumber-self.rows-self.cols
            if(colNumber==0 or colNumber==self.h-1):
                return True
        return False

    @classmethod
    def testIncludesSide(cls):
        print "testing includesSide()...",
        ShapeMaker.rows = ShapeMaker.cols = ShapeMaker.h = 3
        ShapeMaker.keyNumber=3
        assert(ShapeMaker().includesSide()==True)
        ShapeMaker.keyNumber=7
        assert(ShapeMaker().includesSide()==False)
        ShapeMaker.rows = 4
        ShapeMaker.cols = 5
        ShapeMaker.h = 3
        ShapeMaker.keyNumber=3
        assert(ShapeMaker().includesSide()==True)
        ShapeMaker.keyNumber=11
        assert(ShapeMaker().includesSide()==True)
        print "passed!"
    
    def newFaces(self):
        #to get the colors in the newOrder, we have to take the inverse list
        #for some faces because the orientation of boxes is different for
        #different faces
        clr = self.colors
        if (self.rows==self.cols==self.h):
            if(self.angle==-pi/2): newFaces = self.minusFaces()
            else: newFaces = self.plusFaces()
        else:
            off, off2 = 2*self.cols, self.rows*2
            if (self.keyNumber<self.rows):
                #original order of self.colors: front, back, right, left
                #new order = back,front,left,right
                reverseFB = clr[off-1:self.cols-1:-1] + clr[self.cols-1::-1]
                reverseRL = clr[-1:off+self.h-1:-1]+clr[off+self.h-1:off-1:-1]
                newFaces = reverseFB + reverseRL
            elif(self.keyNumber<self.rows+self.cols):
                #original order: front, back, top,bottom
                #new order = back, front, bottom, top
                reverseFB =clr[off2-1:self.rows-1:-1]+clr[self.rows-1::-1]
                reverseTB =clr[-1:off2+self.h-1:-1]+clr[off2+self.h-1:off2-1:-1]
                newFaces = reverseFB + reverseTB
            else:
                #original order: right, left, top, bottom
                #new order = left, right, bottom, top
                c= self.cols
                reverseRL = clr[off2-1:self.rows-1:-1]+clr[self.rows-1::-1]
                reverseTB = clr[-1:c+off2-1:-1] + clr[off2+c-1:off2-1:-1]
                newFaces = reverseRL + reverseTB
        return newFaces

    def minusFaces(self):
        clr = self.colors
        off, off2 = 2*self.cols, 2*self.rows
        if (self.keyNumber<self.rows):
            #original order: front, back, right, left
            #new order = right,left,back,front
            reverseFB = clr[off-1:self.cols-1:-1] + clr[self.cols-1::-1]
            reverseRL = clr[off:off+self.h]+clr[off+self.h:]
            newFaces = reverseRL + reverseFB
        elif(self.keyNumber<self.rows+self.cols):
            #original order of self.colors: front, back, top,bottom
            #new order = bottom, top, front, back
            reverseFB = clr[:self.rows]+clr[self.rows:off2]
            reverseTB = clr[-1:off2+self.h-1:-1]+clr[off2+self.h-1:off2-1:-1]
            newFaces = reverseTB + reverseFB
        else:
            #original order: right, left, top, bottom
            #new order = top, bottom, left, right
            c =self.cols
            reverseRL = clr[self.rows:off2]+clr[:self.rows]
            reverseTB = clr[off2+c-1:off2-1:-1]+clr[-1:c+off2-1:-1] 
            newFaces = reverseTB + reverseRL
        return newFaces

    def plusFaces(self):
        clr = self.colors
        off, off2 = 2*self.cols, 2*self.rows
        if (self.keyNumber<self.rows):
            #original order: front, back, right, left
            #new order = left, right, front back
            off = 2*self.cols
            reverseFB =  clr[:self.cols]+clr[self.cols:off]
            reverseRL = clr[-1:off+self.h-1:-1]+clr[off+self.h-1:off-1:-1]
            newFaces = reverseRL + reverseFB
        elif(self.keyNumber<self.rows+self.cols):
            #original order of self.colors: front, back, top,bottom
            #new order = top, bottom, back, front
            reverseFB = clr[off2-1:self.rows-1:-1]+clr[self.rows-1::-1]
            reverseTB = clr[off2:off2+self.h]+clr[off2+self.h:]
            newFaces = reverseTB + reverseFB
        else:
            #original order: right, left, top, bottom
            #new order = bottom, top, left, right
            c =self.cols
            reverseRL = clr[self.rows-1::-1]+clr[off2-1:self.rows-1:-1]
            reverseTB = clr[c+off2:] +clr[off2:off2+c]
            newFaces = reverseTB + reverseRL
        return newFaces

    def getSideFrame(self, changingSet, newColor):
        if(self.rows==self.cols==self.h):
            #the side frame rotates only 90 degrees in cubes
            #the rotation fo the sideFrame differs depending on angle and face
            if (self.angle ==-pi/2):
                self.type2rot(changingSet, newColor)
            else:
                self.type1rot(changingSet, newColor)          
        
        else:
            #side face in cubiods always become the inverse as it undergoes
            #180 degree rotations
            if (self.keyNumber<self.rows):
                sideFace = self.faces[2*self.grid1+2*self.grid2:]
            elif(self.keyNumber<self.rows+self.cols):
                sideFace = self.faces[2*self.grid1+2*self.grid3:]
            else:
                sideFace = self.faces[2*self.grid2+2*self.grid3:]
            for i in xrange(len(sideFace)-1,-1,-1):
                changingSet.add(sideFace[i][0])
                newColor.append(sideFace[i][1])
                    
    def type1rot(self, changingSet, newColor):
        #this obtains the respective change in the orientation of the
        #sideFace when angle is -pi/2
        #eg, when rows = 3, orientation = 2,5,8,1,4,7,0,3,6
        faces = 4
        sideFace = self.faces[faces*self.grid1:]
        for i in xrange(self.rows-1,-1,-1):
            for index in xrange(i, self.grid1, self.rows):
                changingSet.add(sideFace[index][0])
                newColor.append(sideFace[index][1])      
                
    def type2rot(self, changingSet, newColor):
        #this obtains the respective change in the orientation of the
        #sideFace when angle is pi/2
        #eg, when rows = 3, orientaion = 6,3,0,7,4,1,8,5,2
        faces = 4
        sideFace = self.faces[faces*self.grid1:]
        start = self.grid1-self.rows
        while start<self.grid1:
            for i in xrange(start,-1,-self.rows):
                changingSet.add(sideFace[i][0])
                newColor.append(sideFace[i][1])
            start+=1
    
    def modifyNewColor(self,newColor):
        #returns newColor to the order of the boxes in self.boxes since
        #side face can come in between
        r, c, h = self.rows, self.cols, self.h
        if(self.keyNumber<self.rows):
            return newColor
        elif (self.keyNumber<self.rows+self.cols):
            sideFace = 2*r + 2*h
            #right/ left face comes before top and bottom faces
            newColor=newColor[:2*r]+newColor[sideFace:]+newColor[2*r:sideFace]
        else:
            sideFace = 2*r+2*c
            #bottom/top faces come before all others
            newColor =newColor[sideFace:] + newColor[:sideFace]
                #back face comes after one row is changed
        return newColor

    @classmethod
    def testModifyNewColor(cls):
        print "testing modifyNewColor()...",
        ShapeMaker.rows = ShapeMaker.cols = ShapeMaker.h = 2
        ShapeMaker.keyNumber=1
        assert(ShapeMaker().modifyNewColor([1,2,1,2,3,4,3,4,9,9,9,9])==
              [1, 2, 1, 2, 3, 4, 3, 4, 9, 9, 9, 9])
        ShapeMaker.keyNumber=3
        assert(ShapeMaker().modifyNewColor([1,2,1,2,3,4,3,4,9,9,9,9])==
               [1, 2, 1, 2, 9, 9, 9, 9, 3, 4, 3, 4])
        ShapeMaker.keyNumber=5
        assert(ShapeMaker().modifyNewColor([1,2,1,2,3,4,3,4,9,9,9,9])==
               [9, 9, 9, 9, 1, 2, 1, 2, 3, 4, 3, 4])
        print "passed!"

    def shuffle(self):
        if self.preStart==False:
        #doesn't allow users to shuffle cube drawn in instructions
            self.shuffleMode, mps = True, 15
            #setting shuffle mode to True ensures user can do other things
            #while shuffle is on
            while True:
                self.getRandom()
                #Does rotations based on random choice of angle and keyNumber
                if (self.keyNumber<self.rows):
                    axis = (0,1,0)
                    rotationframe = self.horizontalRotFrame()
                elif(self.keyNumber<self.rows+self.cols):
                    axis = (1,0,0)
                    rotationframe = self.frontVerticalRotFrame()
                else:
                    axis = (0,0,1)
                    rotationframe = self.sideVerticalRotFrame()
                for r in arange(0,self.angle,self.angle/mps):
                    rate(mps)
                    rotationframe.rotate(angle = self.angle/mps, axis=axis)
                self.newColors = self.updateBoxes()
                self.makeNewCube()
                if(self.shuffleMode == False): break
                #breaks out of shuffle loop if user pressed stopShuffle buttom
            self.shuffleMode = False
            self.getRotateKey()

    def getRandom(self):
        #picks a random angle and key for the 
        if(self.rows==self.cols==self.h):
            angles = [-pi/2,pi/2]
        else:
            angles = [-pi, pi]
        self.keyNumber = random.randint(0,self.rows+self.cols+self.h-1)
        #random valid key Press
        self.angle = random.choice(angles)
        #random angle to determine clockwise/anticlockwise rotation
        self.addToKeyPressed()        

    def addToKeyPressed(self):
        #based on random key selected, adds actual keyPress to the list 
        key = chr(ord('a')+self.keyNumber)
        if (self.angle==pi or self.angle==pi/2):
            #psoitive angle means uppercase key was pressed
            self.keysPressed.append(key.upper())
        else:
            #nagative angle means lowercase key was pressed
            self.keysPressed.append(key)

    def stopShuffle(self):
        #allows users to stop shuffle whenever they wish to
        self.shuffleMode = False

    def showSolution(self):
        (textPos, axis, wrongPos) = self.textPosition()
        if(self.shuffleMode): text(text="Stop Shuffle First", align = "center",
                                   pos = textPos, axis= axis)
        #user is not allowed to press solution key while shuffle is on
        else:
            self.solutionMode = True
            self.improveSolution()
            lenght, i,solutionList=len(self.keysPressed),0,self.solutionList()
            while i<lenght:
                (textPos, axis, wrongPos) = self.textPosition()
                if(self.solutionMode==False): break
                #stops showing solution if user pressed "stop solution"
                self.solutionKey = solutionList[i]
                text(text=("Press %s" % self.solutionKey), align = "center",
                     pos=textPos,color=color.white,axis = axis)
                while True:
                    key = scene.kb.getkey()
                    if key == self.solutionKey: break
                    else:
                        #displays msg that wrong key was pressed
                        wrong = text(text="Wrong Key Pressed!",align = "center",
                         pos=wrongPos ,axis = axis)
                #makes the required rotation and removes key from keysPressed
                self.rotate(self.solutionKey)
                self.keysPressed = self.keysPressed[:len(self.keysPressed)-1]
                i+=1
            self.solutionMode = False

    def textPosition(self):
        #prints the text based on the position of the camera
        posX = scene.mouse.camera.x
        posY = scene.mouse.camera.y
        posZ = scene.mouse.camera.z
        offset = 10
        #the following determines the axis of rotation for the text
        #based on the x and z position of the camera
        if(posZ>=0): x = +1 
        else: x = -1
        if(self.cols/2>posX>-self.cols/2): z=0
        elif(self.h/2>=posZ>=-self.h/2 and posZ>=0 ): z = -offset
        elif(self.h/2>=posZ>=-self.h/2 and posZ<0):  z = offset
        elif(posX>0): z = -1
        elif(posX<0): z = 1
        axis = (x,0,z)
        if(posY>0):
            textPos = (0,+self.textPos, 0)
            wrongPos = (0,+self.textPos+1, 0)
        else:
            textPos = (0,-self.textPos, 0)
            wrongPos = (0,-self.textPos-1, 0)
        return textPos, axis, wrongPos
        
    def stopSolution(self):
        #stops showing solution and deletes current showing solution key
        if self.preStart==False:
            self.solutionMode=False
            for object in scene.objects:
                if type(object)!=box:
                    object.visible=False
            if(self.showKeys==True and self.shuffleMode==False):
                #reprints rotationKeys if they were showing before
                self.drawRotationKeys()
                           
    def improveSolution(self):
        i=0
        keys = self.keysPressed
        while i<len(self.keysPressed)-1:
            #excludes last element of list as it can't be compared to next
            key = self.keysPressed[i]
            nextKey = self.keysPressed[i+1]
            if(self.rows==self.cols==self.h):
            #for cube, if the same upper and lowercase letter is pressed
            #successively, no change is made to the box
                if((key.isupper() and key.lower()==nextKey) or
                   (key.islower() and key.upper()==nextKey)):
                    self.keysPressed = keys[:i]+keys[i+2:]
                    i+=2
                else:
                    i+=1
            else:
            #for cuboid: if the same letter is pressed twice, irrespective
            #of uppercase or lowercase, the cube is not affected
                if(key==nextKey.upper() or key==nextKey.lower()):
                    self.keysPressed = keys[:i]+keys[i+2:]
                    i+=2
                else:
                    i+=1       
                
    def solutionList(self):
        #returns a list of keys to be pressed to solve the cube
        solutionList= []
        for i in xrange(len(self.keysPressed)):
            key = self.keysPressed[-1-i]
            #beggins from end of the list
            if key.isupper():
                solutionList.append(key.lower())
            else:
                solutionList.append(key.upper())
        return solutionList

    @classmethod
    def testSolutionList(cls):
        print "testing solutionList()...",
        ShapeMaker.keysPressed = ['a','d','F','e','G']
        assert(ShapeMaker().solutionList()==['g', 'E', 'f', 'D', 'A'])
        ShapeMaker.keysPressed = ['E','f','L','K','H']
        assert(ShapeMaker().solutionList()==['h', 'k', 'l', 'F', 'e'])
        ShapeMaker.keysPressed = []
        assert(ShapeMaker().solutionList()==[])
        print "passed!"
        
    def solve(self):
        #solves the cube for the user (shows the rotations)
        if(self.shuffleMode): text(text="Stop Shuffle First", align = "center",
                                   pos = (0,-self.textPos, self.h/2))
        elif(self.preStart==False):
            self.showKeys=False #doesn't show keys while solving
            self.solveMode = True
            self.solutionMode = True
            self.improveSolution()
            solutionList = self.solutionList()
            for i in xrange(len(solutionList)):
                if(self.solveMode==False or self.preStart==True): break
                #makes the desired rotation and removes last element from
                #list of keysPressed
                self.rotate(solutionList.pop(0))
                self.keysPressed = self.keysPressed[:len(self.keysPressed)-1]
            if(self.preStart==True):
                self.clearAll()
            else:
                self.drawRotationKeys()
                self.showKeys=True
                self.solutionMode = False
            
    def stopSolve(self):
        #causes the solve loop to break
        self.solveMode = False

    @classmethod
    def testAll(cls):
        ShapeMaker().testGetDivs()
        ShapeMaker().testCheckValidKeyPress()
        ShapeMaker().testGetAngle()
        ShapeMaker().testIncludesSide()
        ShapeMaker().testModifyNewColor()
        ShapeMaker().testSolutionList()

class CubeBuild(ShapeMaker):
    def __init__(self):
        scene.title="Rube-oid"
        #title for the screen window
        scene.autoscale = False
        scene.width=500
        scene.height=500
        scene.background = color.black
        dist = 50
        self.run()

    def run(self):
        self.inGame = False
        self.preStart=True
        titlePos, offset1, offset2 = 7, -4, -6
        self.rows = self.cols = self.h = 3
        self.getCube()
        text(text="15-112 Term Project:",
             align = "center", pos=(0,titlePos),color=color.white)
        text(text="RUBE-OID: Rubik's cube-oid\ngenerator and solver",
             align = "center", pos=(0,titlePos-2),color=color.white)
        text(text="Made by Richa Mohan", pos = (0,offset1),
             align = "center", color = color.blue)
        text(text="Press 'c' to continue", pos = (0,offset2),
             align = "center", color = color.green)        
        while True:
            #allows users to go through the intro and instructions
            key = scene.kb.getkey()
            if key == "c":
                self.instructions()
            elif key=="g":
                self.programInstructions()
            elif key == "s":
                self.runControls()
                   
    def instructions(self):
        self.reset()
        self.rows = self.cols = self.h = 3
        offset1, offset2, offset3, offset4 = 9, 6, -4, -8
        self.getCube() #creates a cube in the center of the instructions
        text(text="How to Use VPython",align = "center",pos = (0,offset1))
        text(text="Zoom in and out by holding down\noptions while using mouse",
             pos = (0,offset2),align = "center", color= color.green)
        text(text="Rotate objects by holding down\ncontrol while using mouse",
             pos = (0,offset3),align = "center", color= color.blue)
        text(text="TRY IT!",pos = (0,offset4+1),align = "center",
             color= color.red)
        text(text="Press 'g' if you got it", pos = (0,offset4-1),
             align = "center", color= color.red)

    def programInstructions(self):
        self.reset()
        self.preStart=True
        #user can't perfrom functions on cube while instructions are displayed
        self.rows = self.cols = self.h = 3
        offset1, offset2, offset3, offset4, height = 10, 8, 5, 3, .75
        self.getCube()
        text(text="How to Use This Program",align = "center",pos = (0,offset1))
        text(text="Select a cube or cuboid and press\nkeyboard keys to rotate",
             height = height,pos = (0,offset2),align = "center")
        text(text="Solve the cube by yourself\nor click on 'solve'",
             height = height,pos = (0,-offset3+2),align = "center")
        text(text="Shuffle Cube by pressing Shuffle/StopShuffle",
             pos = (0,offset3),align = "center", height = height)
        text(text="Click on\"Show Solutions\" to get solution steps",
             pos = (0,offset4-1),align = "center",height = height)
        text(text="Click \"reset\" to start over", pos =(0,-offset2+1),
             align = "center", height = height)
        if(self.inGame==False):
            #shows this only in intro instructions
            text(text="Press 's' to start!",pos =(0,-offset1+1),
                 align = "center")
    
    def runControls(self):
        self.reset()
        self.preStart=False
        self.inGame=True
        width = 300
        height = 500
        c = controls(x=scene.width, y = 0 ,width=width ,height = height,
                     title = "Controls", range=150)
        #makes a controller panel for the Rubik Cube Generator
        self.buttons()

    def buttons(self):
        x, y, h, w = 40, 120, 12, 60
        m1 = menu(pos=(-x,y), height = h, width = w, text="Cube")
        m1.items.append(("2x2x2", lambda: self.getFace(2)))
        m1.items.append(("3x3x3", lambda: self.getFace(3)))
        m1.items.append(("4x4x4", lambda: self.getFace(4)))
        m1.items.append(("5x5x5", lambda: self.getFace(5)))
        m1.items.append(("6x6x6", lambda: self.getFace(6)))
        m1.items.append(("7x7x7", lambda: self.getFace(7)))
        m1.items.append(("8x8x8", lambda: self.getFace(8)))
        #Adding items to the Sqaure menue for different possible square cubes
        m2 = menu(pos=(+x,y), height = h, width = w, text="Cuboid")
        m2.items.append(("2x3x4", lambda: self.getFace(2,3,4)))
        m2.items.append(("3x4x2", lambda: self.getFace(3,4,2)))
        m2.items.append(("4x4x5", lambda: self.getFace(3,4,5)))
        m2.items.append(("4x5x3", lambda: self.getFace(4,5,3)))
        m2.items.append(("4x5x6", lambda: self.getFace(4,5,6)))
        m2.items.append(("5x4x6", lambda: self.getFace(5,4,6)))
        m2.items.append(("6x5x4", lambda: self.getFace(6,5,4)))
        self.getButtons2()

    def getButtons2(self):
        #makes all the buttons in the control panel and assigns then functions
        h, h1, w = 28,38, 75
        x, y1, y2, y3, y4, y5= 40, 10, -20, -55, -90, -120
        b1 = button(pos=(-x,y1), height = h, width = w, text="Instructions",
                    action=lambda:self.programInstructions())
        b2 = button(pos=(x,y1), height = h, width =w, text="Reset",
                    action=lambda:self.reset())
        b3 = button(pos=(-x,y2), height = h, width = w, text="Shuffle",
                    action=lambda:self.shuffle())
        b4 = button(pos=(x,y2), height = h, width = w, text="Stop Shuffle",
                    action=lambda:self.stopShuffle())
        b5 = button(pos=(-x,y3), height = h1, width = w,
                    text="Show\nSolution",action=lambda:self.showSolution())
        b6 = button(pos=(+x,y3),height = h1,width =w,
                    text="Stop Showing\nSolution",
                    action=lambda:self.stopSolution())
        b7 = button(pos=(-x,y4), height = h, width =w, text="Solve",
                    action=lambda:self.solve())
        b8 = button(pos=(+x,y4), height = h, width =w, text="Stop Solve",
                    action=lambda:self.stopSolve())
        b9 = button(pos=(-x,y5), height = h, width = w, text="Remove Keys",
                    action=lambda:self.removeKeys())
        b10 = button(pos=(x,y5), height = h, width = w, text="Show Keys",
                    action=lambda:self.showKey())
       
    def reset(self):
        #user can start over by creating a new rubik's cube
        for objects in scene.objects:
            objects.visible=False
        self.keysPressed = [] #resets list of Keys Pressed
        self.rows,self.cols,self.h = 0,0,0
        #ensures that shuffle/showKeys do not work right after reset is pressed

CubeBuild()

