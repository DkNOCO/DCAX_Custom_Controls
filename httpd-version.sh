output=`/usr/sbin/httpd -v`

message=`echo "$output" | grep "$1"`
if [[ $message == *"$1"* ]]; then
  echo "2.4.6 installed"
  exit 0
fi
message=`echo "$output" | grep "Apache/"`
if [[ $message == *"Apache/"* ]]; then
  echo "$message wrong version installed"
  exit 1
fi
echo "not installed"
exit 1