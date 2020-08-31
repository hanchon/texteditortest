<template>
    <div id="ck" class="ck-editor" @click="imActive">
        <ckeditor :editor="editor" v-model="editorData" :config="editorConfig" @ready="onReady" @input="onEditorInput" ></ckeditor>
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
    import ImagePlugin from '@ckeditor/ckeditor5-image/src/image';
    import ImageStylePlugin from '@ckeditor/ckeditor5-image/src/imagestyle';
    import ImageResizePlugin from '@ckeditor/ckeditor5-image/src/imageresize';
    //import ImageToolbar from '@ckeditor/ckeditor5-image/src/imagetoolbar';
    //import AutoLink from '../plugins/autolink/autolink';
    //import AddToDict from '../plugins/addtodict/addtodict';
    import List from '@ckeditor/ckeditor5-list/src/list';
    import CreateDictionary from '../plugins/addtodict/createDictionary';
    import AutoLink from '../plugins/ckeditor5-link/src/autolink';
    import Heading from '@ckeditor/ckeditor5-heading/src/heading';
    

    export default {
        name: 'ck',
        props: {
            id:Number
        },
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
                        List,
                        CreateDictionary,
                        ImagePlugin,
                        ImageStylePlugin,
                        ImageResizePlugin,
                        Heading
                    ],

                    toolbar: {
                        items: [
                            'heading',
                            'bold',
                            'italic',
                            '|',
                            'undo',
                            'redo',
                            '|',
                            'numberedList',
                            'bulletedList',
                            'createDict',
                            'imageStyle:side',
                        ]
                    },
                }
            };
        },
        created: async function () {
          this.$parent.$on("update_text", this.update_text);
          this.$on("change", this.onReady);          
        },
        methods: {
          imActive (){
              this.$emit("active", this.id)
          },
          onEditorInput: function () {
            // pass updated content back to the parent
            this.$emit("input", { content: this.editorData, file: this.file });
          },
          update_text: function (obj) {
            if (obj.panel == this.id) {
                this.editorData = obj.text;
                this.file = obj.file;
                this.$emit("update", { content: this.editorData, file: this.file });
            }
          },
          onReady( editor )  {
                // Insert the toolbar before the editable area.
                console.log('ready', editor)
                editor.ui.view.editable.element.style.minHeight = '100px'
                
            },
        }
    };
</script>

<style>
    .ck-editor{
        position:relative;
    }

</style>