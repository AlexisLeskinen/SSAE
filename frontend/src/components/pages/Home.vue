<template>
  <div class="home">
    <el-row type="flex" justify="space-around" align="middle">
      <entry-card
        v-for="item in enrtyList"
        :icon="item.icon"
        :option-name="item.optionName"
        :url="item.url"
      />
    </el-row>
    <el-row style="margin-top: 50px">
      <el-button>
        <el-link href="https://shotgun.zone/admin/"
                 target="_blank" :underline="false">
          进入系统后台
        </el-link>
      </el-button>
    </el-row>
  </div>
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
          optionName: "用户信息管理",
          url: "/user",
        },
        {
          icon: "el-icon-box",
          optionName: "校内快递流转",
          url: "/login",
        },
        {
          icon: "el-icon-receiving",
          optionName: "自提与配送",
          url: "/login",
        },
      ],
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.home {
  margin-top: 100px;
}
</style>
