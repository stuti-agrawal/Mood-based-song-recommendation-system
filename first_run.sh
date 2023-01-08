APP_DIR=$(pwd)

echo "**********FLASK**********"
echo "Installing Flask requirements"
python3 -m pip install -r requirements.txt
echo "Flask requirements installed"

echo "**********REACT**********"
echo "Installing React libraries"
cd "$APP_DIR"/static
npm install
npm run build
cd "$APP_DIR"
echo "React libraries installed"

echo "**********Starting server**********"
export FLASK_APP=app.py
export FLASK_ENV=production
flask run