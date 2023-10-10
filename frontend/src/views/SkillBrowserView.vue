<template>
  <SkillBrowser @skills-selected="handleSkills" />
</template>

<script>
import SkillBrowser from "@/components/SkillBrowser.vue";

export default {
  components: {
    SkillBrowser,
  },
};
</script>
