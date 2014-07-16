# This runs the server on a machine with no GL context

Xvfb :5 -screen 0 800x600x24 &
export DISPLAY=:5

echo "Starting server ..."
python3 server.py &

read -p "Press enter to terminate. " answer

kill %1
kill %2
