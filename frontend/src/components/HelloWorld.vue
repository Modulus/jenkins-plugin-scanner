<template>
  <div class="hello">
    <button class="ui button" v-on:click="fetchPlugins()">Clicketey</button>
    <h1>{{ msg }}</h1>
    <p>
      For a guide and recipes on how to configure / customize this project,<br>
      check out the
      <a href="https://cli.vuejs.org" target="_blank" rel="noopener">vue-cli documentation</a>.
    </p>
    <h3>Installed CLI Plugins</h3>
 
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  data(){
    return {
      input: {
        plugins:  ["kubernetes:123", "git:123", "bitbucket:123"]
      },
      output_plugins: []
    }
  },
  methods: {
    fetchPlugins(){
      let url = "http://localhost:5000/multi"
      console.log("Fetching plugins!")
      console.log("Sending: ", JSON.stringify(this.input))
      fetch(url, {
          method: 'POST', // *GET, POST, PUT, DELETE, etc.
          mode: 'cors', // no-cors, *cors, same-origin
          cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
          headers: {
            'Content-Type': 'application/json'
          },
          //redirect: 'follow', // manual, *follow, error
          //referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
          body: JSON.stringify(this.input) // body data type must match "Content-Type" header
      })
      .then(stream => stream.json())
      .then(result => {
        console.log("Found ", result)
      })
      .catch(error => {
        console.error("Failed to fetch data: ", error)
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
