cd static
npm run build
cd ..

$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
flask run