<template>
  <div id="app">
    <div id="nav">
      <span style="font-weight: bold;margin-right: 4px;float: right;">
        <!-- <img :src="this.user.single.avatar_url" style="border-radius: 1000px;width: 24px;height: 24px;border: 2px solid white;" /> -->
        Hello, {{ this.user.single.first_name }}
      </span>
      <router-link to="/"><i class="el-icon-document"></i> Track Time</router-link>
      <router-link to="/time"><i class="el-icon-date"></i> View Time</router-link>
    </div>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
  components: {},
  data: function() {
    return {
      user: {},
    }
  },
  mounted: function() {
    eel.get_user()((val) => {
      this.user = val
    })
  },
  methods: {}
}
</script>

<style lang="scss">
  @import "./assets/sass/main.scss";
</style>
