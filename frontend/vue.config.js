// 跨域代理，重定向到后端

module.exports = {
  runtimeCompiler: true,
  publicPath: "/", // 设置打包文件相对路径
  outputDir: "dist", // 构建时输出的目录根路径
  // assertDir: 'static',  // 放置静态资源的目录
  // indexPath: 'index.html', // HTML 输出的路径
  devServer: {
    // proxy: "http://localhost:8000",
    port: "8080",
    proxy: {
      "/api": {
        // 配置到接口包含 api 使用该代理
        target: "http://127.0.0.1:8000/api", // 定义后端的接口
        changeOrigin: true,
        ws: true,
        pathRewrite: {
          "^/api": "",
        },
      },
      static: {
        target: "http://127.0.0.1:8000/static", // 定义后端接口
        changeOrigin: true,
        ws: true,
        pathRewrite: {
          "^/static": "",
        },
      },
    },
  },
};
