/**
 * @license Copyright (c) 2003-2020, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or https://ckeditor.com/legal/ckeditor-oss-license
 */

/**
 * @module select-all/selectallcommand
 */

import Command from '@ckeditor/ckeditor5-core/src/command';

export default class AddToDictCommand extends Command {
	/**
	 * @inheritDoc
	 */
	execute() {
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
		console.log(read)
		if (read) {
			localStorage[read] = read + '.html'
			document.getElementById("app").dispatchEvent(new CustomEvent("updateDict", {
				detail: { 'name': read + '.html', 'complete': true }}));

		}
	}
}
