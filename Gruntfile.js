module.exports = function(grunt) {
    
  var vendorsPath = 'build/share/vendors';
  var jqueryPath = 'bower_components/jquery/dist/jquery.min.js';    
  var labjsPath = 'bower_components/labjs/LAB.min.js';
  var kineticPath = 'bower_components/kineticjs/kinetic.min.js';
  var bootstrapPath = 'bower_components/bootstrap/dist/js/bootstrap.min.js';
  
  var locales = ["en_US", "fr_FR"];
  var _ = require('lodash');  
  var mos = _.map(locales, function(locale){
	  return 'build/share/i18n/' + locale + '/LC_MESSAGES/xia-converter.mo';
  });
  var pos = _.map(locales, function(locale){
	  return 'build/share/i18n/' + locale + '/LC_MESSAGES/xia-converter.po';
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
      },
      bootstrap: {
        files: [
            {dest: vendorsPath + '/bootstrap.min.js', src:bootstrapPath}
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

      kinetic: {
        files: {
          'build/share/themes/game1clic/js/kinetic-xia.js': ['src/share/themes/game1clic/js/kinetic-xia.js'],          
          'build/share/themes/gameDragAndDrop/js/kinetic-xia.js': ['src/share/themes/gameDragAndDrop/js/kinetic-xia.js'],
        }
       }      
    },
    concat: {
        options: {
          separator: ';',
        },
        build: {
            files: {
                'build/share/themes/accordionBlack/js/xia.js': ['src/share/themes/accordionBlack/js/iascene.js',
                                                                'src/share/themes/accordionBlack/js/hooks.js',
                                                                'src/share/themes/accordionBlack/js/iaobject.js',
                                                                'src/share/themes/accordionBlack/js/iframe.js',
                                                                'src/share/themes/accordionBlack/js/main.js',
                                                                ],
                'build/share/themes/accordionCloud/js/xia.js': ['src/share/themes/accordionCloud/js/iascene.js',
                                                                'src/share/themes/accordionCloud/js/hooks.js',
                                                                'src/share/themes/accordionCloud/js/iaobject.js',
                                                                'src/share/themes/accordionCloud/js/iframe.js',
                                                                'src/share/themes/accordionCloud/js/main.js',
                                                                ], 
                'build/share/themes/audioBrown/js/xia.js': ['src/share/themes/audioBrown/js/iascene.js',
                                                                'src/share/themes/audioBrown/js/hooks.js',
                                                                'src/share/themes/audioBrown/js/iaobject.js',
                                                                'src/share/themes/audioBrown/js/iframe.js',
                                                                'src/share/themes/audioBrown/js/main.js',
                                                                ],
                'build/share/themes/buttonBlue/js/xia.js': ['src/share/themes/buttonBlue/js/iascene.js',
                                                                'src/share/themes/buttonBlue/js/hooks.js',
                                                                'src/share/themes/buttonBlue/js/iaobject.js',
                                                                'src/share/themes/buttonBlue/js/iframe.js',
                                                                'src/share/themes/buttonBlue/js/main.js',
                                                                ],
                'build/share/themes/popBlue/js/xia.js': ['src/share/themes/popBlue/js/iascene.js',
                                                                'src/share/themes/popBlue/js/hooks.js',
                                                                'src/share/themes/popBlue/js/iaobject.js',
                                                                'src/share/themes/popBlue/js/iframe.js',
                                                                'src/share/themes/popBlue/js/main.js',
                                                                ],
                'build/share/themes/popYellow/js/xia.js': ['src/share/themes/popYellow/js/iascene.js',
                                                                'src/share/themes/popYellow/js/hooks.js',
                                                                'src/share/themes/popYellow/js/iaobject.js',
                                                                'src/share/themes/popYellow/js/iframe.js',
                                                                'src/share/themes/popYellow/js/main.js',
                                                                ],
                'build/share/themes/game1clic/js/xia.js': ['src/share/themes/game1clic/js/iascene.js',
                                                                'src/share/themes/game1clic/js/hooks.js',
                                                                'src/share/themes/game1clic/js/iaobject.js',
                                                                'src/share/themes/game1clic/js/iframe.js',
                                                                'src/share/themes/game1clic/js/main.js',
                                                                ],
                'build/share/themes/gameDragAndDrop/js/xia.js': ['src/share/themes/gameDragAndDrop/js/iascene.js',
                                                                'src/share/themes/gameDragAndDrop/js/hooks.js',
                                                                'src/share/themes/gameDragAndDrop/js/iaobject.js',
                                                                'src/share/themes/gameDragAndDrop/js/iframe.js',
                                                                'src/share/themes/gameDragAndDrop/js/main.js',
                                                                ]
            }
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
  grunt.registerTask('default', ['clean', 'copy:main' , 'copy:jquery' , 'copy:kinetic', 'copy:labjs', 'copy:bootstrap','pot',  'shell:msgmerge', 'potomo', 'chmod', 'uglify:kinetic', 'concat:build']);
  grunt.registerTask('tests', ['jshint']);
  grunt.registerTask('dev', ['clean', 'copy:main' , 'copy:jquery' , 'copy:kinetic', 'copy:labjs', 'copy:bootstrap', 'pot',  'shell:msgmerge', 'potomo', 'chmod']);
  grunt.registerTask('debianbuild', ['clean', 'copy:main' , 'pot',  'shell:msgmerge', 'potomo', 'chmod']);
};


