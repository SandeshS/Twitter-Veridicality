# About

This is a demo of the work we present in our paper. This demo takes as input a text file containing the name of the event and the contenders in the event to be tracked.

The demo then runs the Twitter API to fetch realtime tweets about the event and contenders. Every tweet is further processed by our veridicality classifier and a prediction is made for each tweet about the veridicality of the tweet. Further, winning prediction scores are calculated for every contender and displayed to the user on the console.

## Steps for running the demo

* Before you try running this demo, you will need to install [Twitter-NLP](https://github.com/aritter/twitter_nlp) tools made available by Prof. Ritter and [TweeboParser](https://github.com/ikekonglp/TweeboParser) made available by Linpeng Kong et.al. 
* Make sure the locations of Twitter-NLP and TweeboParser are noted. (It is preferred to have TweeboParser in the same directory as this demo)
* Once you have Twitter-NLP installed, run `export TWITTER_NLP=<location where twitter nlp tools was installed>`.
* Now you are ready to run the demo! :)
* First, you would want to create a text file with the following format (please follow this strictly) -
  * The first line of the file has to be the event you want to track on Twitter. (Example: Oscars, NBAAwards, Elections)
  * This line can be followed by all the contenders you want to track for that particular event. (Example: For Oscars, Leonardo di Caprio, Tom Hanks, Bradley Cooper)
  * All the contenders **have** to be separated by a newline character.
  * An example file has been provided for you as `event1.txt`.
* Now, you can run the demo as follows `python demo.py <filename>`

## Citing our work

If you used this demo in your research project/work, do cite our work as follows -

    @inproceedings{ssarmcdm2017forecasting,
    title      = {"i have a feeling trump will win..................": Forecasting Winners and Losers from User Predictions on Twitter},
    author     = {Swamy, Sandesh and Ritter, Alan and de Marneffe, Marie-Catherine},
    booktitle  = {Proceedings of the Conference on Empirical Methods in Natural Language Processing.},
    year       = {2017},
    url        = {http://aclweb.org/anthology/D17-1166}
    } 

## NOTE

You will need to get your own Twitter API keys before you can run the demo. Follow the instructions [here](http://socialmedia-class.org/twittertutorial.html)(courtesy of Prof. Xu) to get the keys and plug it into the `demo.py *lines 551-554*` file before running the demo.

### Known bug

The scores for contenders all start off equal - this is intentional. We start with the assumption that every contender is equally likely to win. However, with the demo, the scores go up for a candidate who is predicted to win and correspondingly, the score does not go down for the other contenders. A fix will be rolled out soon.
