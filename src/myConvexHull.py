import numpy as np

#Main Function:
#Find dot at extreme left and extreme right
#Using Func SplitTwo splits arr_of_dots into upperpart and lowerpart
#Uses 2 instances of Func ConvexHull2 to find the convexhull of the upper part and lowerpart
#Returns the combined result of top convexhull2 and bottom convexhull2, creating Convexhull
#Final Return structure Example [[dot1],[dot2],[dot2],[dot2],[dot3],[dot4],[dot4],[dot5],[dot5],[dot1]] 
#Tip: Connect pairs of 2 dots to make a line
#Example: dot1 to dot2, dot2 to dot3, dot3 to dot4, dot4 to dot5, dot5 to dot1 to make the full convexhull
def CONVEXHULL(arr_of_dots): 
    min_index_col = np.argmin(arr_of_dots, axis=0)[0]
    max_index_col = np.argmax(arr_of_dots, axis=0)[0]

    mindot = arr_of_dots[min_index_col]
    maxdot = arr_of_dots[max_index_col]
    
    upperpart,lowerpart = SplitTwo(mindot,maxdot,arr_of_dots)

    Convex = []
    for x in (ConvexHull2(mindot,maxdot,upperpart,True)):
        Convex.append(x)
    for x in (ConvexHull2(mindot,maxdot,lowerpart,False)):
        Convex.append(x)
    return Convex

#Using Func findfurthest finds point furthest from line of mindot and maxdot 
#And then using Func Split split arr_of_dots into 2 areas based on bool (True means takes upper part, False means take bottom part)
#And then recursively calls itself with the parameters of 2/3 dots and the split parts.
#Returns the mindot and maxdot when arr_of_dots is empty
#After all recursions are done: Returns all of the dots that make up the convex
#Final Return structure Example [[dot1],[dot2],[dot2],[dot2],[dot3],[dot4]] 
#Tip: Connect pairs of 2 dots to make a line
#Example: dot1 to dot2, dot2 to dot3, dot3 to dot4 to make a half finished perimeter
#The other convexhull2 will make the second half of the perimeter and combined will make the convex hull
def ConvexHull2(mindot,maxdot,arr_of_dots,bool):
    if(arr_of_dots.size != 0):
        maxdistancedot = FindFurthest(mindot,maxdot,arr_of_dots)
        
        part = Split(mindot,maxdistancedot,arr_of_dots,bool)
        part2  = Split(maxdistancedot,maxdot,arr_of_dots,bool)

        Convex = []
        for x in (ConvexHull2(mindot,maxdistancedot,part,bool)):
            Convex.append(x)
        for x in (ConvexHull2(maxdistancedot,maxdot,part2,bool)):
            Convex.append(x)
        return Convex
    else:
        return maxdot.tolist(),mindot.tolist()

#find the dot furthest from the line made by mindot and maxdot from arr_of_dots
def FindFurthest(mindot,maxdot,arr_of_dots):
    x1 = mindot[0]
    y1 = mindot[1]
    x2 = maxdot[0]
    y2 = maxdot[1]

    b = -(x2-x1)            #find a, b, c created by mindot and maxdot
    a = y2-y1
    c = -a * x1 - b*y1

    max_dist = 0
    maxangle = 0
    for dots in arr_of_dots:
        x3 = dots[0]
        y3 = dots[1]

        dist = abs(a * x3 + b * y3 + c) #check distance of dot to line, Note: division by sqrt(a^2+b^2) is not needed because it is a constant

        if dist > max_dist :        #if dot's distance is further than  maxdot, replace maxdot and  maxangle 
            max_dist = dist
            maxdistancedot = dots
            d12 = np.sqrt((x1-x2)**2 + (y1-y2)**2)
            d13 = np.sqrt((x1-x3)**2 + (y1-y3)**2)
            d23 = np.sqrt((x3-x2)**2 + (y3-y2)**2)
            maxangle = np.arccos((d13*d13 + d23*d23 - d12*d12)/(2*d13*d23))
        elif(dist == max_dist):     #if dot is same distance than maxdot, compare angle and maxangle. Replace maxdot and maxangle if new angle > maxangle
            d12 = np.sqrt((x1-x2)**2 + (y1-y2)**2)
            d13 = np.sqrt((x1-x3)**2 + (y1-y3)**2)
            d23 = np.sqrt((x3-x2)**2 + (y3-y2)**2)
            angle = np.arccos((d13*d13 + d23*d23 - d12*d12)/(2*d13*d23))
            if(angle > maxangle):
                max_dist = dist
                maxdistancedot = dots
                maxangle = angle
    return maxdistancedot

#Split arr_of_dots into two parts (top and bottom) and returns array of dots of top and bottom parts
def SplitTwo(mindot,maxdot,arr_of_dots):
    x1 = mindot[0]
    y1 = mindot[1]
    x2 = maxdot[0]
    y2 = maxdot[1]
    
    upperpart = np.array([])
    lowerpart = np.array([])

    for dots in arr_of_dots:
        x3 = dots[0]
        y3 = dots[1]
        det = round(((x1*y2)+(x3*y1)+(x2*y3)-(x3*y2)-(x2*y1)-(x1*y3)),10)   #det is rounded to 10 because float multiplication 
                                                                            #sometimes has a residue 0.000000000001, causing problems
        if(det > 0):                                        #toppart             
            if upperpart.size == 0:
                upperpart = np.array([dots])
            upperpart = np.vstack([upperpart,dots])
        elif(det < 0):                                      #bottompart
            if lowerpart.size == 0:
                lowerpart = np.array([dots])
            lowerpart = np.vstack([lowerpart,dots])
    return upperpart, lowerpart

#Split arr_of_dots based on mindot and maxdot line
#bool True means take arr_of_dots which are located above of mindot&maxdot line
#bool False means take arr_of_dots which are located below of mindot&maxdot line
def Split(mindot,maxdot,arr_of_dots,bool):
    x1 = mindot[0]
    y1 = mindot[1]
    x2 = maxdot[0]
    y2 = maxdot[1]
    
    part = np.array([])

    if bool:                            #Bool = True
        for dots in arr_of_dots:
            x3 = dots[0]
            y3 = dots[1]
            det = round(((x1*y2)+(x3*y1)+(x2*y3)-(x3*y2)-(x2*y1)-(x1*y3)),10)
            if(det > 0):                        #toppart
                if part.size == 0:
                    part = np.array([dots])
                else:
                    part = np.vstack([part,dots])
    else:                                #Bool = False
        for dots in arr_of_dots:
            x3 = dots[0]
            y3 = dots[1]
            det = round(((x1*y2)+(x3*y1)+(x2*y3)-(x3*y2)-(x2*y1)-(x1*y3)),10)
            if(det < 0):                        #bottompart
                if part.size == 0:
                    part = np.array([dots])
                else:
                    part = np.vstack([part,dots])
    return part