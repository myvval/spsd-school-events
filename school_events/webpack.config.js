const path = require('path');

module.exports = {
  entry: {
    events: './src/components/EventsList.jsx',
    students: './src/components/StudentsList.jsx'
  },
  output: {
    path: path.resolve(__dirname, 'static/js'),
    filename: '[name].bundle.js'
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react']
          }
        }
      }
    ]
  },
  resolve: {
    extensions: ['.js', '.jsx']
  }
};
