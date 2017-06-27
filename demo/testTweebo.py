import sys
import os

text = "Hello, this is an amazing tweet!"
#text2 = "This is a second tweet with Apple, Samsung, Twitter"
fp = open("tweet1.txt", 'w')
fp.writelines(text + "\n")
#fp.writelines(text2)
fp.close()
#os.system("cd tweeboparser/TweeboParser")
#os.system("pwd")
os.system("bash tweeboparser/TweeboParser/run.sh tweet1.txt")
fp = open("tweeboparser/TweeboParser/tweet1.txt.predict")

for line in fp.readlines():
    print line
