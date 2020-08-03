<template>
  <div class="home">
    <h1>Jenkins Plugin Scanner</h1>
    <PluginScanner/>
  </div>
</template>

<script>
// @ is an alias to /src
import PluginScanner from '@/components/PluginScanner.vue'

export default {
  name: 'Home',
  components: {
    PluginScanner
  }
}
</script>
