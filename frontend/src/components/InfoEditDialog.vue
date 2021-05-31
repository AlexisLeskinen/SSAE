<template>
  <el-dialog
    title="修改信息"
    :visible="dialogVisible"
    width="30%"
    :before-close="handleClose">
    <span>这是一段信息</span>
    <span slot="footer" class="dialog-footer">
    <el-button @click="handleFinish">取 消</el-button>
    <el-button type="primary" @click="handleFinish">确 定</el-button>
  </span>
  </el-dialog>
</template>

<script>
export default {
  name: "InfoEditDialog",
  props: {
    dialogVisible: {
      type: Boolean,
      default: false,
    }
  },
  data() {
    return {};
  },
  methods: {
    handleClose(done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          done();
        })
        .catch(_ => {
        });
    },
    handleFinish() {
      this.$emit('finish',this.dialogVisible)
    }
  }
}
</script>

<style scoped>

</style>
