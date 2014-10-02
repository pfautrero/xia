module.exports = function(grunt) {
  var locales = ["en_US", "fr_FR"];
  var _ = require('lodash');  
  var mos = _.map(locales, function(locale){
	  return 'build/share/i18n/' + locale + '/LC_MESSAGES/messages.mo';
  });
  var pos = _.map(locales, function(locale){
	  return 'build/share/i18n/' + locale + '/LC_MESSAGES/messages.po';
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
        src: ['build/converter/xia.py']
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
            var po = "build/share/i18n/" + locale + "/LC_MESSAGES/messages.po";
            var po_src = "src/share/i18n/" + locale + "/LC_MESSAGES/messages.po";
            return "if [ -f \"" + po + "\" ]; then\n" +
                       "    echo \"Updating " + po + "\"\n" +
                       "    msgmerge " + po + " build/share/i18n/messages.pot > .new.po.tmp\n" +
                       "    exitCode=$?\n" +
                       "    if [ $exitCode -ne 0 ]; then\n" +
                       "        echo \"Msgmerge failed with exit code $?\"\n" +
                       "        exit $exitCode\n" +
                       "    fi\n" +
                       "    cp .new.po.tmp " + po + "\n" +
                       "    mv .new.po.tmp " + po_src + "\n" +                       
                       "else \n" + 
                       "    cp build/share/i18n/messages.pot " + po + "\n" + 
                       "    cp build/share/i18n/messages.pot " + po_src + "\n" +                        
                       "fi\n";
          }).join("")
        }
    },
    jshint: {
      all: ['Gruntfile.js', 'src/**/*.js', '!src/**/jquery-1.11.1.js', '!src/**/LAB.js', '!src/**/kinetic.js', '!src/**/bootstrap.min.js']
    },
    nose: {
     options: {
      verbosity: 2,
      with_coverage: true
     },
     src: ['tests']
    },
    uglify: {
      jquery: {
        files: {
          'build/share/themes/accordionBlack/js/jquery-1.11.1.js': ['src/share/themes/accordionBlack/js/jquery-1.11.1.js'],
          'build/share/themes/accordionCloud/js/jquery-1.11.1.js': ['src/share/themes/accordionCloud/js/jquery-1.11.1.js'],
          'build/share/themes/audioBrown/js/jquery-1.11.1.js': ['src/share/themes/audioBrown/js/jquery-1.11.1.js'],
          'build/share/themes/buttonBlue/js/jquery-1.11.1.js': ['src/share/themes/buttonBlue/js/jquery-1.11.1.js'],
          'build/share/themes/game1clic/js/jquery-1.11.1.js': ['src/share/themes/game1clic/js/jquery-1.11.1.js'],          
          'build/share/themes/gameDragAndDrop/js/jquery-1.11.1.js': ['src/share/themes/gameDragAndDrop/js/jquery-1.11.1.js'],
          'build/share/themes/popBlue/js/jquery-1.11.1.js': ['src/share/themes/popBlue/js/jquery-1.11.1.js'],
          'build/share/themes/popYellow/js/jquery-1.11.1.js': ['src/share/themes/popYellow/js/jquery-1.11.1.js']
        }
      },
      kinetic: {
        files: {
          'build/share/themes/accordionBlack/js/kinetic.js': ['src/share/themes/accordionBlack/js/kinetic.js'],
          'build/share/themes/accordionCloud/js/kinetic.js': ['src/share/themes/accordionCloud/js/kinetic.js'],
          'build/share/themes/audioBrown/js/kinetic.js': ['src/share/themes/audioBrown/js/kinetic.js'],
          'build/share/themes/buttonBlue/js/kinetic.js': ['src/share/themes/buttonBlue/js/kinetic.js'],
          'build/share/themes/game1clic/js/kinetic.js': ['src/share/themes/game1clic/js/kinetic.js'],          
          'build/share/themes/gameDragAndDrop/js/kinetic.js': ['src/share/themes/gameDragAndDrop/js/kinetic.js'],
          'build/share/themes/popBlue/js/kinetic.js': ['src/share/themes/popBlue/js/kinetic.js'],
          'build/share/themes/popYellow/js/kinetic.js': ['src/share/themes/popYellow/js/kinetic.js']
        }
       },

       labjs: {
        files: {
          'build/share/themes/accordionBlack/js/LAB.js': ['src/share/themes/accordionBlack/js/LAB.js'],
          'build/share/themes/accordionCloud/js/LAB.js': ['src/share/themes/accordionCloud/js/LAB.js'],
          'build/share/themes/audioBrown/js/LAB.js': ['src/share/themes/audioBrown/js/LAB.js'],
          'build/share/themes/buttonBlue/js/LAB.js': ['src/share/themes/buttonBlue/js/LAB.js'],
          'build/share/themes/game1clic/js/LAB.js': ['src/share/themes/game1clic/js/LAB.js'],          
          'build/share/themes/gameDragAndDrop/js/LAB.js': ['src/share/themes/gameDragAndDrop/js/LAB.js'],
          'build/share/themes/popBlue/js/LAB.js': ['src/share/themes/popBlue/js/LAB.js'],
          'build/share/themes/popYellow/js/LAB.js': ['src/share/themes/popYellow/js/LAB.js']
        }        
      }      
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
  grunt.registerTask('default', ['clean', 'copy', 'pot',  'shell:msgmerge', 'potomo', 'chmod', 'uglify:jquery', 'uglify:kinetic', 'uglify:labjs']);
  grunt.registerTask('tests', ['jshint']);
  grunt.registerTask('dev', ['clean', 'copy', 'pot',  'shell:msgmerge', 'potomo', 'chmod']);
};
