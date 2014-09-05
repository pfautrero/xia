module.exports = function(grunt) {
  var locales = ["en", "fr"];
  var _ = require('lodash');  
  var mos = _.map(locales, function(locale){
	  return 'build/converter/i18n/' + locale + '/LC_MESSAGES/messages.mo';
  });
  var pos = _.map(locales, function(locale){
	  return 'build/converter/i18n/' + locale + '/LC_MESSAGES/messages.po';
  });


  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    clean: ['build'],
    chmod: {
      options: {
        mode: '744'
      },
      yourTarget1: {
        // Target-specific file/dir lists and/or options go here.
        src: ['build/converter/activit.py']
      }
    },
    copy: {
      main: {
        expand: true,
        src: '**',
        dest: 'build/',
        cwd    : 'src',
      },
    },
    pot: {
      options:{
      text_domain: 'messages', // Produces messages.pot
      dest: 'build/converter/i18n/', // directory to place the pot file
      keywords: ['gettext', '__'], // functions to look for
      encoding: 'UTF-8'
    },
    files:{
      src:  [ 'build/**/*.py' ],
      expand: true,
       }
    },
    dirs: {
        lang: 'build/converter/i18n',
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
            var po = "build/converter/i18n/" + locale + "/LC_MESSAGES/messages.po";
            var po_src = "src/converter/i18n/" + locale + "/LC_MESSAGES/messages.po";
            return "if [ -f \"" + po + "\" ]; then\n" +
                       "    echo \"Updating " + po + "\"\n" +
                       "    msgmerge " + po + " build/converter/i18n/messages.pot > .new.po.tmp\n" +
                       "    exitCode=$?\n" +
                       "    if [ $exitCode -ne 0 ]; then\n" +
                       "        echo \"Msgmerge failed with exit code $?\"\n" +
                       "        exit $exitCode\n" +
                       "    fi\n" +
                       "    cp .new.po.tmp " + po + "\n" +
                       "    mv .new.po.tmp " + po_src + "\n" +                       
                       "else \n" + 
                       "    cp build/converter/i18n/messages.pot " + po + "\n" + 
                       "    cp build/converter/i18n/messages.pot " + po_src + "\n" +                        
                       "fi\n";
          }).join("")
        }
    },
    jshint: {
      all: ['Gruntfile.js', 'src/**/*.js', '!src/**/jquery-1.11.1.js', '!src/**/LAB.min.js', '!src/**/kinetic.js', '!src/**/bootstrap.min.js']
    }    
  });

  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-potomo');
  grunt.loadNpmTasks('grunt-pot');
  grunt.loadNpmTasks('grunt-shell');
  grunt.loadNpmTasks('grunt-chmod');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.registerTask('default', ['clean', 'copy', 'pot',  'shell:msgmerge', 'potomo', 'chmod']);
  grunt.registerTask('dev', ['jshint']);
};
