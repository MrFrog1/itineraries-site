const path = require('path');

module.exports = {
  entry: './itins/frontend/src/index.js',
  // Define output path and filename
  output: {
    path: path.resolve(__dirname, 'itins/frontend/static/frontend'),
    filename: 'main.js',
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      }
    ]
  }
  // Include other configurations like output, plugins, etc., as necessary
};