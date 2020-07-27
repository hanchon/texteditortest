 <template>
  <div id="texto">
    <editor
      api-key="no-api-key"
      :init="initial"
      v-model="content"
      v-on:onChange="this.update"
    />
    <!-- tinymceScriptSrc: 'http://localhost:8080//js/tinymce/js/tinymce/tinymce.min.js', -->
    <!-- v-on:onChange="this.update" -->
  </div>
</template>

 <script>
import Editor from "@tinymce/tinymce-vue";

import config from '../config'

export default {
  name: "Texto",
  components: {
    editor: Editor,
  },
  computed: {
    initial(){
      return config.config;
    }
  }, 
  data: function () {
    return {
      content: this.value, // default to the passed value
      file: "",
    };
  },
  created: async function () {
    this.$parent.$on("update_text", this.update_text);
  },
  methods: {
    update: function () {
      // pass updated content back to the parent
      this.$emit("input", { content: this.content, file: this.file });
    },
    update_text: function (obj) {
      this.content = obj.text;
      this.file = obj.file;
    },
  },
};
</script>
