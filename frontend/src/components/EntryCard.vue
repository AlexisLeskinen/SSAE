<template>
  <el-card class="box-card">
    <div slot="header" class="clearfix">
      <i class="icon-size" :class="icon"></i>
    </div>
    <el-link :href="url" :underline="false" class="text">{{ optionName }}</el-link>
  </el-card>
</template>

<script>
export default {
  name: "EntryCard",
  props: {
    icon: {
      type: String,
      default: "el-icon-setting",
    },
    optionName: {
      type: String,
      default: "功能模块",
    },
    url: {
      type: String,
      required: true,
    },
  },
  data() {
    return {};
  },
}
</script>

<style scoped>
.icon-size {
  font-size: 50px;
}

.text {
  font-size: 14px;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both;
}

.box-card {
  width: 150px;
}
</style>
