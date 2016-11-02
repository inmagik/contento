import React, { Component } from 'react';
import Page from './Page'

export default class Pages extends Component {
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
      this.props.updatePages(this.props.hierarchyKey, items)
    }
  }

  render() {
    return (
      <div>
        {this.props.pages.map((page, index) => (
          <Page
            key={page.viewUrl}
            updateState={this.updateSortState}
            items={this.props.pages}
            draggingIndex={this.state.draggingIndex}
            sortId={index}
            outline="list"
            childProps={{
              hierarchyKey: this.props.hierarchyKey,
              updatePages: this.props.updatePages,
              togglePage: this.props.togglePage,
              page: page
            }}
          />
        ))}
      </div>
    )
  }
}
