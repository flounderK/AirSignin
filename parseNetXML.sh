#!$SHELL
if [ -z "$1" ]; then
	capturepath=$(/home/pi/kismet)
else
	capturepath=$1
fi

cd $capturepath
filename=$(date +"%m-%d-%y")
if [ ! -d $capturepath/$filename ]; then
	mkdir $capturepath/$filename
fi

for i in $( ls *.netxml );do
	mv $i $capturepath/$filename/$i
done

cd $filename
grep -r -h -o -P "(?<=BSSID\>)([A-F0-9]{2}:){5}[A-F0-9]{2}" >> ./$filename.txt
mv $filename.txt ..


