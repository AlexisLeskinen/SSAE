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
        @select="handleSelect"
        @select-all="handleSelectAll"
        v-loading="loading"
        :data="expressList"
        height="400"
        border
        stripe
        style="width: 100%">
        <el-table-column
          type="selection"
          width="50">
        </el-table-column>
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
      <el-button v-if="type===0" type="primary" class="footer-button"
                 round @click="handleExpress('express-notified')">
        通知分发快递
      </el-button>
      <div v-else class="footer-button">
        <el-button type="plain"
                   round @click="handleExpress('express-divided')">
          领取快递
        </el-button>
        <el-button type="primary"
                   round @click="handleHandOn">
          上架快递
        </el-button>
      </div>
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
      getExpressParam: "",
      expressList: [],
      buildings: [],
      selected: [],
      loading: true,
      newSelect: false,
      shelves: {},
    }
  },
  created() {
    this.initTableApi();
    this.getExpress();
  },
  methods: {
    initTableApi() {
      this.type = Number(this.$route.query.type);
      switch (this.type) {
        case 0:
          this.tableName = "总仓快递管理";
          this.getExpressParam = {
            is_divided: false
          };
          break;
        //分仓管理员
        case 1:
          this.tableName = this.$route.query.building + "分仓快递管理";
          this.getExpressParam = {
            is_notified: true,
            building: this.$route.query.building
          };
          this.shelves = new Set();
          break;
      }
    },
    updateState() {
      this.expressList.forEach(v => {
        let notifyTips = ""
        switch (this.type) {
          case 0:
            notifyTips = "已通知工作人员分发";
            break;
          case 1:
            notifyTips = "待领取";
            break;
        }
        if (v["receive_date"])
          v["state"] = "已签收";
        else if (v["locate"])
          v["state"] = "快递在" + v["building"] + "-" + v["locate"];
        else if (v["is_divide"])
          v["state"] = "已分发至" + v["building"];
        else
          v["state"] = v["is_notified"] ? notifyTips : "未通知分发";
      });
    },
    // 获取快递信息
    getExpress() {
      this.$axios.post(this.api + "get-express", this.getExpressParam)
        .then(response => {
            this.expressList = response.data;
            this.updateState();
            this.initFilterList();
            this.loading = false;
          }
        )//获取失败
        .catch(error => {
          console.log(error);
        })
    },
    // 初始化筛选列表的楼号
    initFilterList() {
      this.$axios.get(this.api + "get-warehouse")
        .then(response => {
            response.data.forEach((v) => {
              let item = {
                text: v['building'],
                value: v['building'],
              }
              this.buildings.push(item);
            });
          }
        )//获取失败
        .catch(error => {
          this.$message.error(error);
        });
    },
    filterHandler(value, row, column) {
      const property = column['property'];
      return row[property] === value;
    },
    handleSelectAll(value) {
      this.selected = value
    },
    handleSelect(value) {
      this.selected = value
    },
    //获取被选中的快递id
    getSelectedId() {
      let arr = [];
      this.selected.forEach(i => {
        arr.push({
          id: i.id,
        })
      });
      return arr
    },
    // 通知分发快递||领取快递
    handleExpress(url) {
      //只提取快递id作为参数
      let param = this.getSelectedId();

      //发起请求
      this.$axios.post(this.api + url, param).then(
        response => {
          this.$message.success(response.data);
          if (param.length)
            this.getExpress();
        }
      ).catch(error => {
        this.$message.error(error);
      })
    },
    //随机生成货架
    generalShelves() {
      let res = null
      let alp = ['A', 'B', 'C', 'D']
      let num = Math.random()
      num = Math.floor(num * 4)
      res = alp[num]
      num = Math.random()
      num = ('000000' + Math.floor(num * 100000)).slice(-6);
      res += num[0] + '-' + num[1] + '-' + num.slice(2)
      if (res in this.shelves)
        res = this.generalShelves()
      else
        this.shelves.add(res)
      return res
    },
    //上架快递
    handleHandOn() {
      //只提取快递id作为参数
      let arr = [];
      this.selected.forEach(i => {
        if (i.is_divide) {
          if (!i.locate)
            i.locate = this.generalShelves()
          arr.push({
            id: i.id,
            locate: i.locate,
          })
        }
      });
      // console.log(arr)
      //发起请求
      this.$axios.post(this.api + "express-handon", arr).then(
        response => {
          this.$message.success(response.data);
          if (arr.length)
            this.getExpress();
        }
      ).catch(error => {
        this.$message.error(error);
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

.footer-button {
  float: right;
  margin-top: 10px;
  margin-right: 10px;
}
</style>
