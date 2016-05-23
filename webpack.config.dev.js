const path = require('path');
const ROOT_PATH = path.resolve(__dirname);
const webpack = require('webpack');

module.exports = {
  entry: path.resolve(ROOT_PATH,
      'brp/static/embark/index'),
  output: {
    path: path.resolve(ROOT_PATH, 'brp/static/embark/build'),
    filename: 'bundle.js',
  },
  module: {
    loaders: [
      {
        test: /\.js$/,
        loaders: ['babel'],
        exclude: /node_modules/,
      },
    ],
  },
  externals: {
  },
  resolve: {
    extensions: ['', '.js', '.jsx'],
  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': '"development"',
    }),
  ],
};
