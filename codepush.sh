WORKING_DIR=$(pwd)
echo "is working dir"
echo $WORKING_DIR
sudo rsync --archive --progress --update --modify-window=-1 "$WORKING_DIR"/ rpi@192.168.12.1:~/Sailtracker/sail/ --rsync-path="mkdir -p ~/Sailtracker/sail && rsync" --exclude ".venv" --exclude ".idea" --exclude "output.csv" --exclude ".git"
ssh rpi@192.168.12.1