const customToolbarButton = function(editor){
    editor.ui.registry.addButton('myCustomToolbarButton', {
        text: 'My Custom Button',
        icon: 'user',
        onAction: function () {
            console.log(editor.selection.getContent({format : 'html'}));
          }
    });

    editor.ui.registry.addMenuItem('myCustomToolbarButton', {
        icon: 'image',
        text: 'Image',
        onAction: function () {
          console.log(editor.selection.getContent({format : 'html'}));
        }
      });
}

export {customToolbarButton};