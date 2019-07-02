#!/env/bin/python3.7
import os
import sys
import xml.etree as xxxml
import xml.etree.ElementTree as ET
from androguard.core.bytecodes.apk import APK
from androguard.core.bytecodes.axml import AXMLPrinter
from androguard.core.bytecodes.axml import ARSCParser

ANDROID_SCHEME = "{http://schemas.android.com/apk/res/android}scheme"
ANDROID_HOST = "{http://schemas.android.com/apk/res/android}host"
ANDROID_NAME = "{http://schemas.android.com/apk/res/android}name"

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
# 			<intent-filter>
# 				<action android:name="android.provider.Telephony.SECRET_CODE" />
#				<data android:scheme="android_secret_code" android:host="727" />
#			</intent-filter>			
# 3. выводит список библиотек, используемых в приложении.

if len(sys.argv) != 2:
	print("Я принимаю на вход только 1 параметр - путь к APK\n"
			"И да, лучше кормить меня только APK, я не знаю, "
			"что делать с другими файлами\n¯\\_(ツ)_/¯")
	exit(400)
file = sys.argv[1]

apk = APK(file)
axml = apk.get_android_manifest_xml()
num_check = 0

# 1. Флаги Безопасности


# 2. Список секретных кодов
print("Задание 2 - Список секретных кодов")
for element in axml.findall(".//receiver//data[@{}='android_secret_code']".format(ANDROID_SCHEME)):
	num_check = 1
	print("Код {} вызывает {}".format(element.attrib.get(ANDROID_HOST), element.find(".../...").attrib.get(ANDROID_NAME)))
if not num_check:
	print("Не обнаружено.")
num_check = 0

# 3. Список библиотек
print("Задание 3 - Список использованных библиотек:")
apk_dict = apk.files
for pack in apk_dict:
	sopack = str(pack)
	if (sopack.endswith(".so")):
		num_check = 1
		print(sopack.rsplit("/")[-1])
if not num_check :
	print("Не обнаружено.")
num_check = 0
