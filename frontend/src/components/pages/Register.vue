<template>
  <div class="whole">
    <el-card v-if="!login">
      <div slot="header">
        <span>用户登陆</span>
        <el-dropdown class="header-right">
          <span>注册</span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item @click.native.stop="userCard">收件人注册</el-dropdown-item>
            <el-dropdown-item>工作人员注册</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
      <el-form :model="login_form" label-width="70px">

        <el-form-item label="用户ID:" prop="account">
          <el-input v-model="login_form.account" clearable maxlength="6" placeholder="请输入账号" type="text"/>
        </el-form-item>
        <el-form-item label="密码:" prop="password">
          <el-input v-model="login_form.password" clearable maxlength="8" placeholder="请输入密码" type="password"/>
        </el-form-item>
        <el-button type="plain" v-on:click="onBack">返回</el-button>
        <el-button type="primary" v-on:click="userCard">登录</el-button>
      </el-form>
    </el-card>
    <el-card v-else>
      <div slot="header">
        <span>注册</span>
      </div>
      <el-form :rules="rule" label-width="50px" :inline="true" size="mini">
        <el-form-item label="姓名">
          <el-input v-model="user_from.name" type="text"/>
        </el-form-item>
        <el-form-item label="性别">
          <el-select v-model="value" placeholder="请选择">
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <el-button @click="userCard">返回</el-button>
    </el-card>
  </div>
</template>

<script>
export default {
  name: "Register",
  data() {
    return {
      login_form: {
        account: "",
        password: ""
      },
      login: false,
      user_from: {
        name: "",
      },
      rule: {
        name: [{required: true, message: '您的姓名', trigger: 'blur'},
          {min: 2, max: 5, message: '长度在 2 到 5 个字符', trigger: 'blur'}],

      }
    }
  },
  methods: {
    onBack() {
      this.$router.push('/');
    },
    userCard() {
      let _v = this
      setTimeout(function () {
        _v.login = !_v.login
      }, 500)
    }
  }
}
</script>

<style scoped>
.whole {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  width: fit-content;
  margin: 100px auto 0 auto;
}

.header-right {
  cursor: pointer;
  color: #409EFF;
  float: right;
  padding: 3px 0;
}
</style>
