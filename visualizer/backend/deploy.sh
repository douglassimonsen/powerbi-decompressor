rm -rf dist
mkdir dist
rm -rf dist
pip3 install -r requirements.txt -t dist/
cp app.py dist/
cp application.py dist/
cp util.py dist/
cp -R static dist/
cp -R psycopg2 dist/
# copy creds