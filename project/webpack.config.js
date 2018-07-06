"use strict";
const path = require("path");

const webpack = require("webpack");

const ExtractTextPlugin = require("extract-text-webpack-plugin");
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
        use: [
          {
            loader: "style-loader" // creates style nodes from JS strings
          },
          {
            loader: "css-loader" // translates CSS into CommonJS
          },
          {
            loader: "less-loader" // compiles Less to CSS
          }
        ]
      },
      {
        test: /\.js?$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      },
      {
        test: /\.css$/,
        exclude: /node_modules/,
        loader: ExtractTextPlugin.extract("style-loader", "css-loader")
      },
      {
        test: /\.(png|jp(e*)g|svg)$/,
        use: [
          {
            loader: "url-loader",
            options: {
              limit: 8000,
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
    new ExtractTextPlugin({
      filename: "[name].[hash].css"
    }),
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
    alias: {
      src: path.resolve(__dirname, "./src")
    }
  },
  resolveLoader: {
    moduleExtensions: ["-loader"]
  }
};
