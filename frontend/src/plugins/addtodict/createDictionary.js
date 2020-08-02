import Plugin from '@ckeditor/ckeditor5-core/src/plugin';
import imageIcon from '@ckeditor/ckeditor5-core/theme/icons/image.svg';
import ButtonView from '@ckeditor/ckeditor5-ui/src/button/buttonview';
import AddToDictCommand from './addtodictcommand' 

export default class CreateDictionary extends Plugin {
    init() {
        const editor = this.editor;

        editor.ui.componentFactory.add( 'createDict', locale => {
            const view = new ButtonView( locale );

            view.set( {
                label: 'Add to Dictionary',
                icon: imageIcon,
                tooltip: true
            } );

            // Callback executed once the image is clicked.
            view.on( 'execute', () => {
                const editor = this.editor;
                const modelDocument = this.editor.model.document;
                //const model = this.editor.model;
                const content = editor.data.toView( editor.model.getSelectedContent( modelDocument.selection ) );
                //this.editor.model.insertContent(selection)
        //		let scopeElement = model.schema.getLimitElement( selection );
                let read = ''
                let current = content['_children']
                let depth = 0
                while (depth < 3) {
                    if (current.length === 1)
                        if ('_textData' in current[0]) {
                            read = current[0]['_textData'];
                            break;
                        }
                        current = current[0]['_children']
                        depth += 1
                    
                }
                console.log(read)                
            } );

            return view;
        } );

        editor.commands.add( 'createDict', new AddToDictCommand( editor ) );

		// Set the Ctrl+U keystroke.
		editor.keystrokes.set( 'CTRL+U', 'createDict' );
    }
}