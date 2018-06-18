"use strict";
const path = require("path");

const webpack = require("webpack");

const ExtractTextPlugin = require("extract-text-webpack-plugin");
const CopyWebpackPlugin = require("copy-webpack-plugin");
const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  entry: {
    context: path.join(__dirname, "webapp", "src"),
    app: ["./index.js"]
  },
  output: {
    filename: "[name].[hash].js",
    path: path.resolve(__dirname, "webapp/src/dist")
  },
  mode: "development",
  devtool: "inline-source-map",
  module: {
    rules: [
      {
        test: /\.html$/,
        loader: "underscore-template-loader",
        query: {
          interpolate: "\\{\\{#(.+?)\\}\\}",
          evaluate: "\\{\\{=(.+?)\\}\\}",
          escape: "\\{\\{(?!#|=)(.+?)\\}\\}"
        }
      },
      {
        test: /\.less$/,
        use: ["style-loader", "css-loader", "less-loader"]
      },
      {
        test: /\.js?$/,
        exclude: /node_modules/,
        loader: "babel",
        query: {
          presets: ["es2015"]
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
    new CopyWebpackPlugin([
      {
        from: "./webapp/static/index.html",
        to: "./index.html"
      }
    ]),
    new BundleTracker({
      filename: "./static/webpack-stats.json"
    }),
    new webpack.ProvidePlugin({
      _: "underscore",
      $: "jquery",
      jQuery: "jquery",
      Backbone: "backbone",
      Bb: "backbone",
      Marionette: "backbone.marionette",
      Mn: "backbone.marionette"
    })
  ],
  resolveLoader: {
    moduleExtensions: ["-loader"]
  }
};
