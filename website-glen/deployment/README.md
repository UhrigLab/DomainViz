# Intro to the site
Hello! If you are reading this, you are probably trying to deploy, redeploy, or fix the Uhrig Lab DomainViz website. Thanks!

The way this site is organized is rather standard, however, I (Cameron Ridderikhoff) haven't fully separated the REST API/backend from the frontend.

The frontend is contained mainly within the `src` folder, but there are some important files contained within the `public` folder as well, namely `index.html`, `example_iframe.html` and `favicon.ico`. You can find these folders at the path: `Glen Website/website-glen/src` and `Glen Website/website-glen/public` respectively.

The api is contained in a folder aptly named: `api`. You can find this in the path: `Glen Website/website-glen/api`, however, this folder is mainly for Flask environment variables, and for Flask's wsgi.py file, which is the entrypoint for the backend's service. This will be further explained in *Section 2 - Backend Deployment*. You can find the Python files that contain the API endpoints in the `api/api` subfolder. Feel free to rename this if you like, but you will have to change the service files.


# Section 1 - Frontend Deployment
## Section 1.1 Redeploy - Frontend
The frontend deployment is quite easy, at least if you are redeploying the site, and not making too many major changes. There is a file within this folder `Glen Website/website-glen/deployment/redeploy.sh` that will automatically redeploy both the frontend and backend. However, this shell file isn't ideal, and could certainly use some updating (There is a TODO in the file if you want some more work).

This file needs to be run with `sudo`, so the full commands from logging onto the server should be:
### 1.1.1 IMPORTANT
```bash
$cd Website_Glen/website-glen/deployment
$sudo ./redeploy.sh
```

You may have to deal with npm (it has certainly been a struggle for me), and I find the best way to fix issues I am having with npm is to delete the `node_modules` folder and `package-lock.json` files, and then run `redeploy.sh`, which runs `npm install` to refresh your packages. This usually fixes enough npm package conflicts to allow the `redeploy.sh` to run to completition.

## Section 1.2 Fresh Deploy - Frontend
This guide only works for Linux distributions. If you have another OS that you are trying to serve this site from, you can loosely follow these instructions, but many may not work, or may have incorrect file paths.

If you run in the situation that Glen, or others, ask you to deploy the site onto a fresh Cirrus instance, or other cloud infrastructure (Azure/AWS/GCP, etc...) then you will need to do a bit more work. I have tried to list all of the steps below, but I may miss something, so stay sharp! (Note: you will also have to install the backend - see *Section 2.2 Fresh Deploy - Backend*)
1. Clone the repo
2. Install node and npm
3. Run `sudo npm install` in the `Website_Glen/website_glen` directory to ensure npm has correctly installed.
4. Create a SSL certificate using [certbot](https://certbot.eff.org/) NOTE: We are running `Nginx` on whatever Ubuntu/Linux distro you are using.
5. Ensure that the file paths of the certificate match those of the frontend service file (`Website_Glen/website-glen/deployment/prodoplot.nginx`):
```bash
$ssl_certificate /etc/letsencrypt/live/uhriglabdev.biology.ualberta.ca/fullchain.pem;
$ssl_certificate_key /etc/letsencrypt/live/uhriglabdev.biology.ualberta.ca/privkey.pem;
```
If they are not, either change the filepaths, or lines 8 and 9 of the frontend service file.
6. Copy the frontend service file  into the `/etc/nginx/sites-available/` folder
```bash
$sudo cp Website_Glen/website-glen/deployment/prodoplot.nginx /etc/nginx/sites-available/prodoplot.nginx
```
7. Create a soft-link from the sites-available folder to sites-enabled: 
```bash
$sudo ln /etc/nginx/sites-available/prodoplot.nginx /etc/nginx/sites-enabled/prodoplot.nginx
```
8. Reload Nginx: 
```bash
$sudo systemctl reload nginx
```

With all of this done, you should have a working frontend, that you can view in your web browser.

**RESOURCES**
Here are some of the videos/blogs that I used to learn how to deploy an Nginx site:
1. [How to Deploy a React + Flask App](https://blog.miguelgrinberg.com/post/how-to-deploy-a-react--flask-project)
2. [How to run Flask App on HTTPS](https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https)


# Section 2 - Backend Deployment
The backend is slightly more complex, but certainly manageable. It is quite easy to redeploy, but rather difficult to deploy fresh.

## Section 2.1 Redeploy - Backend
The backend deployment is quite easy, at least if you are redeploying the site, and not making too many major changes, much like the frontend. There is a file within this folder `Glen Website/website-glen/deployment/redeploy.sh` that will automatically redeploy both the frontend and backend. (See *Section 1.1 Redeploy - Frontend* for more details)

This file needs to be run with `sudo`, so the full commands from logging onto the server should be:
### 2.1.1 IMPORTANT
```bash
$cd Website_Glen/website-glen/deployment
$sudo ./redeploy.sh
```

Luckily python is nicer than npm, so usually modules aren't as big of an issue. However, if you run into any issues, install all packages inside the virtual environment by traveling to the first api folder and activate the virtual environment and install packages: 
```bash
$cd Website_Glen/website-glen/api/
$source venv/bin/activate
$pip3 install -r requirements.flask.txt
``` 
Then navigate to the second api folder and activate the virtual environment and install packages: 
```bash
$cd Website_Glen/website-glen/api/api/
$source propplotenv/bin/activate
$pip3 install -r requirements.domainviz.txt
```

If you add more packages to the backend, add them to `requirements.flask.txt`.

## Section 2.2 Fresh Deploy - Backend
This guide only works for Linux distributions. If you have another OS that you are trying to serve this site from, you can loosely follow these instructions, but many may not work, or may have incorrect file paths.

The same applies for backend as for frontend.
1. Clone the repo
2. Install python3.8 [Downloads Page](https://www.python.org/downloads/release/python-3811/)
3. Install python3 virtual environment 
```bash
$sudo python3 -m pip install --user virtualenv
```
4. Create a virtual environment for the backend in the `Website_Glen/website-glen/api/` directory: 
```bash
$sudo python3 -m venv venv
```
5. Activate the virtual environment: 
```bash
$source venv/bin/activate
```
6. Deactivate the environment: 
```bash
$deactivate
```
7. Install packages: 
```bash
$pip install -r requirements.flask.txt
```
8. Create a virtual environment for domainviz.py in the `Website_Glen/website-glen/api/api/` directory: 
```bash
$sudo python3 -m venv protplotenv
```
9. Activate the virtual environment: 
```bash
$source venv/bin/activate
```
10. Install packages: 
```bash
$pip install -r requirements.domainviz.txt
```
11. Deactivate the environment: 
```bash
$deactivate
```
12. Copy the backend service file from the `Website_Glen/website_glen/deployment` folder into the `/etc/systemd/system/` folder: 
```bash
$sudo cp prodoplot.service /etc/systemd/system/prodoplot.service
```
13. Run the service: 
```bash
$sudo systemctl daemon-reload
$sudo systemctl start prodoplot.service
```

With all of this done, you should have a working backend, and you can check that it is running by running the command:
```bash
$sudo systemctl status prodoplot
```
It should say "active (running)" in green text, and have a green dot by the `prodoplot.service` name. Press `CTL+C` to exit.