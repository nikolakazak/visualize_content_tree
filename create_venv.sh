echo "create venv"
python -m venv ./venv
cd ./venv/Scripts/
./activate.bat
echo "install requirements"
./pip install -r ../../requirements.txt
echo "fix treelib"
cp ../../tree.py ../Lib/site-packages/treelib/tree.py
echo "done"
sleep 3
pause >nul