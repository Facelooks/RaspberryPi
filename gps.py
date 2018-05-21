#$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47
#
#Where:
#GGA          Global Positioning System Fix Data
#     123519       Fix taken at 12:35:19 UTC
#     4807.038,N   Latitude 48 deg 07.038' N
#     01131.000,E  Longitude 11 deg 31.000' E
#     1            Fix quality: 0 = invalid
#                               1 = GPS fix (SPS)
#                               2 = DGPS fix
#                               3 = PPS fix
#			                    4 = Real Time Kinematic
#			                    5 = Float RTK
#                               6 = estimated (dead reckoning) (2.3 feature)
#			                    7 = Manual input mode
#			                    8 = Simulation mode
#     08           Number of satellites being tracked
#     0.9          Horizontal dilution of position
#     545.4,M      Altitude, Meters, above mean sea level
#     46.9,M       Height of geoid (mean sea level) above WGS84
#                      ellipsoid
#     (empty field) time in seconds since last DGPS update
#     (empty field) DGPS station ID number
#     *47          the checksum data, always begins with *



#$GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A
#
#Where:
#     RMC          Recommended Minimum sentence C
#     123519       Fix taken at 12:35:19 UTC
#     A            Status A=active or V=Void.
#     4807.038,N   Latitude 48 deg 07.038' N
#     01131.000,E  Longitude 11 deg 31.000' E
#     022.4        Speed over the ground in knots
#     084.4        Track angle in degrees True
#     230394       Date - 23rd of March 1994
#     003.1,W      Magnetic Variation
#     *6A          The checksum data, always begins with *

GGA_FIXTIME = 1
GGA_LAT = 2
GGA_LONG = 4
GGA_QUAL = 6
GGA_SATNUM = 7
GGA_DILU = 8
GGA_ALT = 9
GGA_HEIGHT = 11
GGA_SECUPD = 13

RMC_FIXTIME = 1
RMC_STAT = 2
RMC_LAT = 3
RMC_LOG = 5
RMC_SPEED = 7
RMC_ANGLE = 8
RMC_DATE = 9

import serial
from threading import Thread

class gps(object):
    
    def start(self,serialPort):
        self.__GGA = []
        self.__RMC = []
        self.t = Thread(target=self.__start_handle, args=(serialPort,))
        self.t.start()
        
        
    def __start_handle(self,serialPort):
        self.ser = serial.Serial()
        self.ser.baudrate = 9600
        self.ser.port = serialPort
        self.ser.open()
        while True:
            self.__decodeNmea(self.ser.readline().decode())
                    
    def __decodeNmea(self, data):
        if data[0:6] == "$GPGGA":
           self.__GGA = data.split(",")
        if data[0:6] == "$GPRMC":
            self.__RMC = data.split(",")
    
    def getFixTime(self):
        try:
            return self.__GGA[GGA_FIXTIME]
        except:
            return "NO DATA"

    def getLatitude(self):
        try:
            return self.__GGA[GGA_LAT]
        except:
            return "NO DATA"

    def getLongitude(self):
        try:
            return self.__GGA[GGA_LONG]
        except:
            return "NO DATA"
        
    def getSatellites(self):
        try:
            return self.__GGA[GGA_SATNUM]
        except:
            return "NO DATA"

    def getAltitude(self):
        try:
            return self.__GGA[GGA_ALT]
        except:
            return "NO DATA"

    def getDate(self):
        try:
            return self.__RMC[RMC_DATE]
        except:
            return "NO DATA"
        
        

######################## INIT GPS ############################

import time

gps =gps()

gps.start('/dev/serial0')
#time.sleep(3)
while True:
    print("Altitude: {}m".format(gps.getAltitude()))
    print("Date: {}".format(gps.getDate()))
    print("Satellites: {}".format(gps.getSatellites()))
    print()
    time.sleep(1)
    