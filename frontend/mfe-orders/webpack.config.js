const HtmlWebpackPlugin = require("html-webpack-plugin");
const ModuleFederationPlugin = require("webpack/lib/container/ModuleFederationPlugin");
const webpack = require("webpack");
const path = require("path");

module.exports = {
  entry: "./src/index.js",
  mode: process.env.NODE_ENV || "development",
  devServer: {
    port: 3001,
    historyApiFallback: true,
    headers: { "Access-Control-Allow-Origin": "*" },
  },
  output: {
    publicPath: "auto",
    path: path.resolve(__dirname, "dist"),
    clean: true,
  },
  resolve: { extensions: [".js", ".jsx"] },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/preset-env", "@babel/preset-react"],
          },
        },
      },
      { test: /\.css$/, use: ["style-loader", "css-loader"] },
    ],
  },
  plugins: [
    new ModuleFederationPlugin({
      name: "mfe_orders",
      filename: "remoteEntry.js",
      exposes: {
        "./OrdersApp": "./src/OrdersApp",
      },
      shared: {
        react: { singleton: true, requiredVersion: "^18.3.0" },
        "react-dom": { singleton: true, requiredVersion: "^18.3.0" },
        "react-router-dom": { singleton: true },
      },
    }),
    new HtmlWebpackPlugin({ template: "./public/index.html" }),
    new webpack.DefinePlugin({
      "process.env.NODE_ENV": JSON.stringify(process.env.NODE_ENV || "development"),
      "process.env.ORDERS_API_URL": JSON.stringify(process.env.ORDERS_API_URL || ""),
    }),
  ],
};
