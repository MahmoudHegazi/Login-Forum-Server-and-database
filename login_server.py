from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from users import Base, Users, Info
import cgi

engine = create_engine('sqlite:///users.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

users = []
passwords = []
search = session.query(Info).all()

        

class WebServerHandler(BaseHTTPRequestHandler):
    
        def do_GET(self):
            try:
                
                if self.path.endswith('/login'):
                    self.send_response(200)
                    self.send_header('Content-type','text-html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/login'>"
                    output += "UserName: <input name='user' type='text' placeholder='Enter User Name'><br><br>"
                    output += "Password: <input name='password' type='password' placeholder='Enter Password'>"
                    output += "<br><br>"
                    output += "<input type='submit' value='Login'>"
                    output += "</form></body></html>"
                    self.wfile.write(output)
                    print output
                    return


            except IOError:
                self.send_error(404, 'File Not Found: %s' % self.path)


        def do_POST(self):
            
            try:
                    
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                        
                user = fields.get('user')
                password = fields.get('password')               
                    
                for i in search:
                        
                        if user[0] == str(i.user) and password[0] == i.password:
                            x = session.query(Users).filter_by(id = i.user_id).one()                            
                            self.send_response(301)
                            self.send_header('Content-type','text-html')
                            self.end_headers()                          
                            
                            output = ""
                            output += "<html><body>"
                            output += "<h2>Login Accepted Hello Mr: %s </h2>" % x.name
                            output += "</body></html>"
                            self.wfile.write(output)
                            print "Works Very Well"
                            print user[0]
                            print i.user
                            print password[0]
                            print i.password
                            return
      
                else:
                    self.send_response(301)
                    self.send_header('Content-type','text-html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h2>Sorry Invalid User Or Password</h2>"
                    output += "<a href='/login'>Try Agin</a>"
                    output += "</body></html>"
                    self.wfile.write(output)
                        
                    print "Wrong User or password"                   

                    return
                                        
                    
                    
                  
                            

            except:
                print "anything"
                pass




def main():
    try:
        
        port = 8080
        server = HTTPServer(('',port),WebServerHandler)
        print "Server Is Now Runing on Port %s " % port
        server.serve_forever()

    except:
        print "^ C Entered Server Is Now Clossing..."
        server.socket.close()


if __name__ == '__main__':
    main()
    
