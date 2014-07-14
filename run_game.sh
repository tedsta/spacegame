echo "Starting server ..."
python3 server.py &
sleep 2
echo "Starting first client ..."
python3 client.py &
sleep 2
echo "Starting second client ..."
python3 client.py &

sleep 3
read -p "Press enter to terminate. " answer

kill %1
kill %2
kill %3

