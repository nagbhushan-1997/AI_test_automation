```html
<template>
  <form @submit.prevent="submit">
    <!-- Form fields and buttons -->
  </form>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  methods: {
    submit() {
      // Form submission logic
    }
  },
});
</script>

<style scoped>
button {
  background-color: #42b983;
  color: white;
  border: none;
  /* Added CSS variable for better maintainability */
  --primary-color: #42b983;

  background-color: var(--primary-color);
}
</style>
```