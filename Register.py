import serial
import time
import datetime
import MySQLdb
import MFRC522
import RPi.GPIO as GPIO
from pyfingerprint.pyfingerprint import PyFingerprint

db = MySQLdb.connect(host="172.37.40.40", user="root", passwd="password", db="rfid")
curs= db.cursor()
#ser=serial.Serial('/dev/ttyACM1', 9600)

def fingerscan ():
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        exit(1)

    

    ## Tries to enroll new finger
    try:
        print('Waiting for finger...')

        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

    ## Checks if finger is already enrolled
        result = f.searchTemplate()
        positionNumber = result[0]

        if ( positionNumber >= 0 ):
            print('Template already exists at position #' + str(positionNumber))
            exit(0)

        print('Remove finger...')
        time.sleep(2)

        print('Waiting for same finger again...')

        ## Wait that finger is read again
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 2
        f.convertImage(0x02)

        ## Compares the charbuffers
        if ( f.compareCharacteristics() == 0 ):
            raise Exception('Fingers do not match')

        ## Creates a template
        f.createTemplate()

        ## Saves template at new position number
        positionNumber = f.storeTemplate()
    
        print('Finger enrolled successfully!')
        
    
        f.loadTemplate(positionNumber, 0x01)
        char_store = str (f.downloadCharacteristics(0x01))
        char_store1= char_store.translate(None, ',[]')
    
        return positionNumber, char_store1
        
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)
      
def main ():
    #GPIO.setmode(GPIO.BCM)
    print("Type DONE to exit!")
    status=" kosong" 
    while (status!='DONE'):
        status=raw_input("Enter Status  : ")
        if(status=='Mahasiswa'):
            nama=raw_input ("Enter Name    : ")
            nim=raw_input  ("Enter Nim     : ")
            kelas=raw_input("Enter Class   : ")
            print('Scan RFID Card!')
            MIFAREReader = MFRC522.MFRC522()
            (status1,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
            (status1,uid) = MIFAREReader.MFRC522_Anticoll()
            while status1 != MIFAREReader.MI_OK :
                MIFAREReader = MFRC522.MFRC522()
                (status1,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
                (status1,uid) = MIFAREReader.MFRC522_Anticoll()       
            if status1 == MIFAREReader.MI_OK:
                rt_rfid = str (uid)
                read_rfid = rt_rfid.translate(None, ',[] ')
                print('ID  RFID      : %s' %read_rfid)
                result=fingerscan()
                id_finger=result[0]
                print('ID Fingerprint: %i' %id_finger)
                print(' \n')
                templ_finger=result[1]
                curs.execute("INSERT INTO user (rfid, nomor_induk, status, nama, id_finger, temp_finger) VALUES ('%s', '%s', '%s', '%s', '%i', '%s')" %(read_rfid, nim, status, nama, id_finger, templ_finger )) 
                curs.execute("INSERT INTO Mahasiswa(rfid, id_finger, Nama, Nim, Class)VALUES ('%s', '%i', '%s', '%s', '%s')" %(read_rfid, id_finger, nama, nim, kelas))
                db.commit()
        else :
            nama=raw_input ("Enter Name    : ")
            nidn=raw_input ("Enter Nidn    : ")
            matkul1=raw_input("Enter Subject : ")
            matkul2=raw_input("Enter Subject : ")
            matkul3=raw_input("Enter Subject : ")
            matkul4=raw_input("Enter Subject : ")
            print('Scan RFID Card!')
            MIFAREReader = MFRC522.MFRC522()
            (status1,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
            (status1,uid) = MIFAREReader.MFRC522_Anticoll()
            while status1 != MIFAREReader.MI_OK :
                MIFAREReader = MFRC522.MFRC522()
                (status1,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
                (status1,uid) = MIFAREReader.MFRC522_Anticoll()
            if status1 == MIFAREReader.MI_OK:
                rt_rfid = str (uid)
                read_rfid = rt_rfid.translate(None, ',[] ')
                print('ID  RFID      : %s' %read_rfid)
                result=fingerscan()
                id_finger=result[0]
                print('ID Fingerprint: %i' %id_finger)
                print(' \n')
                templ_finger=result[1]
                curs.execute("INSERT INTO user (rfid, nomor_induk, status, nama, id_finger, temp_finger) VALUES ('%s', '%s', '%s', '%s', '%i', '%s')" %(read_rfid, nidn, status, nama, id_finger, templ_finger )) 
                curs.execute("INSERT INTO Dosen (rfid, id_finger, nidn, Nama, matakuliah1, matakuliah2, matakuliah3, matakuliah4) VALUES ('%s', '%i', '%s', '%s', '%s', '%s', '%s', '%s')" %(read_rfid, id_finger, nidn, nama, matkul1, matkul2, matkul3, matkul4 )) 
                db.commit()

    status=raw_input("Enter Status  : ")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print "Goodbye!"
        #lcd_byte(0x01, LCD_CMD)
        #lcd_string("Goodbye!",LCD_LINE_2,2)
        GPIO.cleanup()
