import React, {PropTypes} from 'react';
import Pages from './Pages'

const setPages = (pages, hierarchyKey, newPages) => {
  if (hierarchyKey.length === 0) {
    return newPages.map(page => page)
  }
  return pages.map(page => {
    if (hierarchyKey[0] === page.key) {
      return {
       ...page,
       children: setPages(page.children, hierarchyKey.slice(1, hierarchyKey.lentgh), newPages)
      }
    }
    return page
 })
}

export default class SortablePages extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      pages: props.pages,
    }
    this.updatePages = this.updatePages.bind(this)
  }

  updatePages(hierarchyKey, newPages) {
    this.setState({
      pages: setPages(this.state.pages, hierarchyKey, newPages)
    }, () => this.props.savePages(this.state.pages))
  }


  render() {
    return <Pages
      hierarchyKey={[]}
      updatePages={this.updatePages}
      pages={this.state.pages}
    />
  }
}

SortablePages.propTypes = {
};
