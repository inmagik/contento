var path = require('path');
var webpack = require('webpack');

module.exports = {
  devtool: 'cheap-module-eval-source-map',
  entry: [
    './src/index.js',
  ],
	output: {
		path: path.join(__dirname, '../static/contento/dashboard/js'),
    filename: 'jshook.js',
		library: 'JsHook',
		libraryTarget: 'umd',
    publicPath: '/static/contento/dashboard/js/'
  },
  plugins: [
    new webpack.NoErrorsPlugin(),
  ],
  module: {
    loaders: [
      {
        test: /\.jsx?$/,
        loader: 'babel',
        exclude: /node_modules/,
        include: __dirname
      }
    ]
  }
};
