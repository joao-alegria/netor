const webpack = require('webpack');

module.exports = {
  plugins: [
    new webpack.DefinePlugin({
      $ENV: {
        NETOR_ENDPOINT: JSON.stringify(process.env.NETOR_ENDPOINT)
      }
    })
  ]
};