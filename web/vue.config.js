const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

module.exports = {
  devServer: {
    proxy: {
      '^/v1': {
        target: 'http://127.0.0.1:8000',
        ws: true,
        changeOrigin: true
      },
    }
  }
}