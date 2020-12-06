from api.__init__ import create_app
app=create_app()

if __name__ == '__main__':
	app.run(ssl_context=('/etc/letsencrypt/live/uhrigprotools.biology.ualberta.ca/fullchain.pem', '/etc/letsencrypt/live/uhrigprotools.biology.ualberta.ca/privkey.pem'))
