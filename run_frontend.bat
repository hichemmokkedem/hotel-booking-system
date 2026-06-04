@echo off
pushd "%~dp0frontend"
echo Installing dependencies...
npm install
echo Starting Frontend...
npm run dev
popd
