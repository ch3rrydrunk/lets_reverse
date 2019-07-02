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
ANDROID_BACKUP = "{http://schemas.android.com/apk/res/android}allowBackup"
ANDROID_CLEAR = "{http://schemas.android.com/apk/res/android}usesCleartextTraffic"
ANDROID_VALUE = "{http://schemas.android.com/apk/res/android}value"

# Данный скрипт принимает в качестве аргумента имя файла и осуществляет следующие операции:
# 1. выводит значение флагов безопасности в Android Manifest 
# - WebView Metrics 
# 	<meta-data android:name="android.webkit.WebView.EnableSafeBrowsing" android:value="false" />
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

# Принимаем файл и задаем необходимые для работы переменные
if len(sys.argv) != 2:
	print("Я принимаю на вход только 1 параметр - путь к APK\n"
			"И да, лучше кормить меня только APK, я не знаю, "
			"что делать с другими файлами\n¯\\_(ツ)_/¯")
	exit(400)
file = sys.argv[1]
apk = APK(file)
axml = apk.get_android_manifest_xml()
lil_pow = 0


# 1. Флаги Безопасности
print("Задание 1 - Флаги безопасности Manifest'а\n"
		"а. Установки CleartextTraffic:")
guess = axml.find("./application[@{}]".format(ANDROID_CLEAR))
if guess != None:
	print(guess.attrib.get(ANDROID_CLEAR))
else:
	print("Не обнаружено.")

print("b. Установки allowBackup:")
guess = axml.find("./application[@{}]".format(ANDROID_BACKUP))
if guess != None:
	print(guess.attrib.get(ANDROID_BACKUP))
else:
	print("Не обнаружено.")

print("b. Установки WebView:")
guess = axml.find("./application/meta-data[@{}='android.webkit.WebView.EnableSafeBrowsing']".format(ANDROID_NAME))
if guess != None:
	print(guess.attrib.get(ANDROID_VALUE))
else:
	print("Не обнаружено.")


# 2. Список секретных кодов
print("Задание 2 - Список секретных кодов")
for element in axml.findall(".//receiver//data[@{}='android_secret_code']".format(ANDROID_SCHEME)):
	lil_pow = 1
	print("Код {} вызывает {}".format(element.attrib.get(ANDROID_HOST), element.find(".../...").attrib.get(ANDROID_NAME)))
if not lil_pow:
	print("Не обнаружено.")
lil_pow = 0


# 3. Список библиотек
print("Задание 3 - Список использованных библиотек:")
apk_dict = apk.files
for pack in apk_dict:
	sopack = str(pack)
	if (sopack.endswith(".so")):
		lil_pow = 1
		print(sopack.rsplit("/")[-1])
if not lil_pow :
	print("Не обнаружено.")
