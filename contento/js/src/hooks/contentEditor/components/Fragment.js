import React, { Component } from 'react'
import { SortableHandle, SortableElement } from 'react-sortable-hoc'
import Form from 'react-jsonschema-form'
import MarkdownEditorWidget from '../../../widgets/MarkdownEditorWidget'

const DragHandle = SortableHandle(() => (
  <div style={{
    cursor: 'move',
  }}>
   <i className="glyphicon glyphicon-menu-hamburger" />
  </div>
))

class Fragment extends Component {
  constructor(props) {
    super(props)
    this.handleDataChange = this.handleDataChange.bind(this)
  }

  handleDataChange({ formData }) {
    this.props.updateFragmentData(formData)
  }

  getJsonSchema() {
    const jsonSchema = { ...this.props.schema, type: 'object', title: null }
    delete jsonSchema['__ui__']
    return jsonSchema
  }

  getUiSchema() {
    const jsonSchema = { ...this.props.schema }
    return jsonSchema['__ui__'] || {}
  }

  render() {
    const { fragment, fragmentTitle, removeFragment, index } = this.props;

    const schema = this.getJsonSchema()
    const uiSchema = this.getUiSchema()
    const widgets = {
      markdownEditorWidget: MarkdownEditorWidget
    }

    return (
      <div style={{
        borderTop: '1px solid #eee',
        paddingTop: '10px',
        marginTop: '10px',
       }}>
        <div>
          <div className="pull-right">
            <button type="button" className="btn btn-xs btn-danger" onClick={removeFragment}>
              <i className="glyphicon glyphicon-remove" />
            </button>
          </div>
          <div className="pull-left"><DragHandle /></div>
        </div>
        <div className="clearfix"></div>
        <h2 style={{ marginTop: '10px' }}>{fragmentTitle}</h2>
        <div style={{ paddingLeft: '1em' }}>
          <Form
            schema={schema}
            uiSchema={uiSchema}
            widgets={widgets}
            formData={fragment.data}
            onChange={this.handleDataChange}>
            <div></div>
          </Form>
        </div>
      </div>
    )
  }
}

export default SortableElement(Fragment)
