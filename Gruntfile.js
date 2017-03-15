module.exports = function(grunt) {

  var vendorsPath = 'build/share/vendors';
  var jqueryPath = 'bower_components/jquery/dist/jquery.min.js';
  var labjsPath = 'bower_components/labjs/LAB.min.js';
  var kineticPath = 'bower_components/kineticjs/kinetic.min.js';
  var bootstrapPath = 'bower_components/bootstrap/dist/js/bootstrap.min.js';

  var locales = ["en_US", "fr_FR", "pt_BR", "pt_PT"];

  var themesArray = [
      "accordionBlack",
      "accordionCloud",
      "audioBrown",
      "popBlue",
      "popYellow",
      "buttonBlue",
      "game1clic",
      "gameDragAndDrop",
      "material"
  ];

  var jsfiles = [
      "iaobject.js",
      "hooks.js",
      "iascene.js",
      "iframe.js",
      "main.js"
  ];

  var _ = require('lodash');
  var mos = _.map(locales, function(locale){
	  return 'build/share/i18n/' + locale + '/LC_MESSAGES/xia-converter.mo';
  });
  var pos = _.map(locales, function(locale){
	  return 'build/share/i18n/' + locale + '/LC_MESSAGES/xia-converter.po';
  });

  var xiajs = _.map(themesArray, function(theme){
	  return 'build/share/themes/' + theme + '/js/xia.js';
  });

  var jsfilestoconcat = _.map(themesArray, function(theme){
      var map = _.map(jsfiles, function(jsfile){
          return 'src/share/themes/' + theme + '/js/'+jsfile;
      });
      return map;
  });

  var jsfilestoremove = _.map(themesArray, function(theme){
      var map = _.map(jsfiles, function(jsfile){
          return 'build/share/themes/' + theme + '/js/'+jsfile;
      });
      return map;
  });

    // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    clean: {
        build: ['build'],
        js: jsfilestoremove
    },
    chmod: {
      options: {
        mode: '744'
      },
      yourTarget1: {
        // Target-specific file/dir lists and/or options go here.
        src: ['build/xia.py']
      }
    },
    copy: {
      main: {
        expand: true,
        src: '**',
        dest: 'build/',
        cwd    : 'src',
      },
      jquery: {
        files: [
            {dest: vendorsPath + "/jquery.min.js", src: jqueryPath}
        ]
      },
      labjs: {
        files: [
            {dest: vendorsPath + '/LAB.min.js', src:labjsPath}
        ]
      },
      kinetic: {
        files: [
            {dest: vendorsPath + '/kinetic.min.js', src:kineticPath}
        ]
      }
    },
    pot: {
      options:{
      text_domain: 'xia-converter', // Produces messages.pot
      dest: 'build/share/i18n/', // directory to place the pot file
      keywords: ['gettext', '__', 'translate'], // functions to look for
      encoding: 'UTF-8'
    },
    files:{
      src:  [ 'build/**/*.py' ],
      expand: true,
       }
    },
    dirs: {
        lang: 'build/share/i18n',
    },
    potomo: {
        dist: {
          files: _.object(mos, pos)
        }
    },
    shell: {
        options: {
          failOnError: true
        },
        msgmerge: {
          command: _.map(locales, function(locale) {
            var po = "build/share/i18n/" + locale + "/LC_MESSAGES/xia-converter.po";
            var po_src = "src/share/i18n/" + locale + "/LC_MESSAGES/xia-converter.po";
            return "if [ -f \"" + po + "\" ]; then\n" +
                       "    echo \"Updating " + po + "\"\n" +
                       "    msgmerge " + po + " build/share/i18n/xia-converter.pot > .new.po.tmp\n" +
                       "    exitCode=$?\n" +
                       "    if [ $exitCode -ne 0 ]; then\n" +
                       "        echo \"Msgmerge failed with exit code $?\"\n" +
                       "        exit $exitCode\n" +
                       "    fi\n" +
                       "    cp .new.po.tmp " + po + "\n" +
                       "    mv .new.po.tmp " + po_src + "\n" +
                       "else \n" +
                       "    cp build/share/i18n/xia-converter.pot " + po + "\n" +
                       "    cp build/share/i18n/xia-converter.pot " + po_src + "\n" +
                       "fi\n";
          }).join("")
        }
    },
    jshint: {
      options: {
        asi : true
      },
      all: ['Gruntfile.js', 'src/**/*.js', '!src/**/kinetic-xia.js', '!src/**/jquery-1.11.1.js', '!src/**/jquery.js', '!src/**/git-sha1.js', '!src/**/xorcipher.js', '!src/**/LAB.js', '!src/**/kinetic.js']
    },
    nose: {
     options: {
      verbosity: 2,
      with_coverage: true
     },
     src: ['tests']
    },
    uglify: {

      kinetic_xia: {
        files: {
          'build/share/themes/game1clic/js/kinetic-xia.min.js': ['src/share/themes/game1clic/js/kinetic-xia.js'],
          'build/share/themes/gameDragAndDrop/js/kinetic-xia.min.js': ['src/share/themes/gameDragAndDrop/js/kinetic-xia.js'],
        }
       }
    },
    concat: {
        options: {
          separator: ';',
        },
        jsfiles: {
            files: _.zipObject(xiajs,jsfilestoconcat)
        },
    }
  });

  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-potomo');
  grunt.loadNpmTasks('grunt-pot');
  grunt.loadNpmTasks('grunt-shell');
  grunt.loadNpmTasks('grunt-chmod');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-nose');
  grunt.loadNpmTasks('grunt-contrib-concat');

  grunt.registerTask('default', ['clean:build', 'copy:main' , 'pot', 'shell:msgmerge', 'potomo', 'chmod', 'concat:jsfiles', 'clean:js']);
  grunt.registerTask('minify', ['uglify:kinetic_xia']);
  grunt.registerTask('copy_vendors_js', ['copy:jquery' , 'copy:kinetic', 'copy:labjs']);

  grunt.registerTask('full', function(){
      grunt.task.run('default');
      grunt.task.run('copy_vendors_js');
      grunt.task.run('minify');
  });
  grunt.registerTask('debianbuild', function(){
      grunt.task.run('default');
      grunt.task.run('minify');
  });
  grunt.registerTask('dev', function(){
      grunt.task.run('default');
      grunt.task.run('copy_vendors_js');
  });
  grunt.registerTask('tests', ['jshint']);
};
