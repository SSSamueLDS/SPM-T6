<template>
  <div class="EditPostingView">
    <EditRoleForm :role_ID=Number(roleID) />
  </div>
</template>

<script>
// @ is an alias to /src
import EditRoleForm from "@/components/EditRoleForm.vue";

export default {
  name: "EditPostingView",
  components: {
    EditRoleForm,
  },
  props: ['roleID']
};
</script>
