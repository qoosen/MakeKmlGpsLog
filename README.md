# MakeKmlGpsLog
Make KML file from Race track GPS log  
【機能】   
　自動車レースやサーキット走行等の周回走行(筑波サーキットTC2000)におけるNMEAフォーマットのGPSログデータから、ラップタイム/区間タイム/軌跡をKMLフォーマットに変換するPythonスクリプトになります。   
   
【開発背景】   
　Amazon等で¥2000前後で入手できるUSB‐GPSレシーバーとノートPC(車載)を用いて安価に実現できる、サーキット等でのクローズド周回路における運転技術の向上に役立つ事を目的とした。
   
NMEAフォーマットの例 (本プログラムで参照するのは'$GPGGA'になります。)   
```
$GPGGA,052032.40,3609.00729,N,13955.30284,E,2,09,0.82,26.5,M,39.4,M,,0000*67   
$GPGSA,A,3,26,31,16,27,18,02,29,08,09,,,,1.30,0.82,1.02*0C   
$GPGSV,4,1,14,02,15,046,41,04,33,292,,08,14,222,42,09,10,319,25*78   
$GPGSV,4,2,14,16,54,303,33,18,31,088,33,22,17,184,,26,65,026,38*74   
$GPGSV,4,3,14,27,47,219,45,28,40,133,,29,09,041,38,31,49,128,25*76   
$GPGSV,4,4,14,39,03,262,,50,46,201,44*77   
$GPGLL,3609.00729,N,13955.30284,E,052032.40,A,D*68   
$GPRMC,052032.50,A,3609.00729,N,13955.30284,E,0.091,,260123,,,D*7C   
$GPVTG,,T,,M,0.091,N,0.169,K,D*20
```
【使用(変換)方法】   
　0.Pythonのインストール   
　1.MakeKmlGpsLog.pyのダウンロード   
　　　任意のフォルダ上にMakeKmlGpsLog.pyをダウンロードする。   
　2.NMEAフォーマットのGPSログデータの保存   
　　　"TC2000.log"というファイルネームでNMEAフォーマットのGPSログデータをMakeKmlGpsLog.pyを保存した同一フォルダに保存する。   
　　　USB‐GPSレシーバーによるログの取得方法は、こちらを参考にしてください。
　3.KMLファイルの生成/MakeKmlGpsLog.pyの実行   
　　　MakeKmlGpsLog.pyを実行する。   
　　　'The process has been completed. / プロセスは完了しました。'   
　　　と表示されたら、各LAP/セクターに分割した"TC2000.kml"が生成されます。   
　　　中間生成物として"TC2000tmp.kml"と"TC2000tmp.txt"が生成されますが、正常終了後は消去してもらって良いです。   
    
【KMLファイルの閲覧方法】   
　1.Google earth proによる閲覧   
　　Google Earth Proは無料でダウンロード/利用できますので、こちらを使うのがおすすめです。   
　　インストールされていれば、生成されたKMLファイルをダブルクリックするだけで   
　2.Webブラウザ(Google Map)による閲覧
　　お試しやノンネイティブ環境での閲覧は、こちらの方法を使うのがおすすめです。   
　　とりあえず、こちらで試してみて1.の環境に移行するのもよいかと思います。   
     
【追伸】   
　筑波サーキットTC2000以外に適用したい場合は、座標データ(東経,北緯)を変更することで対応可能です。   
　連立方程式の解法を使用している関係上、関数にならない(=Point1/2で北緯が同じ)と演算できなくなります。   
　この場合は、極小さな値を加算するなどして対策してください。
 ```
    Sector1StartPoint1 = [139.91930,36.15020]   #Sector1 start line(Start line) point1 [Longitude,Latitude]/ セクター1(スタートライン)の点1 東経,北緯
    Sector1StartPoint2 = [139.91982,36.15011]   #Sector1 start line(Start line) point2 [Longitude,Latitude]/ セクター1(スタートライン)の点2 東経,北緯
    Sector2StartPoint1 = [139.92052,36.15013]   #Sector2 start line point1 [Longitude,Latitude]/ セクター2開始線の点1 東経,北緯
    Sector2StartPoint2 = [139.92095,36.15007]   #Sector2 start line point2 [Longitude,Latitude]/ セクター2開始線の点2 東経,北緯
    Sector3StartPoint1 = [139.92161,36.14971]   #Sector3 start line point1 [Longitude,Latitude]/ セクター3開始線の点1 東経,北緯
    Sector3StartPoint2 = [139.92208,36.14942]   #Sector3 start line point2 [Longitude,Latitude]/ セクター3開始線の点1 東経,北緯
```
 
 　サンプルとして、TC2000.logおよび生成したTC2000.kmlをこちらに置きます。   
　　本サンプルに対して、遅い！とか、ライン取りが悪い！等のissueは受け付けません(笑) 
