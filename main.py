#!/env/bin/python3.7
import os
import sys
import xml.etree.ElementTree as ET
from androguard.core.bytecodes.apk import APK
from androguard.core.bytecodes.axml import AXMLPrinter
from androguard.core.bytecodes.axml import ARSCParser

# 1. выводит значение флагов безопасности в Android Manifest 
# - WebView Metrics 
# 	какие такие метрики хэз;
# - usesCleartextTraffic
#	[безопасно - android:usesCleartextTraffic=”false”];
# - Backup
#	[безопасно - android:allowBackup=”false”]
# 2. выводит список секретных кодов приложения; 
# (имеются ввиду телефонные коды) 
#    типа такого:
# 		<receiver android:name=".receivers.DebugReceiver">
# 		<intent-filter>
# 		<action android:name="android.provider.Telephony.SECRET_CODE" />
#		<data android:scheme="android_secret_code" android:host="727" />
#		</intent-filter>			
#
# 3. выводит список библиотек, используемых в приложении.

# Импорт пути
if len(sys.argv) != 2:
	print("Я принимаю на вход только 1 параметр - путь к APK\n"
			"И да, лучше кормить меня только APK, я не знаю, ч"
			"то делать с другими файлами\n¯\\_(ツ)_/¯")
	exit(400)
file = sys.argv[1]

apk = APK(file)
apk_lib_list = apk.get_libraries()
axml = apk.get_android_manifest_xml()
# axml_text = axml.tostring(root, encoding='utf8').decode('utf8')
