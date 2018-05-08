# Data

The annotated data files(`train_with_metadata`, `dev_with_metadata` and `test_with_metadata` - this was the split we used in our experiments) consists of two columns - the Tweet ID and the Veridicality Annotation. 

Each file has three columns. The columns can be read as follows:

`TweetID, Tweet Metadata, Veridicality annotation`

The metadata field can be explained with an example. ['elections', 'Trump', 'Nevada'] indicates that we were annotating for the
outcome of the election event for Trump in Nevada. Similarly, ['Oscars', 'Matthew McConaughey '] indicates that we were annotating for the outcome of the Oscars Best actor award for Matthew McConaughey.

The annotations can be interpreted as follows
   
   
   
   * DY- Tweet indicates "definitely yes" towards an event happening (i.e., strong positive veridicality)
   
   
   
   * PY- Tweet indicates "probably yes" towards an event happening (i.e., positive veridicality)
   
   
   
   * UC - uncertain towards the event's outcome (i.e., neutral)
   
   
   
   * PN- Tweet indicates "probably no" towards an event happening (i.e., negative veridicality)
   
   
   
   * DN- Tweet indicates "definitely no" towards an event happening (i.e., strong negative veridicality)
   
   
There is also another file - `completedataset.txt` which contains the entire dataset which was collected for this project. This is a file containing all the Tweet IDs for the tweets we used. Twitter policy restricts from distributing actual text data. If you are having trouble downloading actual text from the IDs, you can refer to [this](https://github.com/aritter/twitter_download) tool courtesy of [Prof. Alan Ritter](https://aritter.github.io)
   
# Citing our work

If you are using this dataset in your task, cite our work as follows -
          
          
          
          @inproceedings{ssarmcdm2017forecasting,
  	        title      = {"i have a feeling trump will win..................": Forecasting Winners and Losers from User Predictions on Twitter},
  	        author     = {Swamy, Sandesh and Ritter, Alan and de Marneffe, Marie-Catherine},
  	        booktitle  = {Proceedings of the Conference on Empirical Methods in Natural Language Processing.},
  	        year       = {2017},
  	        url        = {http://aclweb.org/anthology/D17-1166}
  	      }
 
