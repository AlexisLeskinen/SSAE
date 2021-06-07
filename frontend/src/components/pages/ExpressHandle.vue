<template>
  <el-container class="main-table">
    <el-header>
      <div class="header-title">
        <i class="el-icon-user"></i>
        <span>{{ tableName }}</span>
      </div>
    </el-header>
    <el-main>
      <el-table
        v-loading="loading"
        :data="expressList"
        height="350"
        border
        style="width: 100%">
        <el-table-column
          prop="id"
          label="快递id"
          width="120">
        </el-table-column>
        <el-table-column
          prop="receiver"
          label="姓名"
          width="120">
        </el-table-column>
        <el-table-column
          prop="building"
          width="60"
          label="地址">
        </el-table-column>
        <el-table-column
          prop="state"
          label="快递状态">
        </el-table-column>
        <el-table-column
          prop="receive_date"
          label="签收时间">
        </el-table-column>
      </el-table>
    </el-main>
  </el-container>
</template>

<script>

export default {
  name: "ExpressHandle",
  props: {
    tableName:  "快递管理",
  },
  data() {
    return {
      userRole: [
        "总仓管理员", "分仓管理员",
      ],
      expressList: [],
      loading: true,
    }
  },
  created() {
    this.tableName = this.$route.query.tableName;
    // 组件创建完后获取数据，
    // 此时 data 已经被 observed 了
    this.getExpress()
  },
  methods: {
    getExpress() {
      this.$axios.get(this.api + this.$route.query.apiParam)
        .then(response => {
            this.expressList = response.data
            this.expressList.forEach(v => {
              if (v["receive_date"])
                v["state"] = "已签收"
              else if (v["locate"])
                v["state"] = "快递在" + v["building"] + "-" + v["locate"]
              else if (v["is_divide"])
                v["state"] = "已分发至" + v["building"]
              else
                v["state"] = v["is_notified"] ? "已通知分发" : "未通知分发"
            })

            this.loading = false
          }
        )//获取失败
        .catch(error => {
          console.log(error);
        })
    },
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
  line-height: 60px;
}
</style>
