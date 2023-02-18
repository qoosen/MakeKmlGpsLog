## Make KML file from Race track GPS log by qoosen
## For TSUKUBA circuit TC2000
## https://github.com/qoosen/MakeKmlGpsLog
## File:MakeKmlGpsLog001.py

def LogFileRead():
    # Definition of KML file Header,Footer / KMLファイルのヘッダーとフッター部分の定義
    HeadCom = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<kml xmlns="http://earth.google.com/kml/2.2">\n<Document>\n<Style id="trace">\n<LineStyle>\n<color>ffff0000</color>\n<width>4</width>\n</LineStyle>\n</Style>\n'
    HeadCom2 = '<Placemark>\n<name>Lap-1</name>\n<styleUrl>#trace</styleUrl>\n<LineString>\n<coordinates>\n'
    FootCom = '</coordinates>\n</LineString>\n</Placemark>\n</Document>\n</kml>'

    first = True                            #1st calcuration / 初回計算フラグ
    Lap = -1                                #Lap initialization / Lap初期化
    LongitudeKmlComp = 0                   #Longitude compensation / 東経補正値(Not in use case:0/補正を使用しない場合は0)
    LatitudeKmlComp = 0                    #Latitude compensation / 北緯補正値(補正を使用しない場合は0)
    ###LongitudeKmlComp = -0.000041466 
    ###LatitudeKmlComp = 0.000057951 
    Sector1StartPoint1 = [139.91930,36.15020]   #Sector1 start line(Start line) point1 [Longitude,Latitude]/ セクター1(スタートライン)の点1 東経,北緯
    Sector1StartPoint2 = [139.91982,36.15011]   #Sector1 start line(Start line) point2 [Longitude,Latitude]/ セクター1(スタートライン)の点2 東経,北緯
    Sector2StartPoint1 = [139.92052,36.15013]   #Sector2 start line point1 [Longitude,Latitude]/ セクター2開始線の点1 東経,北緯
    Sector2StartPoint2 = [139.92095,36.15007]   #Sector2 start line point2 [Longitude,Latitude]/ セクター2開始線の点2 東経,北緯
    Sector3StartPoint1 = [139.92161,36.14971]   #Sector3 start line point1 [Longitude,Latitude]/ セクター3開始線の点1 東経,北緯
    Sector3StartPoint2 = [139.92208,36.14942]   #Sector3 start line point2 [Longitude,Latitude]/ セクター3開始線の点1 東経,北緯

    Sec1TimMn = 0
    Sec1TimSc = 0

    LinerSector1Start = LinerEquation(Sector1StartPoint1,Sector1StartPoint2)
    LinerSector2Start = LinerEquation(Sector2StartPoint1,Sector2StartPoint2)
    LinerSector3Start = LinerEquation(Sector3StartPoint1,Sector3StartPoint2)
    #Open file / ファイルを開く
    LogData = open("TC2000.log", "r")       #GPSレシーバーログファイルをオープン
    KmlData = open("TC2000tmp.kml", "w")       #KMLファイルをオープン
    TimeData = open("TC2000tmp.txt","w")    #タイム記録用のテンポラリファイルをオープン
    #Write KML Header / KMLヘッダ書込
    WriteData = str(HeadCom)                
    KmlData.write(WriteData)
    WriteData = str(HeadCom2)
    KmlData.write(WriteData)

    #Read GPS log data / GPS ログデータの読込
    for LogNumber in LogData:
        LogContents=LogNumber.split(',')
        
        if '$GPGGA' in LogContents[0]:
            
            #Latitude / 緯度取得
            LatitudeRaw = float(LogContents[2])
            LatitudeInt = LatitudeRaw // 100
            LatitudeKmlTmp = ((LatitudeRaw - (LatitudeInt*100))/60)+(LatitudeInt)
            
            #Longitude / 経度取得
            LongitudeRaw = float(LogContents[4])
            LongitudeInt = LongitudeRaw // 100
            LongitudeKmlTmp = ((LongitudeRaw - (LongitudeInt*100))/60)+(LongitudeInt)
            
            #Calcurate vehicle vector / 車両移動ベクトル演算
            if first:
                first = False
                LatitudeKmlPrev = LatitudeKmlTmp
                LatitudeKml = LatitudeKmlTmp
                LongitudeKmlPrev = LongitudeKmlTmp
                LongitudeKml = LongitudeKmlTmp
            else:
                LatitudeKmlPrev = LatitudeKml
                LatitudeKml = LatitudeKmlTmp  
                LongitudeKmlPrev = LongitudeKml
                LongitudeKml = LongitudeKmlTmp

            #Time / 時間取得
            AltitudeKml = float(LogContents[9])
            TimeKml = "   <!--  "+str(LogContents[1])+"  -->"
            TimHr = float(LogContents[1][:2])
            TimMn = float(LogContents[1][2:4])
            TimSc = float(LogContents[1][4:9])
            
            #Vehicle liner equation / 車両一次方程式
            CarPointPrev = (LongitudeKmlPrev,LatitudeKmlPrev)            
            CarPoint = (LongitudeKml,LatitudeKml)
            LinerCar = LinerEquation(CarPointPrev,CarPoint)

            #Sprit Sector1/Lap / セクター1/LAP演算
            ClossPoint = SystemEquation(LinerSector1Start,LinerCar)
            if (((Sector1StartPoint1[0] <= ClossPoint[0] <= Sector1StartPoint2[0]) or (Sector1StartPoint2[0] <= ClossPoint[0] <= Sector1StartPoint1[0])) 
            and ((Sector1StartPoint1[1] <= ClossPoint[1] <= Sector1StartPoint2[1]) or (Sector1StartPoint2[1] <= ClossPoint[1] <= Sector1StartPoint1[1]))
            and ((LongitudeKmlPrev <= ClossPoint[0] <= LongitudeKml) or (LongitudeKml <= ClossPoint[0] <= LongitudeKmlPrev))
            and ((LatitudeKmlPrev <= ClossPoint[1] <= LatitudeKml) or (LatitudeKml <= ClossPoint[1] <= LatitudeKmlPrev))):
                Lap += 1               
                LapCom =    "</coordinates>\n</LineString>\n</Placemark>\n<Placemark>\n<name>Lap"+str(Lap)+"_Sector1/</name>\n<styleUrl>#trace</styleUrl>\n<LineString>\n<coordinates>\n"
                WriteData = str(LapCom)
                KmlData.write(WriteData)
                
                if Lap >= 1:
                    LapTimHr = TimHr - TimHrSec1Stt
                    LapTimMn = TimMn - TimMnSec1Stt
                    if LapTimMn < 0:
                        LapTimMn +=60
                        LapTimHr -=1
                    LapTimSc = TimSc - TimScSec1Stt
                    if LapTimSc < 0:
                        LapTimSc +=60
                        LapTimMn -=1
                    TimeCom="Lap"+str(Lap-1)+"_Sector1/(LapTime"+str(math.floor(LapTimMn))+":"+str(round(LapTimSc,2))+")/("+str(math.floor(Sec1TimMn))+":"+str(round(Sec1TimSc,2))+")\n"
                    WriteData = str(TimeCom)
                    TimeData.write(WriteData)
                    
                if Lap >= 1:
                    Sec3TimHr = TimHr - TimHrSec3Stt
                    Sec3TimMn = TimMn - TimMnSec3Stt
                    if Sec3TimMn < 0:
                        Sec3TimMn +=60
                        Sec3TimHr -=1
                    Sec3TimSc = TimSc - TimScSec3Stt
                    if Sec3TimSc < 0:
                        Sec3TimSc +=60
                        Sec3TimMn -=1
                    TimeCom="Lap"+str(Lap-1)+"_Sector3/("+str(math.floor(Sec3TimMn))+":"+str(round(Sec3TimSc,2))+")\n"
                    WriteData = str(TimeCom)
                    TimeData.write(WriteData)

                TimHrSec1Stt = TimHr
                TimMnSec1Stt = TimMn
                TimScSec1Stt = TimSc


            #Sprit Sector2 / セクター2演算
            ClossPoint = SystemEquation(LinerSector2Start,LinerCar)
            if (((Sector2StartPoint1[0] <= ClossPoint[0] <= Sector2StartPoint2[0]) or (Sector2StartPoint2[0] <= ClossPoint[0] <= Sector2StartPoint1[0])) 
            and ((Sector2StartPoint1[1] <= ClossPoint[1] <= Sector2StartPoint2[1]) or (Sector2StartPoint2[1] <= ClossPoint[1] <= Sector2StartPoint1[1]))
            and ((LongitudeKmlPrev <= ClossPoint[0] <= LongitudeKml) or (LongitudeKml <= ClossPoint[0] <= LongitudeKmlPrev))
            and ((LatitudeKmlPrev <= ClossPoint[1] <= LatitudeKml) or (LatitudeKml <= ClossPoint[1] <= LatitudeKmlPrev))):
                LapCom =    "</coordinates>\n</LineString>\n</Placemark>\n<Placemark>\n<name>Lap"+str(Lap)+"_Sector2/</name>\n<styleUrl>#trace</styleUrl>\n<LineString>\n<coordinates>\n"
                WriteData = str(LapCom)
                KmlData.write(WriteData)

                if Lap >= 1:
                    Sec1TimHr = TimHr - TimHrSec1Stt
                    Sec1TimMn = TimMn - TimMnSec1Stt
                    if Sec1TimMn < 0:
                        Sec1TimMn +=60
                        Sec1TimHr -=1
                    Sec1TimSc = TimSc - TimScSec1Stt
                    if Sec1TimSc < 0:
                        Sec1TimSc +=60
                        Sec1TimMn -=1

                TimHrSec2Stt = TimHr
                TimMnSec2Stt = TimMn
                TimScSec2Stt = TimSc


            #Sprit Sector3 / セクター3演算
            ClossPoint = SystemEquation(LinerSector3Start,LinerCar)
            if (((Sector3StartPoint1[0] <= ClossPoint[0] <= Sector3StartPoint2[0]) or (Sector3StartPoint2[0] <= ClossPoint[0] <= Sector3StartPoint1[0])) 
            and ((Sector3StartPoint1[1] <= ClossPoint[1] <= Sector2StartPoint2[1]) or (Sector3StartPoint2[1] <= ClossPoint[1] <= Sector3StartPoint1[1]))
            and ((LongitudeKmlPrev <= ClossPoint[0] <= LongitudeKml) or (LongitudeKml <= ClossPoint[0] <= LongitudeKmlPrev))
            and ((LatitudeKmlPrev <= ClossPoint[1] <= LatitudeKml) or (LatitudeKml <= ClossPoint[1] <= LatitudeKmlPrev))):
                LapCom =    "</coordinates>\n</LineString>\n</Placemark>\n<Placemark>\n<name>Lap"+str(Lap)+"_Sector3/</name>\n<styleUrl>#trace</styleUrl>\n<LineString>\n<coordinates>\n"
                WriteData = str(LapCom)
                KmlData.write(WriteData)
                    
                if Lap >= 1:
                    Sec2TimHr = TimHr - TimHrSec2Stt
                    Sec2TimMn = TimMn - TimMnSec2Stt
                    if Sec2TimMn < 0:
                        Sec2TimMn +=60
                        Sec2TimHr -=1
                    Sec2TimSc = TimSc - TimScSec2Stt
                    if Sec2TimSc < 0:
                        Sec2TimSc +=60
                        Sec2TimMn -=1
                    TimeCom="Lap"+str(Lap)+"_Sector2/("+str(math.floor(Sec2TimMn))+":"+str(round(Sec2TimSc,2))+")\n"
                    WriteData = str(TimeCom)
                    TimeData.write(WriteData)

                TimHrSec3Stt = TimHr
                TimMnSec3Stt = TimMn
                TimScSec3Stt = TimSc

            WriteData = str(LongitudeKml+LongitudeKmlComp)+","+str(LatitudeKml+LatitudeKmlComp)+","+str(AltitudeKml)+TimeKml+"\n"
            KmlData.write(WriteData)

    WriteData = str(FootCom)
    KmlData.write(WriteData)
    #ファイルを閉じる
    LogData.close()
    KmlData.close()
    TimeData.close()

def LinerEquation(Point1,Point2):
    Longitude = [Point1[0],Point2[0]]
    Latitude = [Point1[1],Point2[1]]
    return np.polyfit(Longitude,Latitude,1)

def SystemEquation(Line1,Line2):
    Left =[[-Line1[0], 1],
           [-Line2[0],  1]]
    Right= [Line1[1],  Line2[1]]
    return np.linalg.solve(Left,Right)

def Replace():
    TimeData = open("TC2000tmp.txt","r")
    KmlData = open("TC2000tmp.kml", "r")
    LapData = open("TC2000.kml", "w")
    
    Contents = KmlData.read()
    for TimeNumber in TimeData:
        SplitContents = TimeNumber.split('/')
        Contents = Contents.replace(SplitContents[0], TimeNumber)
    LapData.write(Contents)
    #ファイルを閉じる
    TimeData.close()
    KmlData.close()
    LapData.close()


###################################
# Main Routine
###################################
import numpy as np
import math

LogFileRead()
Replace()

print ('The process has been completed. / プロセスは完了しました。')