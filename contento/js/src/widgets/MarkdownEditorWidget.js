import React, { Component } from 'react'
import ace from 'brace'

require('brace/mode/markdown')
require('brace/theme/github')

export default class MarkdownEditorWidget extends Component {
  componentDidMount() {
    const { value, onChange } = this.props
    this.editor = ace.edit(this.editorElement);
    // TODO: Make mode dynamic... as options for ui:widget
    this.editor.getSession().setMode('ace/mode/markdown');
    this.editor.setTheme('ace/theme/github');
    this.editor.setValue(value || '')
    this.editor.clearSelection()
    this.editor.on('change', e => onChange(this.editor.getValue()))
  }

  componentWillReceiveProps(nextProps) {
    if (this.props.value !== nextProps.value && nextProps.value !== this.editor.getValue()) {
      this.editor.setValue(nextProps.value)
      this.editor.clearSelection()
    }
  }

  componentWillUnmount() {
    this.editor.destroy()
    this.editor = null
  }

  render() {
    return (
      <div
        style={{ height: '200px' }}
        ref={(element) => this.editorElement = element}>
      </div>
    )
  }
}

MarkdownEditorWidget.propTypes = {
}
