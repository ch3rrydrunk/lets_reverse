#!/env/bin/python3.7
import os
import sys
import xml.etree as xxxml
import xml.etree.ElementTree as ET
from androguard.core.bytecodes.apk import APK
from androguard.core.bytecodes.axml import AXMLPrinter
from androguard.core.bytecodes.axml import ARSCParser

def android_str(str):
	return "".join(["{http://schemas.android.com/apk/res/android}", str])

# Данный скрипт принимает в качестве аргумента имя файла и :
# 1. выводит значение флагов безопасности в Android Manifest 
# 2. выводит список секретных кодов приложения; 
# 3. выводит список библиотек, используемых в приложении.
# Всегда выводит информативное сообщение, очень вежливый

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
print("<< Флаги безопасности Manifest'а >>\n"
		"  а. Установки CleartextTraffic:")
guess = axml.find("./application[@{}]".format(android_str("usesCleartextTraffic")))
if guess != None:
	print("\t - флаг:'{}'".format(guess.attrib.get(android_str("usesCleartextTraffic"))))
else:
	print("\tНе обнаружено.")

print("  b. Установки allowBackup:")
guess = axml.find("./application[@{}]".format(android_str("allowBackup")))
if guess != None:
	print("\t - флаг:'{}'".format(guess.attrib.get(android_str("allowBackup"))))
else:
	print("\tНе обнаружено.")

print("  c. Установки WebView:")
guess = axml.find("./application/meta-data[@{}='android.webkit.WebView.EnableSafeBrowsing']".format(android_str("name")))
if guess != None:
	print("\t - флаг:'{}'".format(guess.attrib.get(android_str("value"))))
else:
	print("\tНе обнаружено.")


# 2. Список секретных кодов
print("\n<< Список секретных кодов >>")
for element in axml.findall(".//receiver//data[@{}='android_secret_code']".format(android_str("scheme"))):
	lil_pow = 1
	print("\tКод {} вызывает {}".format(element.attrib.get(android_str("host")), element.find(".../...").attrib.get(android_str("name"))))
if not lil_pow:
	print("\tНе обнаружено.")
lil_pow = 0


# 3. Список библиотек
print("\n<< Список использованных библиотек:>>")
apk_dict = apk.files
for pack in apk_dict:
	sopack = str(pack)
	if (sopack.endswith(".so")):
		lil_pow = 1
		print("\t - {}".format(sopack.rsplit("/")[-1]))
if not lil_pow :
	print("\tНе обнаружено.")
