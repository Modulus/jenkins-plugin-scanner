<template>
    <div class="ui aligned center aligned grid">
      <div id="errorBox" class="twelve wide column centered ui red message"
        v-bind:class="{hidden: errorHidden}">
         <span class="errorMessage">{{errorMessage}}</span>
      </div>
 
      <div class="six wide column outline">
          <div class="ui form">
            <div class="field">
              <label>Plugins</label>
              <textarea id="inputPlugins" rows="35" v-model="input.pluginsText"></textarea>
            </div>
  
          </div>
      </div>
      <div class="six wide column outline">
        <div class="ui form">
          <div class="field">
            <label>Newest plugins</label>
            <textarea rows="35" v-model="output.pluginsText"></textarea>
            <input type="hidden" id="pluginsText" :value="pluginsCopyText">
          </div>
      </div>
    </div>
    <div class="twelve wide column  outline">
      <div class="ui">
        <button  v-bind:class="buttons.fetchClass"  v-on:click="fetchPlugins()">
            <i class="angle double down icon"></i>
          Fetch
        </button>
        <button v-bind:class="buttons.clearClass" v-on:click="clear()">
          <i class="trash icon"></i>
          Clear</button>
        <button v-bind:class="buttons.copyClass" v-on:click="copyClipBoard()">
          <i class="copy icon"></i>
          Copy
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PluginScanner',
  props: {
    msg: String
  },
  data(){
    return {
      buttons: {
        copyClass: {
            ui: true,
            button: true,
            orange: true,
            disabled: false,
            icon: true,
            labeled: true,
            loading: false
        },
        fetchClass: {
            ui: true,
            button: true,
            positive: true,
            disabled: false,
            icon: true,
            labeled: true,            
            loading: false
        },
        clearClass: {
            ui: true,
            button: true,
            disabled: false,
            loading:  false,
            icon: true,
            labeled: true,
        }
      },
      input: {
        plugins:  [],
        pluginsText: ""
      },
      output:  {
        plugins: [],
        pluginsText: ""
      },
      errorMessage: "",
      errorHidden: true
    }
  },
  computed: {
    pluginsCopyText: function(){
      return this.output.pluginsText.replace("-", "\n-")
    }
  },
  methods: {
    copyClipBoard(){
      let pluginsTextToCopy = document.querySelector("#pluginsText")
      pluginsTextToCopy.setAttribute("type", "text")
      pluginsTextToCopy.select()

      try {
        var successful = document.execCommand("copy")
        var msg = successful ? "success" : "failed"
        console.log(msg)
      } catch(err){
        this.errorMessage = err
        this.showErrorBox()
      }
      pluginsTextToCopy.setAttribute("type", "hidden")
      window.getSelection().removeAllRanges()
    },
    showErrorBox(){
      this.errorHidden = false
    },
    hideErrorBox(){
        this.errorHidden = true
    },
    lockUi(){
      document.getElementById("inputPlugins").disabled = true
      this.buttons.fetchClass.disabled = true
      this.buttons.clearClass.disabled = true
      this.buttons.fetchClass.loading = true
      this.buttons.clearClass.loading = true
      this.buttons.copyClass.disabled = true
      this.buttons.copyClass.loading = true
    },
    unlockUi(){
      document.getElementById("inputPlugins").disabled = false
      this.buttons.fetchClass.disabled = false
      this.buttons.clearClass.disabled = false
      this.buttons.fetchClass.loading = false
      this.buttons.clearClass.loading = false
      this.buttons.copyClass.loading = false
      this.buttons.copyClass.disabled = false
    },
    clear(){
      this.hideErrorBox()
      console.log("Clearing data")
      this.input.plugins = []
      this.input.pluginsText = ""
      this.output.plugins = []
      this.output.pluginsText = ""
    },
    createList(){
      this.hideErrorBox()
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
      this.hideErrorBox()
      if(this.input.pluginsText){
        let url = window.location.protocol + "//" + window.location.host +  process.env.VUE_APP_SERVICE_URL
        if(!url || process.env.NODE_ENV && process.env.NODE_ENV == "development"){
          url =  process.env.VUE_APP_SERVICE_URL
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
          if (result.plugins.length <= 0 ){
            this.errorMessage = "Did not find any matching plugins!"
            this.showErrorBox()
          }
        })
        .catch(error => {
          this.unlockUi()
          this.errorMessage = "Failed to fetch data: " + error
          console.error("Failed to fetch data: ", error)
          this.showErrorBox()
        })
      }
      else{
        let message = "Missing input!"
        console.error(message)
        this.errorMessage = message
        this.showErrorBox()
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/* .largeText {
  height: 800em;
  min-height: 50%;
  min-width: 50%;
  display: inline-block;
} */
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
