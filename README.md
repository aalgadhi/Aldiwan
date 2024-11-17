<h3 align="right">الديوان</h3>
<p align="right">هذا البرنامج يأخذ القصائد من موقع الديوان ومن ثم يعيد ترتيبها وتنسيقها ليحفظها بعد ذلك بصيغة وورد وبي دي إف</p>

<h3 align="right">طريقة التشغيل</h3>
<p align="right">حمل ملف aldiwan.exe وشغّل البرنامج مباشرة بعد ذلك</p>

<h3 align="right">طريقة بناء البرنامج</h3>
<p align="right">:لبناء البرنامج يمكنك استعمال الأمر التالي

pip install pyinstaller (اذا لم تكن عندك المكتبة)

pyinstaller --onefile --icon=logo.ico --name=aldiwan main.py


### Aldiwan
This program takes a poem from Aldiwan website, rearranges the poem and its info and then it saves it as a docx file and a pdf file.
### Build
To build an exe app you can use pyinstaller in the terminal as the following: 

pip install pyinstaller (if you do not have the library)

pyinstaller --onefile --icon=logo.ico --name=aldiwan main.py

You will find the build in a folder called dest.
