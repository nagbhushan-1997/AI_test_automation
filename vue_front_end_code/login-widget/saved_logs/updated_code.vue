```vue
<template>
  <div class="login-form">
    <form @submit.prevent="handleSubmit" @error="handleError">
      <!-- Form fields and inputs -->
      <button type="submit" class="btn btn-primary">Login</button>
      <p v-if="error" class="error-message">{{ error }}</p>
    </form>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';

export default {
  setup() {
    const formData = ref({});

    const handleSubmit = () => {
      // Handle form submission logic here
      submitFormData();
    };

    const handleErrors = (error) => {
      this.error = error;
      console.error(error);
    };

    const submitFormData = async () => {
      try {
        // Send form data to server-side endpoint for validation and processing
        await fetch('/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData.value),
        });
        this.error = '';
      } catch (error) {
        handleErrors(error);
      }
    };

    onMounted(() => {
      // Reset form data when component is mounted
      formData.value = {};
    });

    return { formData, handleSubmit };
  }
}
</script>

<style scoped>
.login-form {
  max-width: 300px;
  margin: 50px auto;
}

.btn {
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px; /* Consistent border radius value */
  padding: 10px 20px;
  cursor: pointer;
}

.btn:hover {
  background-color: #3e8e41;
}
</style>
```