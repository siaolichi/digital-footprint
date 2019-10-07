const path = require('path');
module.exports = {
    entry: ['@babel/polyfill', './jsx/App.jsx'],
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: 'App.js'
    },
    mode: 'development',
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader",
                    options: { 
                        presets: ["@babel/preset-env", "@babel/preset-react"], 
                        plugins: ["@babel/plugin-proposal-class-properties"]
                    }
                }
            },
            {
                test: /\.css$/i,
                use: ['style-loader', 'css-loader'],
            },
            {
                test: /\.scss$/i,
                use: ['style-loader', 'css-loader', 'sass-loader'],
            },
            {
                test: /\.(jpe?g|gif|png|svg)$/i,
                use: [
                {
                  loader: 'url-loader',
                  options: {
                    limit: 10000
                  }
                }
              ]
            }
        ]
    }
};