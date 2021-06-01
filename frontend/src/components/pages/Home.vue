<template>
  <el-row type="flex" justify="space-around">
    <entry-card v-for="item in enrtyList"
                :icon="item.icon"
                :option-name="item.optionName"
                :url="item.url"/>
  </el-row>
</template>

<script>
import EntryCard from "../EntryCard";

export default {
  name: "Home",
  components: {EntryCard},
  data() {
    return {
      enrtyList: [
        {
          icon: "el-icon-user",
          optionName: "用户管理",
          url: "/admin"
        },
        {
          icon: "el-icon-box",
          optionName: "收件模块",
          url: ""
        },
        {
          icon: "el-icon-receiving",
          optionName: "配送模块",
          url: ""
        }],
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
