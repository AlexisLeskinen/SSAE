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
      <el-main>
        <el-table
          border
          stripe
          :data="accountList"
          style="width: 100%">
          <el-table-column
            prop="id"
            label="人员id">
          </el-table-column>
          <el-table-column
            prop="name"
            label="姓名">
          </el-table-column>
          <el-table-column
            prop="phone"
            label="联系方式">
          </el-table-column>
          <el-table-column
            prop="address"
            label="地址">
          </el-table-column>
          <el-table-column label="操作" width="160">
            <template slot-scope="scope">
              <el-button
                size="mini"
                @click="handleEdit(scope.$index)">编辑
              </el-button>
              <el-button
                size="mini"
                type="danger"
                @click="handleDelete(scope.$index, scope.row)">删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-main>
    </el-container>
    <info-edit-dialog :dialog-visible="dialogVisible" v-on:finish="editFinish"/>
  </el-container>
</template>

<script>
import InfoEditDialog from "../InfoEditDialog";

export default {
  name: "UserManager",
  components: {InfoEditDialog},
  data() {
    return {
      dialogVisible: false,
      userRole: [
        "总仓管理员", "分仓管理员", "分仓工作人员", "订单收件人"
      ],
      accountList: [{
        id: "00000",
        name: "甲",
        phone: 123456789,
        address: "暨大总仓"
      }, {
        id: "00001",
        name: "乙",
        phone: 123456789,
        address: "暨大总仓"
      }],
    }
  },
  methods: {
    handleEdit(index) {
      this.dialogVisible = true;

    },
    editFinish() {
      this.dialogVisible = false
    },
    handleDelete(index, row) {
      console.log(index, row);
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
