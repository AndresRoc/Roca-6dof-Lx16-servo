
from time import sleep; from serial import Serial;import struct
class LX16A:
  def __init__(self,Port="COM5",Baudrate=115200, Timeout= 0.001):
     self.serial = Serial(Port,baudrate=Baudrate,timeout=Timeout)
     self.serial.setDTR(1);self.TX_DELAY_TIME = 0.00002
     self.Header = struct.pack("<BB",0x55,0x55)
  def sendPacket(self,packet):
     packet1=bytearray(packet);sum=0
     for a in packet1: sum=sum+a
     fullPacket = bytearray(self.Header + packet + struct.pack("<B",(~sum) & 0xff))
     self.serial.write(fullPacket); sleep(self.TX_DELAY_TIME)
  def sendReceivePacket(self,packet,receiveSize):
     t_id = pa
     cket[0];t_command = packet[2]
     self.serial.flushInput();self.serial.timeout=0.1;self.sendPacket(packet)
     r_packet = self.serial.read(receiveSize+3); return r_packet 
  def motorOrServo(self,id,motorMode,MotorSpeed):
     packet = struct.pack("<BBBBBh",id,7,29,motorMode,0,MotorSpeed)
     self.sendPacket(packet)# motorMode 1=motor MotorSpeed=rate, 2=servo 
  def moveServo(self,id,position,rate=1000):
     packet = struct.pack("<BBBHH",id,7,1,position,rate)
     self.sendPacket(packet)  # Move servo 0-1000, rate(ms) 0-30000(slow)
  def readPosition(
  	self,id):
     packet = struct.pack("<BBB",id,3,28)
     rpacket = self.sendReceivePacket(packet,5)
     s = struct.unpack("<BBBBBhB",rpacket);return s[5] 
  def LoadUnload(self,id,mode):
     packet = struct.pack("<BBBB",id,4,31,mode)
     self.sendPacket(packet)#Activate motor 0=OFF 1 =Active
  def setID(self,id,newid):# change the ID of servo
     packet = struct.pack("<BBBB",id,4,13,newid)
     self.sendPacket(packet)
  def moveservos(self,speed,n, s1,s2,s3,s4,s5,s6):
     self.moveServo(1,n[0]+s1,speed);self.moveServo(2,n[1]+s2,speed)
     self.moveServo(3,n[2]+s3,speed);self.moveServo(4,n[3]+s4,speed)
     self.moveServo(5,n[4]+s5,speed);self.moveServo(6,n[5]+s6,speed)
  def readservosABS(self):
    m=[0]*6
    for a in range(0,6): m[a]= self.readPosition(a+1)
    return m
  def readservos(self, c):
    m=[0]*6
    for a in range(0,6): m[a]= self.readPosition(a+1)-c[a]
    return m
  def servosoff(self):
    for a in range(1,7): self.LoadUnload(a,0)
  def servoson(self):
    for a in range(1,7): self.LoadUnload(a,1)
  def close(self):
    self.serial.close()
    #123 left 456 right
if __name__ == '__main__':
   m1 = LX16A() # creat a servo class object
   n = (227, 146, 185, 364, 274, 387) #define the neutral position
   m1.moveservos(1000 ,n ,0 ,0, 0, 0, 0, 0) #set ther servos to the netral position 
   r=input ("First position")
   while True:
     m1.moveservos(1000, n, 0, 0, 0, 0, 0, 0)#balance on one leg
     sleep(0.1)
     r=input ("0")
     m1.moveservos(1000, n, 100, 0, 0, 0, 0, 0)
     r=input ("90")
     m1.moveservos(1000, n, 100, 100, 0, 0, 0, 0)#move the leg
     r=input ("20")
     m1.moveservos(1000, n, 100, 200, 100, 0, 0, 0)    
     r=input ("50")
     m1.moveservos(1000, n, 0, 0, 0, 250, 0, 0) # back to the neutral position
     r=input ("150")

   m1.close()     

   