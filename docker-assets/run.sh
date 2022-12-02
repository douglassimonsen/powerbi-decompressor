nohup python3 /visualizer/backend/application.py > /visualizer/frontend.log &
echo "flask backend running"
nohup npm run dev > /visualizer/frontend.log &
echo "nodejs frontend running"
trap : TERM INT; sleep infinity & wait
