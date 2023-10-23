<template>
  <div>Hello World</div>
</template>

<script>
// @ is an alias to /src
export default {
  created() {
    this.$router.push('/login');
  },
}
</script>
