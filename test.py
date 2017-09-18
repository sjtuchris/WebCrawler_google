import urllib2

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

url = "https://www.google.com/search?q=dog"
headers={'User-Agent':user_agent,}

request=urllib2.Request(url,None,headers)
response = urllib2.urlopen(request)
data = response.read()
print data
