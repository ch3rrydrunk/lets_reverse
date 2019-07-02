Let's Reverse!

> **rev_apk_info.py**
# Данный скрипт принимает в качестве аргумента имя файла и осуществляет следующие операции:
# 1. выводит значение флагов безопасности в Android Manifest 
# - WebView Metrics 
# 	<meta-data android:name="android.webkit.WebView.EnableSafeBrowsing" android:value="false" />
# - usesCleartextTraffic
#	[безопасно - android:usesCleartextTraffic=”false”];
# - Backup
#	[безопасно - android:allowBackup=”false”]
#
# 2. выводит список секретных кодов приложения; 
# (имеются ввиду телефонные коды) 
#    типа такого:
# 		<receiver android:name=".receivers.DebugReceiver">
# 			<intent-filter>
# 				<action android:name="android.provider.Telephony.SECRET_CODE" />
#				<data android:scheme="android_secret_code" android:host="727" />
#			</intent-filter>
#
# 3. выводит список библиотек, используемых в приложении.