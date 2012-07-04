#!/usr/bin/python
import urllib2
from json import JSONDecoder
import string

#------------------------------------------------------------------------

__author__ = "Sean Policarpio"
__copyright__ = "Copyright 2011"
__credits__ = ["Sean Policarpio"]
__license__ = "private"
__version__ = "0.1.0"
__maintainer__ = "Sean Policarpio"
__email__ = "kdrakon@gmail.com"
__status__ = "Production"

#------------------------------------------------------------------------
class twitterSearchAggregator:
#------------------------------------------------------------------------
    def __init__(self):
        try:
            since_id_file = open("since_id", 'r')
            self.since_id = since_id_file.read().strip()
            since_id_file.close()
            
            query_terms_file = open("query_terms", 'r')
            self.query_terms = query_terms_file.read().strip()
            query_terms_file.close()       
            
            print "LOG: using since_id (max_id from last search) of " + self.since_id + " and query terms: " + self.query_terms     
            
        except:
            print "error opening init files"

#------------------------------------------------------------------------

    def getSearchResults(self, urlQueryStr):
        '''This function will execute a Twitter search query and return a resulting query object (JSON)'''
        try:
            print "LOG: Attempting to connect to: " + urlQueryStr
            o = urllib2.urlopen(urlQueryStr)
            result = o.read()
        except:
            result = 0
            print "urllib2 failed"
        finally:
            return self.parseSearchResults(result, urlQueryStr)
            
#------------------------------------------------------------------------            
        
    def parseSearchResults(self, result, urlQueryStr):
        '''Parse the JSON return result'''
        
        parsedResults = dict() #final returned results
        
        if (result != 0):
            decoder = JSONDecoder()
            jsonResult = decoder.decode(result)            
    
            #print "LOG: available result keys:\n" + jsonResult.keys()
            
            #-----------------recursive section----------------
            '''If there exists more 'pages' of results, recursively get them'''
            if 'next_page' in jsonResult.keys():
                next_urlQueryStr = string.split(urlQueryStr, "?", 1)[0] + jsonResult['next_page']
                if 'since_id' in jsonResult.keys():
                    '''append the since_id to this query to ensure we don't search too far'''
                    next_urlQueryStr = next_urlQueryStr + "&since_id=" + jsonResult['since_id_str']
                print "LOG: recursively searching at:\n" + next_urlQueryStr
                
                '''This will possibly return results, which must be appended forward to the current search results'''
                parsedResults = self.getSearchResults(next_urlQueryStr)               
            #------------end of recursive section-------------                
                        
            '''save the currently searched tweets and other info'''
            print jsonResult['max_id_str']
            if jsonResult['page'] == 1:
                parsedResults['max_id'] = jsonResult['max_id_str']
            tweetsKey = "tweets_page" + str(jsonResult['page'])       
            parsedResults[tweetsKey] = jsonResult['results'] #dict

        return parsedResults

#------------------------------------------------------------------------

    def saveSearchResults(self, parsedResults):
    
        '''...'''

#------------------------------------------------------------------------
#                          Main execution
#------------------------------------------------------------------------

'''create & execute search object'''
tsa = twitterSearchAggregator()

try:
    pr = tsa.getSearchResults("http://search.twitter.com/search.json?q=" + tsa.query_terms + "&since_id=" + tsa.since_id)
except:
    print "LOG: error creating and executing search class"

'''process parsed results (pr)'''
#save the new max_id as the new since_id for the next search
since_id_file = open("since_id", 'w')
since_id_file.write(pr['max_id'])
since_id_file.close()




