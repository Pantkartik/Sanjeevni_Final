@echo off
REM Build and export Next.js static site
npm run build
npm run export
REM Remove old public folder contents
rmdir /s /q public
mkdir public
REM Copy exported files to public
xcopy /E /I /Y out\* public\
REM Deploy to Firebase Hosting
firebase deploy --only hosting