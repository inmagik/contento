import React, { Component } from 'react'
import { SortableHandle, SortableElement } from 'react-sortable-hoc'
import Form from 'react-jsonschema-form'

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

  render() {
    const { fragment, fragmentTitle, removeFragment, schema, index } = this.props;

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
        <div className="clearfix" />
        <h2 style={{ marginTop: '10px' }}>{fragmentTitle}</h2>
        <div style={{ paddingLeft: '1em' }}>
          <Form
            schema={{ ...schema, type: 'object', title: null }}
            formData={fragment.data}
            onChange={this.handleDataChange}>
            <div />
          </Form>
        </div>
      </div>
    )
  }
}

export default SortableElement(Fragment)
