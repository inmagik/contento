import React, { Component } from 'react'
import { Sortable } from 'react-sortable'

class Fragment extends Component {
  constructor(props) {
    super(props)
    this.state = {
      dataRaw: JSON.stringify(this.props.fragment.data)
    }
    this.handleDataChange = this.handleDataChange.bind(this)
    this.sortableProps = this.sortableProps.bind(this)
  }

  handleDataChange(e) {
    const value = e.target.value
    try {
      this.props.updateFragment({
        ...this.props.fragment,
        data: JSON.parse(value),
      })
    } catch(e) {
      console.error('Invalid json')
    }
    this.setState({ dataRaw: value })
  }

  // Filter only sortable props to pass down to div...
  sortableProps() {
    return (({ fragment, index, removeFragment, updateFragment, ...props }) => props)(this.props)
  }

  render() {
    const { fragment, removeFragment, index } = this.props;
    const { dataRaw } = this.state;

    return (
      <div {...this.sortableProps()}>
        <h2>{fragment.type}{index}</h2>
        <button type="button" onClick={removeFragment}>Remove</button>
        <textarea
          style={{width:'100%'}}
          value={dataRaw}
          onChange={this.handleDataChange}
        />
      </div>
    )
  }
}

const SortableFragment = Sortable(Fragment)
export default SortableFragment
