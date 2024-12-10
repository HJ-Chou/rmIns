# 程式介紹
## 1. 程式名稱:
rmIns_for_sac_mseed.py

## 2. 功能:
用於移除地震資料儀器響應之工具

## 3. 需求:
  ##### 3-1.  python 3.6+
  ##### 3-2.  模組: pip, obspy
  ##### 3-3.  作業系統: Windows / Linux

## 4. 使用:
  ##### 4-1.  使用方法: python rmIns_for_sac_mseed.py <path to SAC or MSEED> <path to StationXML file> <output unit>
  ##### 4-2.  注意: output unit 該項必須是 ACC VEL DISP, 單位分別是公尺/秒平方, 公尺/秒, 公尺, 大小寫不拘
