import React, { Component } from 'react'
import SortableFragment from './SortableFragment'

export default class Region extends Component {
  constructor(props) {
    super(props)
    this.state = {
      draggingIndex: null,
    }
    this.updateSortState = this.updateSortState.bind(this)
  }

  updateSortState({ draggingIndex, items }) {
    if (draggingIndex) {
      this.setState({ draggingIndex })
    }

    if (items) {
      this.props.updateFragments(items)
    }
  }

  render() {
    const { name, updateFragment, removeFragment, fragments } = this.props;
    return (
      <div>
          <h1>{name}</h1>
          <div>
            {fragments.map((fragment, index) => (
              <SortableFragment
                key={index}
                updateState={this.updateSortState}
                items={fragments}
                draggingIndex={this.state.draggingIndex}
                sortId={index}
                outline="list"
                childProps={{
                  fragment,
                  updateFragment: (frag) => updateFragment(index, frag),
                  removeFragment: () => removeFragment(index)
                }}
              />
            ))}
          </div>
      </div>
    )
  }
}
