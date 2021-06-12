<template>
  <el-container class="whole">
    <el-header>
      <div>
        <div class="header-left">
          <span>{{ tableName }}</span>
          <el-link :underline="false">当前仓库快递数量：{{ expressList.length }}</el-link>
        </div>
        <!--        <el-avatar >{{ user[0] }}</el-avatar>-->
        <div class="header-right">
          <el-link :underline="false">{{ user }}</el-link>
          <el-link :underline="false" @click="logout">注销</el-link>
        </div>
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
          prop="express_id"
          label="快递id"
          width="120">
        </el-table-column>
        <el-table-column
          prop="name"
          label="姓名"
          width="120">
        </el-table-column>
        <el-table-column v-if="type===1"
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
        <el-table-column
          prop="s_s_t"
          label="自主取件">
        </el-table-column>
        <div v-if="type===0">
          <el-table-column
            prop="building"
            :filters="buildings"
            :filter-method="filterHandler"
            width="100"
            label="地址">
          </el-table-column>
        </div>
      </el-table>
      <el-button v-if="type===0" type="plain" class="footer-button-left"
                 round @click="getNewExpress">
        从校外接受快递
      </el-button>
      <el-button v-if="type===0" type="primary" class="footer-button-right"
                 round @click="updateExpress({'is_notified':true})">
        通知分发快递
      </el-button>
      <div v-else class="footer-button-right">
        <el-button type="plain"
                   round @click="updateExpress({'is_divided':true})">
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
  name: "ExpressDistribute",
  data() {
    return {
      type: 0,
      user: "",
      tableName: "",
      getExpressParam: {},
      expressList: [],
      buildings: [],
      selected: [],
      loading: true,
    }
  },
  created() {
    this.initTableApi();
  },
  methods: {
    initTableApi() {
      this.$axios.get(this.api + 'admin-type').then(
        r => {
          let result = r.data
          switch (result.code) {
            case 200:
              this.type = Number(result.data.type)
              switch (this.type) {
                //总仓管理员
                case 0:
                  this.tableName = "总仓快递管理";
                  this.getExpressParam = {
                    is_divided: false
                  };
                  break;
                //分仓管理员
                case 1:
                  this.tableName = result.data.building + "分仓快递管理";
                  this.getExpressParam = {
                    is_notified: true,
                    receiver__building: result.data.building
                  };
                  break;
              }
              this.user = result.data.user;
              break;
            default:
              this.logout();
              break;
          }
          this.getExpress();
        }
      ).catch(e => {
        this.logout();
        console.log(e);
      })
    },
    //登出
    logout() {
      let _v = this;
      _v.$axios.get(this.api + 'log-out').then(
        r => {
          if (r.data.msg)
            _v.$message.success(r.data.msg)
        }
      )
      _v.$router.push({
        path: "/login"
      });
    },
    // 获取快递信息
    getExpress() {
      this.$axios.post(this.api + "get-express", this.getExpressParam)
        .then(response => {
            this.expressList = response.data.data;
            this.initFilterList();
            this.loading = false;
          }
        )//获取失败
        .catch(error => {
          console.log(error);
        })
    }
    ,
    // 初始化筛选列表的楼号
    initFilterList() {
      this.$axios.get(this.api + "get-warehouse")
        .then(response => {
            let result = response.data;
            this.buildings = []
            result.data.forEach(i => {
              this.buildings.push({
                text: i,
                value: i
              })
            });
          }
        )//获取失败
        .catch(error => {
          console.log(error)
        });
    }
    ,
    /**
     *
     * @param value 筛选的值
     * @param row 行
     * @param column 列
     * @returns {boolean}
     */
    filterHandler(value, row, column) {
      const property = column['property'];
      return row[property] === value;
    }
    ,
    handleSelectAll(value) {
      this.selected = value
    }
    ,
    handleSelect(value) {
      this.selected = value
    }
    ,
    /**
     * 生成更新数组
     * @param mode  要跟新的字段，字典
     * @returns {*[]}
     */
    getSelectedId(mode) {
      let arr = [];
      this.selected.forEach(i => {
        let t = {
          express_id: i.express_id,
          ...mode
        }
        arr.push(t)
      });
      return arr
    }
    ,
    /**
     * 更新快递状态
     * @param mode  更新的字段
     */
    updateExpress(mode) {
      let param = this.getSelectedId(mode);

      //发起请求
      this.$axios.post(this.api + "express-update", param).then(
        response => {
          this.$message.success(response.data.msg);
          if (param.length)
            this.getExpress();
        }
      ).catch(error => {
        console.log(error)
      })
    },
    /**上架快递
     * 注意非自主取件不能上架
     */
    handleHandOn() {
      let param = this.getSelectedId(null);
      //发起请求
      this.$axios.post(this.api + "express-handon", param).then(
        response => {
          this.$message.success(response.data.msg);
          if (param.length)
            this.getExpress();
        }
      ).catch(error => {
        console.log(error)
      })
    },
    getNewExpress() {
      let num = Math.floor(Math.random() * 50)
      let _v = this;
      this.$axios.post(this.api + "new-express?num=" + num).then(r => {
        _v.$message.success(r.data.msg)
        this.getExpress();
      }).catch(e => {
        console.log(e)
      })
    }
  }
}
</script>

<style scoped>
.whole {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.el-header {
  border-bottom: solid 1px #e6e6e6;
}

.header-left {
  display: inline-block;
  float: left;
  margin-left: 10px;
  line-height: 60px;
}

.header-right {
  display: inline-block;
  float: right;
  margin-right: 20px;
  line-height: 60px;
}

.footer-button-left {
  float: left;
  margin-top: 10px;
  margin-left: 10px;
}

.footer-button-right {
  float: right;
  margin-top: 10px;
  margin-right: 10px;
}
</style>
