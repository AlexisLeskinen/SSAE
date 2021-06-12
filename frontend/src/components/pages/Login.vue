<template>
  <div>
    <el-form :model="form" :rules="rules" label-width="80px" class="login-box">
      <h3 class="login-title">工作人员登陆</h3>
      <el-form-item label="员工ID" prop="account">
        <el-input type="text" clearable maxlength="5" placeholder="请输入账号" v-model="form.account"/>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input type="password" clearable maxlength="8" placeholder="请输入密码" v-model="form.password"/>
      </el-form-item>
      <el-button type="plain" v-on:click="onBack">返回</el-button>
      <el-button type="primary" v-on:click="onSubmit">登录</el-button>
    </el-form>

    <el-dialog
      title="温馨提示"
      :visible.sync="dialogVisible"
      width="30%">
      <span>请输入账号和密码</span>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      form: {
        account: '26970',
        password: '0000'
      },

      // 表单验证，需要在 el-form-item 元素中增加 prop 属性
      rules: {
        username: [
          {required: true, message: '员工ID不可为空', trigger: 'blur'}
        ],
        password: [
          {required: true, message: '密码不可为空', trigger: 'blur'}
        ]
      },

      // 对话框显示和隐藏
      dialogVisible: false
    }
  },
  methods: {
    onSubmit() {
      let _v = this;
      this.$axios.post(this.api + 'log-in', this.form).then(response => {

        switch (response.data.code) {
          case 200:
          case 201:
            _v.$message.success(response.data.msg)
            setTimeout(function () {
              _v.$router.push({
                path: "/distribute"
              });
            }, 500)
            break;
          case 202:
            _v.$message.success(response.data.msg)
            setTimeout(function () {
              _v.$router.push({
                path: "/delivery"
              });
            }, 500)
            break;
          default:
            _v.$message.error(response.data.msg)
        }
      }).catch(error => {
        console.log(error);
      });
    },
    onBack() {
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>
.login-box {
  border: 1px solid #DCDFE6;
  width: 350px;
  margin: 100px auto;
  padding: 35px 15px;
  border-radius: 5px;
  -webkit-border-radius: 5px;
  -moz-border-radius: 5px;
  box-shadow: 0 0 25px #909399;
}

.login-title {
  text-align: center;
  margin: 0 auto 40px auto;
  color: #303133;
}
</style>
