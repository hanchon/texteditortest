 <template>
  <div id="texto">
    <editor
      api-key="no-api-key"
      :init="{
         height: 800,
         menubar: false,
         plugins: [
           'advlist autolink lists link image charmap print preview anchor',
           'searchreplace visualblocks code fullscreen',
           'insertdatetime media table paste code help wordcount'
         ],
         toolbar:
           'undo redo | formatselect | bold italic backcolor | \
           alignleft aligncenter alignright alignjustify | \
           bullist numlist outdent indent | removeformat | help'
       }"
      v-model="content"
      v-on:onChange="this.update"
    />
    <!-- tinymceScriptSrc: 'http://localhost:8080//js/tinymce/js/tinymce/tinymce.min.js', -->
    <!-- v-on:onChange="this.update" -->
  </div>
</template>

 <script>
import Editor from "@tinymce/tinymce-vue";

export default {
  name: "Texto",
  components: {
    editor: Editor,
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
