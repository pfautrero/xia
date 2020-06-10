#Build XIA application in Debian Jessie

```sh
apt-get install -y libjavascript-minifier-perl gettext python
cd project
python setup.py buildstandalone
```

# Build application everywhere (using grunt/bower)

**Beware: not working anymore**

First, install nodejs :

```
apt-get install nodejs nodejs-legacy npm
```

nodejs-legacy is used to be able to call nodejs just with "node".
Finally, install grunt and lodash (used in this project):

```
npm install -g grunt-cli
npm install lodash
npm install -g bower
```

App pre-install (launch just once):

```
cd project
npm install
bower install
```

App install : (must be used each time we want a new release)

```
cd project
grunt full
```

Application is then built in project/build
