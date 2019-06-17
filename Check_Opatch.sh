
output=`sudo -u oracle $2 lsinventory -patch -oh $1`
message=`echo "$output" | grep "There are no Interim patches installed in this Oracle Home."`
if [ "$message" = "There are no Interim patches installed in this Oracle Home." ]; then
  echo "$message dead"
  exit 1
fi
message=`echo "$output" | grep $3`
if [[ $message == *"applied on"* ]]; then
  echo "$message"
  exit 0
fi
message=`echo "$output" | grep "applied on"`
if [[ $message == *"applied on"* ]]; then
  echo "$message"
  exit 1
fi
echo "$message"
exit 1