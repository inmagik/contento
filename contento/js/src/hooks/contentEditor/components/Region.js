import React, { Component } from 'react'
import FragmentList from './FragmentList'
import { arrayMove } from 'react-sortable-hoc'

export default class Region extends Component {
  constructor(props) {
    super(props)
    this.onSortEnd = this.onSortEnd.bind(this)
  }

  onSortEnd({ oldIndex, newIndex }) {
    const newFragments = arrayMove(this.props.fragments, oldIndex, newIndex)
    this.props.updateFragments(newFragments)
  }

  getFragmenTypes() {
    const { fragmentsSchemas } = this.props
    return Object.keys(fragmentsSchemas).map(name => (
      { name, title: fragmentsSchemas[name].title }
    ))
  }

  render() {
    const {
      name,
      updateFragment,
      updateFragmentData,
      removeFragment,
      addFragment,
      fragments,
      fragmentsSchemas,
    } = this.props;

    const fragmentsTypes = this.getFragmenTypes()

    return (
      <div>
          <h1>{name}</h1>
          <div className="form-group" style={{ padding: '1em' }}>
             <select className="form-control" ref={(ref) => this.select = ref}>
              {fragmentsTypes.map(({ title, name }) => (
                <option key={name} value={name}>{title}</option>
              ))}
            </select>
            <button
              style={{ marginTop: '5px' }}
              className="btn btn-success"
              type="button"
              onClick={() => addFragment({ type: this.select.value, data: {} })}>Add Fragment</button>
          </div>
          <div style={{ marginLeft: '1em' }}>
            <FragmentList
              name={name}
              fragments={fragments}
              onSortEnd={this.onSortEnd}
              useDragHandle={true}
              fragmentsSchemas={fragmentsSchemas}
              updateFragment={updateFragment}
              updateFragmentData={updateFragmentData}
              removeFragment={removeFragment}
            />
          </div>
      </div>
    )
  }
}
