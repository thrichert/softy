@REM ---------- Define constants
@set "RTYPE_Ma=Ma"
@set "RTYPE_Mi=Mi"
@set "RTYPE_Pa=Pa"
@set "RTYPE_Te=Te"

@REM ---------- Go in Release folder
@cd ..
@cd release
@REM ---------- Check for current version Number
@for /f "tokens=1,2,3 delims=. " %%a in ('dir /a:d /b') do set /a major=%%a&set /a nMajor=%%a+1&set /a minor=%%b set /a nMinor=%%b+1&set /a patch=%%c&set /a nPatch=%%c+1
@echo Current Version

@echo.Major	: %major:~-4%
@echo.Minor	: %minor:~-4%
@echo.Patch	: %patch:~-4%

@REM ---------- Ask for Release type

@echo Release Type [Ma : for major, Mi : for minor, Pa : for patch]:
@echo Enter the type of release you want to create:
@set /p RTYPE=
@if "%RTYPE%" EQU "%RTYPE_Ma%" (
	@echo selected : %RTYPE%
	@echo create new version : v%nMajor%.%minor%.%patch%
	@mkdir v%nMajor%.%minor%.%patch%
	@cd ../sources
	@pyinstaller.exe --onefile .\main.spec
	@COPY .\dist\main.exe ..\release\v%nMajor%.%minor%.%patch%\softy_%nMajor%.%minor%.%patch%.exe

) else if "%RTYPE%" EQU "%RTYPE_Mi%" (
	@echo selected : %RTYPE%
	@echo create new version : v%major%.%nMinor%.%patch%
	@mkdir v%major%.%nMinor%.%patch%
	@cd ../sources
	@pyinstaller.exe --onefile .\main.spec
	@COPY .\dist\main.exe ..\release\v%major%.%nMinor%.%patch%\softy_%major%.%nMinor%.%patch%.exe

) else if "%RTYPE%" EQU "%RTYPE_Pa%" (
	@echo selected : %RTYPE%
	@echo create new version : v%major%.%minor%.%nPatch%
	@mkdir v%major%.%minor%.%nPatch%
	@cd ../sources
	@pyinstaller.exe --onefile .\main.spec
	@COPY .\dist\main.exe ..\release\v%major%.%minor%.%nPatch%\softy_%major%.%minor%.%nPatch%.exe

) else if "%RTYPE%" EQU "%RTYPE_Te%" (
	@echo selected : %RTYPE%
	@pyinstaller.exe --onefile .\main.spec

)else (
	@echo Error - unvalid parameters
	@echo Major			Ma
	@echo Minor			Mi
	@echo Patch			Pa
	@echo Test			Te		Use for Debug - does not copy in release
	@REM ---------- Go in Source folder
	@cd ../sources
)

