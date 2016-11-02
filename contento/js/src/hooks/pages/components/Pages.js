import React, { Component } from 'react';
import PageList from './PageList'
import { arrayMove } from 'react-sortable-hoc'

export default class Pages extends Component {
  constructor(props) {
    super(props)
    this.onSortEnd = this.onSortEnd.bind(this)
  }

  onSortEnd({ oldIndex, newIndex }) {
    const newPages = arrayMove(this.props.pages, oldIndex, newIndex)
    this.props.updatePages(this.props.hierarchyKey, newPages)
  }

  render() {
    return (
      <div>
        <PageList
          pages={this.props.pages}
          hierarchyKey={this.props.hierarchyKey}
          updatePages={this.props.updatePages}
          togglePage={this.props.togglePage}
          onSortEnd={this.onSortEnd}
          useDragHandle={true}
        />
      </div>
    )
  }
}
