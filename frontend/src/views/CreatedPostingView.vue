<template>
  <div class="PostingView">
    <!-- <h1>This is an about page</h1> -->
    <CreateRole />
  </div>
</template>

<script>
// @ is an alias to /src
import CreateRole from "@/components/CreateRole.vue";

export default {
  name: "PostingView",
  components: {
    CreateRole,
  },
};
</script>
