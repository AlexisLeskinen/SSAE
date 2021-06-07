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
        height="400"
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
        <el-table-column v-if="type===0"
                         prop="building"
                         :filters="buildings"
                         :filter-method="filterHandler"
                         width="100"
                         label="地址">
        </el-table-column>
        <el-table-column v-else
                         prop="locate"
                         width="100"
                         label="放置位置">
        </el-table-column>
        <el-table-column
          prop="phone"
          label="电话">
        </el-table-column>
        <el-table-column
          prop="state"
          label="快递状态" align="center">
        </el-table-column>
        <!--        分仓功能-->
        <el-table-column v-if="type===1"
                         prop="receive_date"
                         label="签收时间">
        </el-table-column>
      </el-table>
      <el-button type="primary" class="footer-button"
                 round @click="handOut">
        {{ handleButton }}
      </el-button>
    </el-main>
  </el-container>
</template>

<script>

export default {
  name: "ExpressHandle",
  data() {
    return {
      type: 0,
      tableName: "",
      apiParam: "",
      expressList: [],
      buildings: [],
      handleButton: "",
      loading: true,
    }
  },
  created() {
    this.initTable();
    this.getExpress();
  },
  methods: {
    initTable() {
      this.type = Number(this.$route.query.type);
      switch (this.type) {
        case 0:
          this.tableName = "总仓快递管理";
          this.apiParam = "get-express?divide=0";
          this.handleButton = "一键通知分发"
          break;
        case 1:
          this.tableName = this.$route.query.bulidng + "分仓快递管理";
          this.apiParam = "get-express?divide=1&building=" + this.$route.query.bulidng;
          this.handleButton = "一键上架"
      }
    },
    getExpress() {
      this.$axios.get(this.api + this.apiParam)
        .then(response => {
            this.expressList = response.data;
            let s = new Set();
            this.expressList.forEach(v => {
              if (v["receive_date"])
                v["state"] = "已签收"
              else if (v["locate"])
                v["state"] = "快递在" + v["building"] + "-" + v["locate"]
              else if (v["is_divide"])
                v["state"] = "已分发至" + v["building"]
              else
                v["state"] = v["is_notified"] ? "已通知工作人员分发" : "未通知分发"

              if (this.type === 0)
                s.add(v["building"]);

            });
            for (let sKey of s) {
              let item = {
                text: sKey,
                value: sKey,
              }
              this.buildings.push(item);
            }
            this.loading = false;
          }
        )//获取失败
        .catch(error => {
          console.log(error);
        })
    },
    filterHandler(value, row, column) {
      const property = column['property'];
      return row[property] === value;
    },
    // 分发快递
    handOut() {

      this.$message({
        message: "通知成功",
        type: "success"
      });
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

.footer-button {
  float: right;
  margin-top: 10px;
  margin-right: 10px;
}
</style>
