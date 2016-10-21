import React, { Component } from 'react'
import SortableFragment from './SortableFragment'
import uuid from 'node-uuid'

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
    const {
      name,
      updateFragment,
      removeFragment,
      addFragment,
      fragments,
      fragmentTypes,
    } = this.props;
    // console.log(name, 'RENDER!', fragments)

    return (
      <div>
          <h1>{name}</h1>
          <div>
            <select ref={(ref) => this.select = ref}>
              {this.props.fragmentsTypes.map(({ title, name }) => (
                <option key={name} value={name}>{title}</option>
              ))}
            </select>
            <button type="button" onClick={() => addFragment({ type: this.select.value, data: {}, uuid: uuid.v4() })}>Add</button>
          </div>
          <div>
            {fragments.map((fragment, index) => {

              console.log(index)
              return <SortableFragment
                key={fragment.uuid}
                updateState={this.updateSortState}
                items={fragments}
                draggingIndex={this.state.draggingIndex}
                sortId={index}
                outline="list"
                childProps={{
                  index: fragment.uuid,
                  fragment,
                  updateFragment: (frag) => updateFragment(index, frag),
                  removeFragment: () => removeFragment(index)
                }}
              />
            })}
          </div>
      </div>
    )
  }
}
