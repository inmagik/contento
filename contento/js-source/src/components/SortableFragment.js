import React, { Component } from 'react'
import { Sortable } from 'react-sortable'
import Form from "react-jsonschema-form"

class Fragment extends Component {
  constructor(props) {
    super(props)
    // this.state = {
    //   dataRaw: JSON.stringify(this.props.fragment.data)
    // }
    this.handleDataChange = this.handleDataChange.bind(this)
    this.sortableProps = this.sortableProps.bind(this)
    console.log(props)
  }

  handleDataChange({ formData }) {
    // const value = e.target.value
    // try {
      this.props.updateFragment({
        uuid: this.props.fragment.uuid,
        type: this.props.fragment.type,
        data: formData
        // ...this.props.fragment,
        // data: JSON.parse(value),
      })
    // } catch(e) {
    //   console.error('Invalid json')
    // }
    // this.setState({ dataRaw: value })
  }

  // Filter only sortable props to pass down to div...
  sortableProps() {
    return (({ schema, fragment, index, removeFragment, updateFragment, ...props }) => props)(this.props)
  }

  render() {
    const { fragment, removeFragment, schema, index } = this.props;
    // const { dataRaw } = this.state;

    return (
      <div {...this.sortableProps()}>
        <h2>{fragment.type}{index}</h2>
        <button type="button" onClick={removeFragment}>Remove</button>
        <Form schema={{ ...schema, type: 'object' }} formData={fragment.data} onChange={this.handleDataChange}>
          <div />
        </Form>
        {/* <textarea
          style={{width:'100%'}}
          value={dataRaw}
          onChange={this.handleDataChange}
        /> */}
      </div>
    )
  }
}

const SortableFragment = Sortable(Fragment)
export default SortableFragment
