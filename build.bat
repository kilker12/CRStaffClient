cd C:\Users\Joey\Development
mkdir .\GitHub\CRStaffClient\temp
rmdir /S /Q .\GitHub\CRStaffClient\build
C:\Python27\python.exe .\Tools\pyinstaller-2.0\pyinstaller.py -c -y -o .\GitHub\CRStaffClient\temp\ .\GitHub\CRStaffClient\client.py
move .\GitHub\CRStaffClient\temp\dist\client .\GitHub\CRStaffClient\build
rmdir /S /Q .\GitHub\CRStaffClient\temp
