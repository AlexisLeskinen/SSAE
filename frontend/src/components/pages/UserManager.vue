<template>
  <el-container class="main-table">
    <el-header>
      <div class="header-title">
        <i class="el-icon-user"></i>
        <span>用户管理</span>
      </div>
    </el-header>
    <el-container>
      <el-aside>
        <el-menu
          default-active="1">
          <el-menu-item v-for="r in userRole">
            <span slot="title">{{ r }}</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main>Main</el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  name: "UserManager",
  data() {
    return {
      userRole: [
        "总仓管理员", "分仓管理员", "分仓工作人员", "订单收件人"
      ],
    }
  }
}
</script>

<style scoped>
.main-table {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.el-header {
  border-bottom: solid 1px #e6e6e6;
}

.header-title {
  float: left;
  line-height: 60px;
}
</style>
