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
  created() {
    if (this.$store.state.logged_in_staff == null) {
      this.$router.push("/login")
    }
    var role = this.$store.state.logged_in_staff.role;
    switch(role) {
      case "User":
          this.$router.push('/apply-role');
          break;
      case "Manager":
          this.$router.push('/posting');
          break;
    }
  },
  props: ['roleID']
};
</script>
