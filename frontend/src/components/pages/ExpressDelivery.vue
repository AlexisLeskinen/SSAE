<template>
  <div class="whole">
    <div class="header">
      <el-link :underline="false">{{ userinfo.building }}{{ userinfo.user }}</el-link>
      <el-link :underline="false" @click="logout">注销</el-link>
    </div>
    <el-table
      class="main-table"
      height="400"
      :data="delivery_list"
      v-loading="loading1">
      <el-table-column label="配送订单信息">
        <el-table-column
          prop="express_id"
          label="快递ID"
          width="120">
        </el-table-column>
        <el-table-column
          prop="name"
          label="收件人"
          width="80">
        </el-table-column>
        <el-table-column
          prop="door"
          label="宿舍号"
          width="120">
        </el-table-column>
        <el-table-column
          prop="phone"
          label="手机号码"
          width="150">
        </el-table-column>
        <el-table-column label="操作" width="300">
          <template slot-scope="scope">
            <el-button
              v-if="!scope.row.receive_date"
              size="mini"
              type="primary" plain
              @click="handleReceive(scope.$index, scope.row)">上门配送
            </el-button>
            <el-button v-else size="mini" disabled>已于{{ scope.row.receive_date }}签收</el-button>
          </template>
        </el-table-column>
      </el-table-column>
    </el-table>

    <el-table
      class="main-table"
      height="400"
      :data="self_service_list"
      v-loading="loading2">
      <el-table-column label="自提订单信息">
        <el-table-column
          prop="express_id"
          label="快递ID"
          width="120">
        </el-table-column>
        <el-table-column
          prop="name"
          label="收件人"
          width="80">
        </el-table-column>
        <el-table-column
          prop="locate"
          label="位置"
          width="120">
        </el-table-column>
        <el-table-column
          prop="phone"
          label="手机号码"
          width="150">
        </el-table-column>
        <el-table-column label="操作" width="300">
          <template slot-scope="scope">
            <el-button
              v-if="!scope.row.receive_date"
              size="mini"
              type="primary" plain
              @click="handleReceive(scope.$index, scope.row)">自提
            </el-button>
            <el-button v-else size="mini" disabled>已于{{ scope.row.receive_date }}签收</el-button>
          </template>
        </el-table-column>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: "ExpressDelivery",
  created() {
    let _v = this;
    this.initApi().then(
      r => {
        _v.getExpress(_v.ssl_param).then(r => {
          // console.log(r)
          _v.self_service_list = r
          _v.loading1 = false
        })
        _v.getExpress(_v.dl_param).then(r => {
          // console.log(r)
          _v.delivery_list = r
          _v.loading2 = false
        })
      }
    );
  },
  data() {
    return {
      loading1: true,
      loading2: true,
      userinfo: {},
      self_service_list: [],
      ssl_param: {},
      delivery_list: [],
      dl_param: {}
    }
  },
  methods: {
    //登出
    logout() {
      let _v = this;
      _v.$axios.get(_v.api + 'log-out').then(
        r => {
          if (r.data.msg)
            _v.$message.success(r.data.msg)
        }
      )
      _v.$router.push({
        path: "/login"
      });
    },
    //初始化获取快递的Api参数
    initApi() {
      let _v = this;
      return new Promise(function (resolve, reject) {
        _v.$axios.get(_v.api + 'admin-type').then(
          r => {
            let result = r.data
            switch (result.code) {
              case 200:
                _v.userinfo = result.data;
                let t = {
                  // 'receive_date__isnull': true,
                  'receiver__building': _v.userinfo.building,
                }
                _v.ssl_param = {
                  'locate__isnull': false,
                  'receiver__self_service': true,
                  ...t
                };
                _v.dl_param = {
                  ...t,
                  'receiver__self_service': false,
                }
                resolve()
                break;
              default:
              // _v.logout();
            }
          }
        ).catch(e => {
          reject(e)
        })
      })
    },
    // 获取自提快递信息
    getExpress(param) {
      let _v = this;
      return new Promise(function (resolve, reject) {
        _v.$axios.post(_v.api + "get-express", param)
          .then(r => {
              resolve(r.data.data);
            }
          )//获取失败
          .catch(e => {
            reject(e);
          })
      })
    },
    /**
     * 处理签收
     * @param index 快递在表格中的索引
     * @param row 快递json信息
     */
    handleReceive(index, row) {
      let _v = this;
      let param = {
        "express_id": row.express_id
      }
      _v.$axios.post(_v.api + "express-received", [param]).then(
        r => {
          _v.$axios.post(_v.api + "get-express", param).then(
            re => {
              row.receive_date = re.data.data[0].receive_date
            }
          )
        }
      ).catch(e => {
        console.log(e)
      })
    },

  }
}
</script>

<style scoped>
.whole {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  width: fit-content;
  margin: 0 auto;
}

.header {
  display: block;
  line-height: 60px;
}

.main-table {
  display: block;
  margin-bottom: 20px;
  width: fit-content;
}

</style>
