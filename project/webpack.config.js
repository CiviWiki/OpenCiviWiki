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
      },
      {
        test: /\.less$/,
        use: ["less-loader"]
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
    // new CopyWebpackPlugin([
    //   {
    //     from: "./static/index.html",
    //     to: "./index.html"
    //   }
    // ]),
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
      "@": path.resolve(__dirname, "src"),
      "utils": path.resolve(__dirname, "./src/utils/"),
      "templates": path.resolve(__dirname, "./src/templates/")
    }
  },
  resolveLoader: {
    moduleExtensions: ["-loader"]
  }
};
