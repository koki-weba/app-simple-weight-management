@echo off
REM 体重管理アプリをローカルサーバーで起動
cd /d "%~dp0"
echo.
echo ===== 体重管理アプリ - 起動中 =====
echo.
echo ブラウザで以下のURLを開いてください:
echo   http://localhost:8080
echo.
echo スマホからアクセスする場合:
echo   http://[このPCのIPアドレス]:8080
echo   (IPアドレスは別ウィンドウで 'ipconfig' で確認)
echo.
echo 終了するには Ctrl+C を押してください。
echo.
npx --yes http-server -p 8080 -c-1 -o
pause
