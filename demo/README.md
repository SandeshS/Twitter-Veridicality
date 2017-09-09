# Steps for running the demo:

* Before you try running this demo, you will need to install [Twitter-NLP](https://github.com/aritter/twitter_nlp) tools made available by Prof. Ritter and [TweeboParser](https://github.com/ikekonglp/TweeboParser) made available by Linpeng Kong et.al. 
* Make sure the locations of Twitter-NLP and TweeboParser are noted. (It is preferred to have TweeboParser in the same directory as this demo)
* Once you have Twitter-NLP installed, run `export TWITTER_NLP=<location where twitter nlp tools was installed>`.
* Now you are ready to run the demo! :)
* First, you would want to create a text file with the following format (please follow this strictly) -
  * The first line of the file has to be the event you want to track on Twitter. (Example: Oscars, NBAAwards, Elections)
  * This line can be followed by all the contenders you want to track for that particular event. (Example: For Oscars, Leonardo di Caprio, Tom Hanks, Bradley Cooper)
  * All the contenders **have** to be separated by a newline character.
* Now, you can run the demo as follows `python demo.py <filename>`
