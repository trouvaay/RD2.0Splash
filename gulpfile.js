var gulp = require('gulp'),
    gulpif = require('gulp-if'),
    inject = require('gulp-inject'),
    useref = require('gulp-useref'),
    uglify = require('gulp-uglify'),
    minifyCss = require('gulp-minify-css');

var mainBowerFiles = require('main-bower-files');


var config = {

  'src': 'src',
  'dest': 'dist',

  'styles': {
    'src' : 'src/css/**/*',
    'dest': 'dist/css',
  },

  'scripts': {
    'src' : 'src/js/**/*.js',
    'dest': 'dist/js',
  },

  'images': {
    'src' : 'src/img/**/*',
    'dest': 'dist/img',
  },

  'views': {
    'src': 'src/views/**/*.html',
    'dest': 'dist/views',
  },

  'bower': {
    'src': 'src/bower_components',
  },

  'main': {
    'src': 'src/*.html',
    'dest': 'dist',
  },
};


/* RESERVED
gulp.task('browserSync', function() {
  browserSync({
    browser: config.browser || 'google chrome',
    server: {
      baseDir: config.src,
    }
  });
});
*/


gulp.task('inject', function () {
  return gulp.src(config.main.src)
    .pipe(inject(gulp.src(mainBowerFiles(), {read: false}), {name: 'bower', relative: true}))
    .pipe(gulp.dest(config.src));
});


gulp.task('combine', function () {
  var assets = useref.assets();

  return gulp.src(config.main.src)
    .pipe(assets)
    .pipe(gulpif('**/app.js', uglify())) // uglify custom js only
    .pipe(gulpif('**/app.account.js', uglify())) // uglify custom js only
    .pipe(gulpif('**/app.css', minifyCss())) // inify custom css only
    .pipe(assets.restore())
    .pipe(useref())
    .pipe(gulp.dest(config.dest));
});


gulp.task('views', function () {
  return gulp.src(config.views.src)
    .pipe(gulp.dest(config.views.dest));
});


gulp.task('fonts', function() {
    // TODO: find better way to build fonts
    gulp.src([
        config.bower.src + '/weather-icons/font/*',
        ])
      .pipe(gulp.dest('dist/font'));

    return gulp.src([
        config.bower.src + '/fontawesome/fonts/*',
        config.src + '/vendor/theme/fonts/**/*',
        ])
      .pipe(gulp.dest('dist/fonts'));
});


gulp.task('images', function () {
  return gulp.src(config.images.src)
    .pipe(gulp.dest(config.images.dest));
});


gulp.task('install', ['inject'], function () {
  // Gerald, do something
});


gulp.task('build', ['combine', 'views', 'fonts', 'images'], function () {
  // Gerald, do something
});
