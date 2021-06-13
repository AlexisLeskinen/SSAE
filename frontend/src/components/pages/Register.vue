<template>
  <div class="whole">
    <el-card v-if="login">
      <div slot="header">
        <span>用户登陆</span>
        <el-link class="header-right" @click="userRegister" :underline="false">注册</el-link>
      </div>
      <el-form :model="login_form" :rules="login_rules"
               ref="login_form" label-width="60px">
        <el-form-item label="手机:" prop="account">
          <el-input v-model="login_form.account" clearable maxlength="11" placeholder="请输入账号" type="text"/>
        </el-form-item>
        <el-form-item label="密码:" prop="password">
          <el-input v-model="login_form.password" clearable maxlength="8" placeholder="请输入密码" type="password"/>
        </el-form-item>
        <el-button type="plain" v-on:click="onBack">返回</el-button>
        <el-button type="primary" v-on:click="userLogin">登录</el-button>
      </el-form>
    </el-card>
    <div v-else>
      <el-card>
        <div slot="header">
          <span v-if="register">注册</span>
          <span v-else>用户信息修改</span>
          <el-link class="header-right" @click="backToLog" :underline="false">返回</el-link>
        </div>
        <el-form label-width="75px" size="mini" :model="user_form"
                 label-position="left" class="form-with"
                 :rules="user_rules"
                 ref="user_form"
        >
          <el-form-item label="姓名" prop="name">
            <el-input v-model="user_form.name" placeholder="请输入姓名" type="text"/>
          </el-form-item>
          <el-form-item label="性别" prop="sex">
            <el-select v-model="user_form.sex" placeholder="请选择">
              <el-option key="男" value="男" label="男"/>
              <el-option key="女" value="女" label="女"/>
            </el-select>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input
              placeholder="请输入密码"
              v-model="user_form.password"
              clearable maxlength="8" show-password>
            </el-input>
          </el-form-item>
          <el-form-item label="手机号" prop="phone">
            <el-input
              placeholder="请输入手机号"
              v-model="user_form.phone"
              clearable maxlength="11" type="tel">
            </el-input>
          </el-form-item>
          <el-form-item label="自助取件">
            <el-switch
              v-model="user_form.self_service">
            </el-switch>
          </el-form-item>
          <el-form-item label="楼号" prop="building">
            <el-input
              placeholder="楼号"
              v-model="user_form.building"
              clearable maxlength="3" type="text">
            </el-input>
          </el-form-item>
          <el-form-item label="宿舍号" prop="door">
            <el-input
              placeholder="宿舍号"
              v-model="user_form.door"
              clearable maxlength="4" type="text">
            </el-input>
          </el-form-item>
        </el-form>
        <el-button size="mini" type="primary" round @click="userSave">保存</el-button>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  name: "Register",
  data() {
    return {
      login_form: {
        account: "13802918265",
        password: "0000"
      },
      login_rules: {
        account: [
          {required: true, message: '帐号不可为空', trigger: 'blur'},
        ],
        password: [
          {required: true, message: '密码不可为空', trigger: 'blur'}
        ]
      },
      login: true,
      register: false,
      user_form: {
        name: "",
        sex: "",
        phone: "",
        building: "",
        password: "",
        door: "",
        self_service: false,
      },
      user_rules: {
        name: [
          {required: true, message: '姓名不可为空', trigger: 'blur'},
        ],
        sex: [
          {required: true, message: '性别不可为空', trigger: 'blur'},
        ],
        password: [
          {required: true, message: '密码不可为空', trigger: 'blur'},
        ],
        phone: [
          {required: true, message: '手机不可为空', trigger: 'blur'},
        ],
        building: [
          {required: true, message: '楼号不可为空', trigger: 'blur'},
        ],
        door: [
          {required: true, message: '宿舍门不可为空', trigger: 'blur'},
        ],
      },
    }
  },
  methods: {
    onBack() {
      this.$router.push('/');
    },
    backToLog() {
      let _v = this
      setTimeout(function () {
        _v.login = true
        _v.register = false
      }, 500)
    },
    userRegister() {
      let _v = this
      setTimeout(function () {
        _v.login = false
        _v.register = true
      }, 500)
    },
    userLogin() {
      let _v = this;
      _v.$refs['login_form'].validate((valid) => {
        if (valid) {
          _v.$axios.post(_v.api + 'user-login', _v.login_form).then(
            r => {
              _v.user_form = r.data.data
              _v.$message.success(r.data.msg)
              setTimeout(function () {
                _v.login = false
              }, 500)
            }
          )
        }
      });
    },
    userSave() {
      let _v = this;
      _v.$refs['user_form'].validate((valid) => {
        if (valid) {
          _v.$axios.post(_v.api + 'user-save', _v.user_form).then(
            r => {
              console.log(r.data)
              _v.user_form = r.data.data
              _v.$message.success(r.data.msg)
            }
          )
        }
      });
    },
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

.form-with {
  padding: 20px;
}
</style>
