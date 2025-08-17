@echo off
echo Starting Deception Detector Frontend...

cd frontend

if not exist node_modules (
    echo Installing npm dependencies...
    npm install
)

echo Starting Vue development server...
npm run serve
