<template>
  <div>
    <entry-card option-name="用户管理" icon="el-icon-user"/>
    <entry-card/>
  </div>
</template>

<script>
import EntryCard from "./EntryCard";

export default {
  name: "Home",
  components: {EntryCard},
  data() {
    return {};
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
