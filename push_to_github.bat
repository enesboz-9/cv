@echo off
cd /d "C:\Users\enesb\cv"

echo [1/3] Degisiklikler ekleniyor...
git add .

echo [2/3] Commit yapiliyor...
git commit -m "Portfolio guncellendi"

echo [3/3] GitHub'a push ediliyor...
git push origin main

echo.
echo Tamamlandi! GitHub'a basariyla yuklendi.
pause
