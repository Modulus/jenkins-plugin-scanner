<template>
    <div class="ui aligned center aligned grid">
 
      <div class="six wide column outline">
          <div class="ui form">
            <div class="field">
              <label>Plugins</label>
              <textarea id="inputPlugins" class="largeText" v-model="input.pluginsText"></textarea>
            </div>
  
          </div>
      </div>
      <div class="six wide column outline">
        <div class="ui form">
          <div class="field">
            <label>Newest plugins</label>
            <textarea disabled v-model="output.pluginsText"></textarea>
          </div>
      </div>
    </div>
    <div class="twelve wide column  outline">
      <div class="ui buttons">
        <button  v-bind:class="buttons.fetchClass"  v-on:click="fetchPlugins()">Fetch</button>
        <div class="or"></div>
        <button v-bind:class="buttons.clearClass" v-on:click="clear()">Clear</button>
      </div>
    </div>
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
      buttons: {
        fetchClass: {
            ui: true,
            button: true,
            positive: true,
            disabled: false,
            loading: false
        },
        clearClass: {
            ui: true,
            button: true,
            disabled: false,
            loading:  false
        }
      },
      input: {
        plugins:  [],
        pluginsText: ""
      },
      output:  {
        plugins: [],
        pluginsText: ""
      }
    }
  },
  methods: {
    lockUi(){
      document.getElementById("inputPlugins").disabled = true
      this.buttons.fetchClass.disabled = true
      this.buttons.clearClass.disabled = true
      this.buttons.fetchClass.loading = true
      this.buttons.clearClass.loading = true
    },
    unlockUi(){
      document.getElementById("inputPlugins").disabled = false
      this.buttons.fetchClass.disabled = false
      this.buttons.clearClass.disabled = false
      this.buttons.fetchClass.loading = false
      this.buttons.clearClass.loading = false
    },
    clear(){
      console.log("Clearing data")
      this.input.plugins = []
      this.input.pluginsText = ""
      this.output.plugins = []
      this.output.pluginsText = ""
    },
    createList(){
      console.log("Creating list from text area input data")
      console.log(this.input.pluginsText)
      if(this.input.pluginsText){
        let  array = this.input.pluginsText.trim().split("\n")
        this.input.plugins = array.map(value =>  {
          console.debug("Changing array valut", value)
          if(value.includes("-")){
            value = value.replace("-", "")
          }
          value = value.trim()
          console.log("Altered value: ", value)
          return value
        })
        console.log(this.input.plugins)
      }
      else {
        console.error("Missing input text!")
      }
    },
    fetchPlugins(){
      if(this.input.pluginsText){
        let url = process.env.VUE_APP_SERVICE_URL
        if(!url){
          url = "http://localhost:5000/multi"
        }
       
        console.log("Fetching plugins from: ", url)
        this.lockUi()
        this.createList()
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
          this.output.pluginsText = ""
          result.plugins.forEach(element => {
            console.log("Current element", element)
            if(element){
              let yamlStr = "- ".concat(element).concat("\n")
              this.output.pluginsText = this.output.pluginsText.concat(yamlStr)
            }
          });
          this.unlockUi()
        })
        .catch(error => {
          this.unlockUi()
          console.error("Failed to fetch data: ", error)
        })
      }
      else{
        console.error("Missing input!")
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.largeText {
  height: 800em;
  min-height: 50%;
  min-width: 50%;
  display: inline-block;
}
.outline {
  border:  1px black;
}
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
