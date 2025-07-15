<template>
  <div class="login-container">
    <div class="login-box">
      <h2>Login</h2>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>Email</label>
          <input type="email" v-model="email" required />
        </div>
        <div class="form-group">
          <label>Password</label>
          <input type="password" v-model="password" required />
        </div>
        
        <div class="form-group button-group">
          <button type="submit">Submit</button>
          <button type="button" @click="handleCancel" class="cancel-button">Cancel</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginForm',
  data() {
    return {
      email: '',
      password: ''
    };
  },
  methods: {
    handleSubmit() {
      alert(`Email: ${this.email}\nPassword: ${this.password}`);
    },
    handleCancel() {
      this.email = '';
      this.password = '';
    }
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: black;
}
.login-box {
  width: 300px;
  margin: 100px auto;
  padding: 25px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: white;
}
.form-group {
  margin-bottom: 15px;
}
input {
  width: 100%;
  padding: 8px;
}
.button-group {
  display: flex;
  justify-content: space-between;
}
button {
  padding: 10px;
  background-color: green;
  color: white;
  border: none;
  border-radius: 4px;
  width: 48%;
}
.cancel-button {
  background-color: red;
}
</style>
