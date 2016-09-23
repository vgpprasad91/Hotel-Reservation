rm -rf output1.txt
read userinput
echo $userinput | syntaxnet/demo.sh >> output1.txt 
python gettime.py

