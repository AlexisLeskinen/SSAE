<template>
  <div class="whole">
    <el-card class="card" style="margin-top: 100px">
      <span slot="header"><i class="el-icon-user-solid"></i>工作人员登陆</span>
      <el-form :model="form" :rules="rules" label-width="80px" ref="form">
        <el-form-item label="员工ID" prop="account">
          <el-input type="text" clearable maxlength="5" placeholder="请输入账号" v-model="form.account"/>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input type="password" clearable maxlength="8" placeholder="请输入密码" v-model="form.password"/>
        </el-form-item>
        <el-button type="plain" v-on:click="onBack">返回</el-button>
        <el-button type="primary" v-on:click="onSubmit">登录</el-button>
      </el-form>
    </el-card>
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
        account: [
          {required: true, message: '员工ID不可为空', trigger: 'blur'},
        ],
        password: [
          {required: true, message: '密码不可为空', trigger: 'blur'}
        ]
      },
    }
  },
  methods: {
    onSubmit() {
      let _v = this;
      _v.$refs['form'].validate(v => {
        if (v) {
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
        }
      });
    },
    onBack() {
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>
.whole {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  width: fit-content;
  margin: 0 auto;
}
</style>
