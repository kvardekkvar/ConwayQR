import qrcode
import numpy
import subprocess
import time 

LIVE = 0
DEAD = 1
LIVECHAR = "*"
DEADCHAR = " "
FIELD_SIZE = 29

class Conway():

    def __init__(self, initial_array):
        self.array  = initial_array
        self.newarray = initial_array.copy()


    def print_array(self):

        for i in range(FIELD_SIZE):
            string = ""
            for j in range(FIELD_SIZE):
                if self.array[i,j] == LIVE:
                    string += LIVECHAR
                else:
                    string += DEADCHAR
            
            #setting cursor to i-th row
            string = ("\033[%d;0H%s") % (i, string)
            
            subprocess.run(["echo", "", string])
       #time.sleep(0.1)   
        
        
    @staticmethod
    def neighbours(x, y):
        result = [[x-1, y-1], [x-1,y], [x-1,y+1], [x,y-1], [x, y+1], [x+1, y-1], [x+1, y], [x+1, y+1]]
        for cell in result.copy():
            if cell[0]<0 or cell[0]>=FIELD_SIZE or cell[1]<0 or cell[1]>=FIELD_SIZE:
                result.remove(cell)
        return result
                
         
        
    def live_neighbours(self, i, j):
        neighbours= self.neighbours(i, j)
        count = 0
        for cell in neighbours:
            x = cell[0]
            y = cell[1]
            if self.array[x, y] == LIVE:
                count += 1
        return count

    def compute_new_cell(self, i, j):
        cell = self.array[i,j]
        newcell = self.newarray[i,j]
        neighbours = self.live_neighbours(i, j)

        if cell == LIVE and neighbours in [2,3]:
            newcell = LIVE
        elif cell == DEAD and neighbours == 3:
            newcell = LIVE
        else:
            newcell = DEAD
        self.newarray[i,j] = newcell
        
        
    def step(self):
        self.print_array()

        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                self.compute_new_cell(i,j)
        self.array, self.newarray = self.newarray, self.array
        
    def run(self):
        while True:
            self.step()            


text = input("Input QR code content: ")

qr_code = qrcode.QRCode(version=1, box_size=1)
qr_code.add_data(text)
qr_code.make(fit=True)

img = qr_code.make_image()

qr_array = numpy.array(img, dtype = numpy.int32)

for i in range(FIELD_SIZE):
    print("")
    
Conway(qr_array).run()

