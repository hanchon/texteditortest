import { customToolbarButton } from './custom-Toolbar.js'

const config = {
    select: "#app-editor",
    plugins:  [
        'advlist autolink lists link image charmap print preview anchor',
        'searchreplace visualblocks code fullscreen',
        'insertdatetime media table paste code help wordcount contextmenu myCustomToolbarButton'
      ],
    toolbar:  'undo redo | formatselect | bold italic backcolor | \
    alignleft aligncenter alignright alignjustify | \
    bullist numlist outdent indent | removeformat | myCustomToolbarButton',
    contextmenu: "undo link myCustomToolbarButton",
    setup: function() {
        window.tinymce.PluginManager.add('myCustomToolbarButton', customToolbarButton);
    }
}

export default { config };