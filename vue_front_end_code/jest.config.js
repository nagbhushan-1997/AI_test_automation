module.exports = {
  testEnvironment: 'jsdom',
  moduleFileExtensions: ['js', 'json', 'vue'],
  transform: {
    '^.+\\.vue$': 'vue-jest',
    '^.+\\.js$': 'babel-jest',
  },
  testMatch: [
  ".\\vue_front_end_code\\login-widget\\tests\\unit\\components\\LoginForm.spec.js"
], // add this line
};