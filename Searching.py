import serial
import time
import datetime
import MySQLdb
import MFRC522
import Adafruit_GPIO.SPI as SPI
from pyfingerprint.pyfingerprint import PyFingerprint
#from datetime import datetime

from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
# Define GPIO to LCD mapping
LCD_RS = 7
LCD_E  = 16
LCD_D4 = 22
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18
#LED_ON = 15
 
# Define some device constants
LCD_WIDTH = 20    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
 
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line
 
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) #tombol1
GPIO.setup(13,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) #tombol2
GPIO.setup(6,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) #tombol3
GPIO.setup(5,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)  #tombol4
GPIO.setup(12,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) #tombol_OK
GPIO.setup(19,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) #tombol update
GPIO.setup(21,GPIO.OUT) #BUZZER

db = MySQLdb.connect(host="172.37.40.40", user="root", passwd="password", db="rfid")
curs= db.cursor()

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)
 
def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command
 
  GPIO.output(LCD_RS, mode) # RS
 
  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)
 
def lcd_string(message,line,style):
  # Send string to display
  # style=1 Left justified
  # style=2 Centred
  # style=3 Right justified
 
  if style==1:
    message = message.ljust(LCD_WIDTH," ")
  elif style==2:
    message = message.center(LCD_WIDTH," ")
  elif style==3:
    message = message.rjust(LCD_WIDTH," ")
 
  lcd_byte(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
 



    
def tampilayar(data1,data2):
    lcd_byte(0x01, LCD_CMD)
    lcd_string("WELCOME",LCD_LINE_1,2)
    lcd_string("Ruangan 715",LCD_LINE_2,2)
    lcd_string(data2,LCD_LINE_3,2)
    lcd_string(data1,LCD_LINE_4,2)
 
    time.sleep(2) # 2 second delay
 
    # Blank display
    #lcd_byte(0x01, LCD_CMD)


def tampilayardosen(ntemp,data1,data2,data3,data4):
    today= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    str(today)
    GPIO.input(26)==0
    GPIO.input(13)==0
    GPIO.input(6)==0
    GPIO.input (5)==0
    GPIO.input (12)==0
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Choose",LCD_LINE_2,2)
    lcd_string("Your Subject!",LCD_LINE_3,2)
    #lcd_string("Subject!",LCD_LINE_4,2)
    time.sleep(1.5)
    
    #draw.text((0,8), 'CHOOSE!', font=font)
    lcd_string("1."+data1,LCD_LINE_1,1)
    lcd_string("2."+data2,LCD_LINE_2,1)
    lcd_string("3."+data3,LCD_LINE_3,1)
    lcd_string("4."+data4,LCD_LINE_4,1)

    ruang = "GD715"
    while( GPIO.input(12)!=1):
        if GPIO.input(26):
            curs.execute("INSERT INTO Log (nama, datetime, ruangan, matakuliah) VALUES ('%s', '%s', '%s', '%s')" %(ntemp, today, ruang, data1))
            print "26 masuk"
            db.commit()
            sleep(.2)
                
        elif GPIO.input(13):
            curs.execute("INSERT INTO Log (nama, datetime, ruangan, matakuliah) VALUES ('%s', '%s', '%s', '%s')" %(ntemp, today, ruang, data2))
            print "13 masuk"
            db.commit()
            sleep(.2)
                
        elif GPIO.input(6):
            curs.execute("INSERT INTO Log (nama, datetime, ruangan, matakuliah) VALUES ('%s', '%s', '%s', '%s')" %(ntemp, today, ruang, data3))
            print "6 masuk"
            db.commit()
            sleep(.2)
                
        elif GPIO.input(5):
            curs.execute("INSERT INTO Log (nama, datetime, ruangan, matakuliah) VALUES ('%s', '%s', '%s', '%s')" %(ntemp, today, ruang, data4))
            print "5 masuk"
            db.commit()
            sleep(.2)
        else:
            pass


def main():
    #MIFAREReader = MFRC522.MFRC522()
    GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
    GPIO.setup(LCD_E, GPIO.OUT)  # E
    GPIO.setup(LCD_RS, GPIO.OUT) # RS
    GPIO.setup(LCD_D4, GPIO.OUT) # DB4
    GPIO.setup(LCD_D5, GPIO.OUT) # DB5
    GPIO.setup(LCD_D6, GPIO.OUT) # DB6
    GPIO.setup(LCD_D7, GPIO.OUT) # DB7
    lcd_init()         

    while (True):
        MIFAREReader = MFRC522.MFRC522()
        lcd_string("ATTENDANCE SYSTEM",LCD_LINE_1,2)
        lcd_string("TA-2 ELEKTRO 2014",LCD_LINE_4,2)
        #today= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rdy = datetime.datetime.now().strftime("%b %d %Y")
        #str(today)
        clk= datetime.datetime.now().strftime("%H:%M:%S")
        lcd_string(rdy,LCD_LINE_2,2)
        lcd_string(clk,LCD_LINE_3,2) 
        if GPIO.input(19):
            lcd_byte(0x01, LCD_CMD)
            lcd_string("UPDATING..",LCD_LINE_2,2)
            try:
                f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

                if ( f.verifyPassword() == False ):
                    raise ValueError('The given fingerprint sensor password is wrong!')

            except Exception as e:
                print('The fingerprint sensor could not be initialized!')
                print('Exception message: ' + str(e))


            ## Tries to delete the template of the finger
            try:
                
                curs.execute ("SELECT max(id_finger)FROM user")
                maks=curs.fetchone()
                y=maks[0]
                print y
                for x in range (0,y):
                    curs.execute("SELECT temp_finger FROM user WHERE id_finger = ('%i')" %x)
                    temp = curs.fetchone()
                    t_temp=temp[0]
                    t1_temp=t_temp.split()
                    t2_temp=list (map (int, t1_temp))
                    f.uploadCharacteristics(0x01,t2_temp)
                    f.storeTemplate(x,0x01 )
                    db.commit()
                
            except Exception as e:
                print('Operation failed!')
                print('Exception message: ' + str(e))
                lcd_byte(0x01, LCD_CMD)
                print('Duplicated Data')    
                lcd_string("Duplicated Data",LCD_LINE_2,2)
                lcd_string("Please Contact",LCD_LINE_3,2)
                lcd_string("Administrator",LCD_LINE_4,2)
                print('Exception message: ' + str(e))
                time.sleep(2)   
                lcd_byte(0x01, LCD_CMD)
                    
        try:
            (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
            if status == MIFAREReader.MI_OK:
                (status,uid) = MIFAREReader.MFRC522_Anticoll()
                if status == MIFAREReader.MI_OK:
                
                    lcd_byte(0x01, LCD_CMD)
                    rt_rfid = str (uid)
                    rt_rfid1 = rt_rfid.translate(None, ',[] ')
                    print rt_rfid1
    
                    curs.execute("SELECT status FROM user WHERE rfid = ('%s')" %rt_rfid1)
                    status_1 = curs.fetchone()
                    t_stat=status_1[0]
                    print t_stat
                    GPIO.output(21, True)
                    time.sleep(.085)
                    GPIO.output(21, False)
                    if(t_stat == "Dosen"):
                        curs.execute("SELECT Nama FROM Dosen  WHERE rfid = ('%s')" %rt_rfid1)
                        nama = curs.fetchone()    
                        ntemp = nama[0]
                        print ntemp
                        #print today
                        curs.execute("SELECT matakuliah1 FROM Dosen  WHERE rfid = ('%s')" %rt_rfid1)
                        matkul1 = curs.fetchone()
                        t_matkul1 = matkul1[0]
                        curs.execute("SELECT matakuliah2 FROM Dosen  WHERE rfid = ('%s')" %rt_rfid1)
                        matkul2 = curs.fetchone()
                        t_matkul2 = matkul2[0]
                        curs.execute("SELECT matakuliah3 FROM Dosen  WHERE rfid = ('%s')" %rt_rfid1)
                        matkul3 = curs.fetchone()
                        t_matkul3 = matkul3[0]
                        curs.execute("SELECT matakuliah4 FROM Dosen  WHERE rfid = ('%s')" %rt_rfid1)
                        matkul4 = curs.fetchone()
                        t_matkul4 = matkul4[0]
                        tampilayar(ntemp,clk)
                        print "Memilih matakuliah"
                        tampilayardosen(ntemp, t_matkul1, t_matkul2, t_matkul3, t_matkul4)
                        print "Data sudah masuk"
                        lcd_byte(0x01, LCD_CMD)
                        lcd_string("DATA RECORDED",LCD_LINE_2,2) 
                        time.sleep(1)
                        lcd_byte(0x01, LCD_CMD)
        
                    else:
                        today= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        str(today)
                        curs.execute("SELECT nama FROM user  WHERE rfid = ('%s')" %rt_rfid1)
                        nama = curs.fetchone()    
                        ntemp = nama[0]
                        print ntemp
                        print today
                        ruang = "GD715"
                        mat="-"
                        tampilayar(ntemp,clk)
                        curs.execute("INSERT INTO Log (nama, datetime, ruangan, matakuliah) VALUES ('%s', '%s', '%s', '%s')" %(ntemp, today, ruang, mat))
                        db.commit()
                        lcd_byte(0x01, LCD_CMD)
                        
        except Exception as e:
            GPIO.output(21, True)
            time.sleep(.075)
            GPIO.output(21, False)
            time.sleep(.045)
            GPIO.output(21, True)
            time.sleep(.075)
            GPIO.output(21, False)
            time.sleep(.045)
            GPIO.output(21, True)
            time.sleep(.075)
            GPIO.output(21, False)
            lcd_byte(0x01, LCD_CMD)
            print('RFID belum didaftar!!!')    
            lcd_string("COBA LAGI",LCD_LINE_2,2)
            print('Exception message: ' + str(e))
            time.sleep(2)   
            lcd_byte(0x01, LCD_CMD)
    
        try:
            f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

            if ( f.verifyPassword() == False ):
                raise ValueError('The given fingerprint sensor password is wrong!')

        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))
        
    #while ( f.readImage() == False ):
     #       pass
        try:
            key= f.readImage()
            if (key != False ):
    ## Converts read image to characteristics and stores it in charbuffer 1
                f.convertImage(0x01)

    ## Searchs template
                result = f.searchTemplate()

                positionNumber = result[0]
    
                lcd_byte(0x01, LCD_CMD)
                curs.execute("SELECT status FROM user WHERE id_finger= ('%s')" %positionNumber)
                status = curs.fetchone()
                t_stat=status[0]
                print t_stat
                GPIO.output(21, True)
                time.sleep(.085)
                GPIO.output(21, False)
                ruang = "GD715"
                if(t_stat == "Dosen"):
                    curs.execute("SELECT Nama FROM Dosen  WHERE id_finger = ('%s')" %positionNumber)
                    nama = curs.fetchone()    
                    ntemp = nama[0]
                    print ntemp
                    #print today
                    curs.execute("SELECT matakuliah1 FROM Dosen  WHERE id_finger = ('%s')" %positionNumber)
                    matkul1 = curs.fetchone()
                    t_matkul1 = matkul1[0]
                    curs.execute("SELECT matakuliah2 FROM Dosen  WHERE id_finger = ('%s')" %positionNumber)
                    matkul2 = curs.fetchone()
                    t_matkul2 = matkul2[0]
                    curs.execute("SELECT matakuliah3 FROM Dosen  WHERE id_finger = ('%s')" %positionNumber)
                    matkul3 = curs.fetchone()
                    t_matkul3 = matkul3[0]
                    curs.execute("SELECT matakuliah4 FROM Dosen  WHERE id_finger = ('%s')" %positionNumber)
                    matkul4 = curs.fetchone()
                    t_matkul4 = matkul4[0]
                    tampilayar(ntemp,clk)
                    print "Memilih matakuliah"
                    tampilayardosen(ntemp, t_matkul1, t_matkul2, t_matkul3, t_matkul4)
                    print "Data sudah masuk"
                    lcd_byte(0x01, LCD_CMD)
                    lcd_string("DATA RECORDED",LCD_LINE_2,2) 
                    time.sleep(1)
                    lcd_byte(0x01, LCD_CMD)
        
                else:
                    today= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    str(today)
                    curs.execute("SELECT nama FROM user  WHERE id_finger = ('%s')" %positionNumber)
                    nama = curs.fetchone()    
                    ntemp = nama[0]
                    print ntemp
                    print today
                    mat="-"
                    tampilayar(ntemp,clk)
                    curs.execute("INSERT INTO Log (nama, datetime, ruangan, matakuliah) VALUES ('%s', '%s', '%s', '%s')" %(ntemp, today, ruang, mat))
                    db.commit()
                    lcd_byte(0x01, LCD_CMD)
      
        except Exception as e:
            GPIO.output(21, True)
            time.sleep(.075)
            GPIO.output(21, False)
            time.sleep(.045)
            GPIO.output(21, True)
            time.sleep(.075)
            GPIO.output(21, False)
            time.sleep(.045)
            GPIO.output(21, True)
            time.sleep(.075)
            GPIO.output(21, False)
            print('Fingerprint belum didaftar!!!')    
            lcd_string("COBA LAGI",LCD_LINE_2,2)
            print('Exception message: ' + str(e))
            time.sleep(2)   
            lcd_byte(0x01, LCD_CMD)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(0x01, LCD_CMD)
        lcd_string("Goodbye!",LCD_LINE_2,2)
        GPIO.cleanup()
