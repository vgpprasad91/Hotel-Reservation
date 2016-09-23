rm -rf parse.txt
rm -rf output.txt
rm -rf output1.txt
read userinput
echo $userinput | syntaxnet/demo.sh > output.txt
echo $userinput | syntaxnet/demo.sh > output1.txt
