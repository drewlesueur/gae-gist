from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch
import simplejson as json

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')
    
class Gist(webapp.RequestHandler):
    def get_gist(self,gist):
        url = "http://gist.github.com/raw/"+gist+"/index.py"
        result = urlfetch.fetch(url)
        if result.status_code == 200:
            return result.content 


    def get_gist_owner(self,gist):
        url = "http://gist.github.com/api/v1/json/" + gist
        result = urlfetch.fetch(url)
        if result.status_code == 200:
            ret = json.loads(result.content)
            owner = ret['gists'][0]['owner']
            return owner
        return ""
    
    def get(self, gist):
        owner = self.get_gist_owner(gist)
        if owner == 'drewlesueur':
            code = self.get_gist(gist)
            self.response.out.write("test")
            compiled = compile(code, '<string>', 'exec')
            exec compiled in {'self':self}
            
application = webapp.WSGIApplication(
                                     [('/', MainPage), (r'/gist/(.*)$',Gist)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()