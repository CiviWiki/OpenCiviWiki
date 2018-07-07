"use strict";
const path = require("path");

const webpack = require("webpack");

const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const BundleTracker = require("webpack-bundle-tracker");
const env = process.env.NODE_ENV || "development";

module.exports = {
  context: path.resolve(__dirname, "webapp"),
  entry: {
    app: "./src/js/app.js"
    // static: ["./static.js"]
  },
  output: {
    filename: "[name].[hash].js",
    path: path.resolve(__dirname, "webapp/static/bundles"),
    publicPath: ""
  },
  mode: "development",
  module: {
    rules: [
      {
        test: /\.html$/,
        loader: "underscore-template-loader",
        query: {
          interpolate: /\{\{=(.+?)\}\}/g,
          evaluate: /\{\{#(.+?)\}\}/g,
          escape: /\{\{(?!#|=)(.+?)\}\}/g
        }
      },
      {
        test: /\.less$/,
        use: [ 'style-loader', 'css-loader', 'less-loader']
      },
      {
        test: /\.css$/,
        use: [ 'style-loader', 'css-loader' ]
      },
      {
        test: /\.js?$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      },
      {
        test: /\.(png|jp(e*)g|svg)$/,
        use: [
          {
            loader: "url-loader",
            options: {
              limit: 5000,
              name: "img/[name].[hash].[ext]"
            }
          }
        ]
      },
      {
        test: /\.(woff|woff2|eot|ttf|otf)$/,
        use: ["file-loader"]
      }
    ]
  },
  plugins: [
    new BundleTracker({
      filename: "./webapp/static/webpack-stats.json"
    }),
    new webpack.ProvidePlugin({
      _: "underscore",
      $: "jquery",
      jQuery: "jquery"
    })
  ],
  resolve: {
    extensions: ["*", ".js"],
    modules: [
      'node_modules',
      'webapp/src',
    ],
    alias: {
      src: path.resolve(__dirname, "./src")
    }
  },
  resolveLoader: {
    moduleExtensions: ["-loader"]
  }
};
