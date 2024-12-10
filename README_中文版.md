# 程式介紹
# 程式名稱:
rmIns_for_sac_mseed.py

# 功能:
用於移除地震資料儀器響應之工具

# 需求:
python 3.6+
模組: pip, obspy
作業系統: Windows / Linux

# 使用:
使用方法: python rmIns_for_sac_mseed.py <path to SAC or MSEED> <path to StationXML file> <output unit>
注意: output unit 該項必須是 ACC VEL DISP, 單位分別是公尺/秒平方, 公尺/秒, 公尺, 大小寫不拘
