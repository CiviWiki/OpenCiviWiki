'use strict';
const path = require('path');

const webpack = require('webpack');
const merge = require('webpack-merge');

const ExtractTextPlugin = require('extract-text-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = {
    entry: {
        app: ['./webapp/src/js/index.js']
    },
    output: {
        filename: '[name].[hash].js',
        path: path.resolve(__dirname, 'webapp/src/dist')
    },
    mode: 'development',
    devtool: 'inline-source-map',
    module: {
        rules: [{
                test: /\.less$/,
                use: [
                    'style-loader',
                    'css-loader',
                    'less-loader'
                ]
            }, {
                test: /\.js?$/,
                exclude: /node_modules/,
                loader: 'babel',
                query: {
                    presets: ['es2015']
                }
            },
            {
                test: /\.jst$/,
                loader: 'underscore-template-loader'
            },
            {
                test: /\.css$/,
                exclude: /node_modules/,
                loader: ExtractTextPlugin.extract('style-loader', 'css-loader')
            }
        ],
    },
    plugins: [
        new ExtractTextPlugin({
            filename: "[name].[hash].css",
            disable: process.env.NODE_ENV === "development"
        }),
        new CopyWebpackPlugin([{
            from: './webapp/static/index.html',
            to: './index.html'
        }]),
        new webpack.ProvidePlugin({
            _: 'underscore',
            $: 'jquery',
            jQuery: 'jquery',
            Backbone: 'backbone',
            Bb: 'backbone',
            Marionette: 'backbone.marionette',
            Mn: 'backbone.marionette',
        }),
    ],
    resolveLoader: {
        moduleExtensions: ['-loader']
    },
};
