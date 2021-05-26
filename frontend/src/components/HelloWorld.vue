<template>
  <el-switch v-model="value" active-color="#13ce66" inactive-color="#ff4949">
  </el-switch>
</template>

<script>
export default {
  name: 'HelloWorld',
  data () {
    return {
       value:true
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
