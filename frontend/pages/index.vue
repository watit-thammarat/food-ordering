<template>
  <div>
    <h1>{{ message }}</h1>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  asyncData(context) {
    return axios
      .get('http://localhost:8000')
      .then(({ data }) => {
        return { message: data.data };
      })
      .catch(err => console.log(err));
  }
};
</script>

<style scoped>
</style>
