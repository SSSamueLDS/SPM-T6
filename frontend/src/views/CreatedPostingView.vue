<template>
  <div class="PostingView">
    <RoleForm mode="create" />
    <!-- <RoleForm mode="edit" /> -->
  </div>
</template>

<script>
// @ is an alias to /src
import RoleForm from "@/components/RoleForm.vue";

export default {
  name: "PostingView",
  components: {
    RoleForm,
  },
};
</script>
