# XIA

This tool is used to generate pedagogical html5 resources.
Thanks to it, you can generate three kinds of resources :
- first ones : Images actives. It is simple images on which we can make a focus on some details by zooming and adding descriptions.
- second ones : games using what we call the "1 click with scoring".
- third ones : games using what we call the "drag and drop with scoring" and "drag and drop without scoring" 

# Build application in Debian Jessie

First, install nodejs :

    apt-get install nodejs nodejs-legacy npm

nodejs-legacy is used to be able to call nodejs just with "node".
Finally, install grunt and lodash (used in this project):

    npm install -g grunt-cli
    npm install lodash

App pre-install (launch just once):

    cd project/upstream
    npm install

App install : (must be used each time we want a new release)

    cd project/upstream
    grunt default

Application is then built in project/upstream/build


# Build the debian package in Debian Jessie

    apt-get install --no-install-recommends --yes git openssl ca-certificates devscripts equivs lsb-release
    git clone 'http://gitlab.crdp.ac-versailles.fr:80/pascal.fautrero/images-actives-html5.git'
    cd images-actives-html5/packaging/
    mk-build-deps --install --tool 'apt-get --yes --no-install-recommends' --remove ./debian/control
    ./debian/rules populate_working_dir
    debuild -us -uc




