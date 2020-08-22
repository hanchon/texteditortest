import Plugin from '@ckeditor/ckeditor5-core/src/plugin';
import imageIcon from '@ckeditor/ckeditor5-core/theme/icons/image.svg';
import ButtonView from '@ckeditor/ckeditor5-ui/src/button/buttonview';
//import AddToDictCommand from './addtodictcommand' 


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
                console.log(content) 
                let read = ''
                let current = content['_children']
                let depth = 0
                while (depth < 3) {
                    if (current.length === 1) {
                        if ('_textData' in current[0]) {
                            read = current[0]['_textData'];
                            break;
                        }
                        current = current[0]['_children']
                        depth += 1
                    } else { //TODO ALERT SELECTION TOO BIG
                        break;}
                    
                }
                if (!read)
                    read = this.getLastWord(this.editor)
                if(!this.isEmptyOrSpaces(read)) {
                    localStorage[read] = read + '.html'
                    document.getElementById("app").dispatchEvent(new CustomEvent("updateDict", {
                        detail: { 'name': read + '.html', 'complete': true }}));
                }
                             
            } );

            return view;
        } );
    }
    
    isEmptyOrSpaces(str){
        return str === null || str.match(/^ *$/) !== null;
    }

    getLastWord( editor ) {
		console.log("asd")
		const model = editor.model;
		const document = model.document;
		const selection = document.selection;
		//const selectionParent = editor.model.document.selection.focus.parent;
		//const probe = model.createSelection( model.document.selection );

		const rangeBeforeSelection = model.createRange( model.createPositionAt( selection.focus.parent, 0 ), selection.focus );

		// Do nothing if selection is not collapsed.
		if ( !selection.isCollapsed ) {
			return;
		}

		const nodesMerged = this.mergeNodes( rangeBeforeSelection.getItems() );

		if ( !( nodesMerged && nodesMerged.length ) ) {
			return;
		}

		const dataArr = nodesMerged.split( ' ' );
		const url = dataArr[ dataArr.length - 1 ];
		return url
	}

	mergeNodes( nodeList ) {
		const _nodeList = Array.isArray( nodeList ) ? nodeList : Array.from( nodeList );
		return _nodeList.reduce( ( rangeText, node ) => {
			if ( node.is( 'softBreak' ) ) {
				return '';
			}
	
			return rangeText + node.data;
		}, '' );
	}
}