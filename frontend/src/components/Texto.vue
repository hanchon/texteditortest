<template>
    <div id="ck">
        <ckeditor :editor="editor" v-model="editorData" :config="editorConfig" @ready="onReady" ></ckeditor>
    </div>
</template>

<script>
    // ⚠️ NOTE: We don't use @ckeditor/ckeditor5-build-classic any more!
    // Since we're building CKEditor from source, we use the source version of ClassicEditor.
    import ClassicEditor from '@ckeditor/ckeditor5-editor-classic/src/classiceditor';

    import EssentialsPlugin from '@ckeditor/ckeditor5-essentials/src/essentials';
    import BoldPlugin from '@ckeditor/ckeditor5-basic-styles/src/bold';
    import ItalicPlugin from '@ckeditor/ckeditor5-basic-styles/src/italic';
    import LinkPlugin from '../plugins/ckeditor5-link/src/link';
    import ParagraphPlugin from '@ckeditor/ckeditor5-paragraph/src/paragraph';
    import AutoLink from '../plugins/autolink/autolink';
    import ClickObserver from '@ckeditor/ckeditor5-engine/src/view/observer/clickobserver';

    export default {
        name: 'ck',
        data() {
            return {
                editor: ClassicEditor,
                editorData: '<p>Content of the editor.</p>',
                editorConfig: {
                    plugins: [
                        EssentialsPlugin,
                        BoldPlugin,
                        ItalicPlugin,
                        LinkPlugin,
                        ParagraphPlugin,
                        AutoLink,
                        ClickObserver
                    ],

                    toolbar: {
                        items: [
                            'bold',
                            'italic',
                            'undo',
                            'redo'
                        ]
                    }
                }
            };
        },
        created: async function () {
          this.$parent.$on("update_text", this.update_text);
          this.$on("change", this.onReady);
        },
        methods: {
          update: function () {
            // pass updated content back to the parent
            this.$emit("input", { content: this.content, file: this.file });
          },
          update_text: function (obj) {
            console.log(this.editorData)
            this.editorData = obj.text;
            this.file = obj.file;
          },
          onReady( editor )  {
                // Insert the toolbar before the editable area.
                console.log('ready', editor)
                
            },
        }
    };
</script>
