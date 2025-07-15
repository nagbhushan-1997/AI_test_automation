module.exports = {
  presets: [
    '@vue/cli-plugin-babel/preset'
  ]
}
// This file is used to configure Babel for the Vue.js project.
// Babel is a JavaScript compiler that allows you to use next generation JavaScript,
// transforming it into a version that is compatible with older browsers.
// The '@vue/cli-plugin-babel/preset' preset includes the necessary plugins and configurations
// to work with Vue.js applications, ensuring that the code is transpiled correctly.
// You can add additional plugins or presets as needed for your project.
// For more information on Babel and its configuration, you can refer to the official documentation:
// https://babeljs.io/docs/en/configuration
// https://cli.vuejs.org/guide/babel.html
// This file is typically located in the root directory of your Vue.js project.
// It is automatically created when you set up a Vue.js project using the Vue CLI.
// You can modify this file to customize the Babel configuration for your project.
// If you need to support specific browsers or environments, you can add the 'targets' option
// to the configuration. For example:
// module.exports = {
//   presets: [
//     ['@vue/cli-plugin-babel/preset', {
//       targets: {
//         browsers: ['> 1%', 'last 2 versions', 'not ie <= 11']
//       }
//     }]
//   ]