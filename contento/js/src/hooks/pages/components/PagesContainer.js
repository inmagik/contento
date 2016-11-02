import React, { Component } from 'react'
import Pages from './Pages'

// Traverse le pages tree and call update on finally page list of tree
const traversePages = (update, pages, hierarchyKey) => {
  const traverse = (pages, hierarchyKey) => {
    if (hierarchyKey.length === 0) {
      return update(pages)
    }
    return pages.map(page => {
      if (hierarchyKey[0] === page.viewUrl) {
        return {
         ...page,
         children: traverse(page.children, hierarchyKey.slice(1, hierarchyKey.lentgh))
        }
      }
      return page
    })
  }
  return traverse(pages, hierarchyKey)
}

const setNewPages = (pages, hierarchyKey, newPages) =>
  traversePages(() => newPages.map(page => page), pages, hierarchyKey)

const togglePage = (pages, hierarchyKey, pageToToggle) =>
  traversePages(pages => pages.map(page => {
    if (page === pageToToggle) {
      return { ...page, toggled: !page.toggled }
    }
    return page
  }), pages, hierarchyKey)

export default class PagesContainer extends Component {
  constructor(props) {
    super(props)
    this.state = {
      pages: props.pages,
    }
    this.updatePages = this.updatePages.bind(this)
    this.togglePage = this.togglePage.bind(this)
  }

  save() {
    this.props.save(this.state.pages)
  }

  togglePage(hierarchyKey, pageToToggle) {
    this.setState({
      pages: togglePage(this.state.pages, hierarchyKey, pageToToggle)
    }, this.save)
  }

  updatePages(hierarchyKey, newPages) {
    this.setState({
      pages: setNewPages(this.state.pages, hierarchyKey, newPages)
    }, this.save)
  }

  render() {
    return <Pages
      hierarchyKey={[]}
      updatePages={this.updatePages}
      togglePage={this.togglePage}
      pages={this.state.pages.map(page => page)}
    />
  }
}
