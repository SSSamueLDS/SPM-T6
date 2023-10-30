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
  created() {
    if (this.$store.state.logged_in_staff == null) {
      this.$router.push("/login")
    }
    if (this.$store.state.logged_in_staff.role == "Manager") {
      this.$router.push("/posting")
    }
  }
};
</script>
