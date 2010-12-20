import logging
import tornado.auth
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import os
from tornado.options import define, options

define ("port", default=1337, help="porty port", type=int)
define ("address", default="0.0.0.0", help="dressy address", type=str)

class App(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", MainHandler),
		]
		settings = dict(
			debug=True,
			cookie_secret = "43oETzKXQAGaYdkL5gEmGeJJFu4h7E4np24dTP4o/Vo=",
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
		)
		
		tornado.web.Application.__init__(self, handlers, **settings)
		

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		if self.get_cookie("s1"):
			self.clear_cookie("s1")
		self.render("index.html")
		
	def post(self):
		i=self.get_argument("input")
		if not self.get_cookie("s1"):
			if i == "yes":
				self.write("Blue present or the red present?")
				self.set_cookie("s1","yes")
			elif i == "no":
				self.write("Very well then. No present for you!!!")
			else:
				self.write("North Pole had a glitch in the snowflake matrix. OMFG.!!!")
			return
		else:
			v=self.get_cookie("s1")

		if v == "confirmed":
			self.write("You're pushing your luck wee man.")
			return
			
		if v == "yes":	
			if i == "blue": 
				self.write("Too bad. I can not give to those that refuse my offer. Good bye.")		
			elif i == "red": 
				self.write("Yeeees. Excellent choice, kthx ? ")
				self.set_cookie("s1","red")
			else:
				self.write("North Pole had a glitch in the snowflake matrix. OMFG.")
			
		if v == "red":
			if i == "yes":
				self.write("Excellent. We must see the Icycle, she will tell you your fortune. Open up a web browser.<br/>")
				self.write("Go to: http://www.humblebundle.com/<br/>")
				self.write("This game bundle has been puchased in your name.<br/>")
				self.write("There are five days of secret santa, which game do you want to download first: <br/>")
				self.write("braid  |  cortex command  |  machinarium  |  osmos  |  renvenge  .  ?")
				self.set_cookie("s1","red|yes")
			elif i == "no":
				self.write("Do not lose faith so quick.")
			else:
				self.write("Your typing is good   ...  but these answers are not your technique. Stop playing around and answer me!!")
		
		if v == "red|yes":
				self.write("Enter in you email to get the download links.")
				f=open("/tmp/santagift.txt","w")
				f.write(i)
				f.close()
				self.set_cookie("s1","complete")
		
		if v == "complete":
			self.write("I will send 5 download links to your email, 1 per day. Write to supermatrixsanta@gmail.com for help in case you don't get your gift.")
			f=open("/tmp/santamail.txt","w")
			f.write(i)
			f.close()
			self.set_cookie("s1","confirmed")
			
				
def main():
	tornado.options.parse_command_line()
	app=App()
	app.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
	
if __name__ == '__main__':
	main()